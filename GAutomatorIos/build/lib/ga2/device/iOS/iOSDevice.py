# -*- coding: UTF-8 -*-
from ga2.device.device import Device

import cv2
import os
import numpy
import logging
import time
import re
from ga2.device.device import Device
from ga2.device.device import DeviceType
from ga2.device.device import DeviceOrientation
from ga2.device.iOS.iMobiledevice import IMobileDevice
from ga2.device.iOS.wdaManager import WdaManager
from ga2.device.iOS.iProxyManager import IProxyManager
from ga2.engine.engineFactory import EngineFactory
from ga2.engine.unityEngine import UnityEngine
from ga2.common.constants import *
from ga2.common.logger_config import logger
from ga2.common.cmdExecuter import CmdExecuter
from ga2.common.utils import *
from ga2.cloud import platform_helper
import atexit


class IOSDevice(Device):
    __device_sdk_port = "27019"

    '''
    param: wdaport: the local port you have forward to the device
    '''

    def __init__(self, udid):
        self.imobile_cmder = IMobileDevice(udid)
        self.__iproxy = IProxyManager(udid)
        self.__engine_connector = None
        self.__wda_connector = None

        def __get_wdaport_by_udid(udid):
            outputlines = CmdExecuter.executeAndWait("ps -ef|grep \"iproxy [0-9]\+ 8100 " + udid + "\"")
            for line in outputlines:
                ret = re.search("iproxy ([0-9]+) 8100 " + udid, line.decode("utf-8"))
                if ret:
                    return ret.group(1)
            outputlines = CmdExecuter.executeAndWait("ps -ef|grep \"iproxy [0-9]\+ 8100" + "\"")
            for line in outputlines:
                ret = re.search("iproxy ([0-9]+) 8100$", line.decode("utf-8"))
                if ret:
                    return ret.group(1)
            logger.warn("No wda port detected for device.. " + udid)
            return None

        wdaport = os.environ.get("WDA_LOCAL_PORT", __get_wdaport_by_udid(udid))
        if wdaport:
            logger.info("wda port detected: " + wdaport)
            self.__wda_connector = WdaManager(wdaport, os.environ.get("PLATFORM_IP", "127.0.0.1"))

        atexit.register(self.__cleanup)
        pass

    def engine_connector(self):
        return self.__engine_connector

    def wda_session(self):
        if self.__wda_connector is None:
            logger.error("wda connector is not inited... plsease make sure wda is connectable")
        return self.__wda_connector.get_session()

    def __cleanup(self):
        if self.__iproxy:
            self.__iproxy.removeAllForwards()

    # def __del__(self):
    #     if self.iproxy:
    #         self.iproxy.removeAllForwards()

    '''
    params: appfile:path to .ipa file
    '''

    # def install(self,appfile):
    #     self.imobile_cmder.install(appfile)
    #
    # def uninstall(self,appid):
    #     self.imobile_cmder.uninstall(appid)

    def device_type(self):
        return DeviceType.DEVICE_IOS

    '''
    init engine gautomator sdk(create a valid client to sdk)
    param:  local_engine_port: a free port used to forward to device engine port
            timeout: engine connecting timeout in seconds
            if running in cloud , a free port will be forward instead of the given param
    '''

    @callLog
    def init_engine_sdk(self, engine_type, local_engine_port="53001", timeout=60):
        local_engine_port = os.environ.get("LOCAL_ENGINE_PORT", local_engine_port)
        if local_engine_port is None:
            local_engine_port = "53001"
        if isInCloudMode():
            response = platform_helper.get_platform_client().platform_forward(self.__device_sdk_port)
            if response is None:
                return ERR_CLOUD_PLATFORM
            else:
                local_engine_port = response["localPort"]
        else:
            self.__forward(local_engine_port, self.__device_sdk_port)
        counts = int(timeout / 2 + 1)
        for i in range(counts):
            try:
                self.__engine_connector = EngineFactory.createEngine(engine_type, os.environ.get("PLATFORM_IP", "127.0.0.1"), int(local_engine_port))
                if self.__engine_connector is None:
                    logger.error("create engine failed . invalid type : " + str(engine_type))
                    return ERR_INVALID_ENGINETYPE
                version = self.__engine_connector.get_sdk_version()
                if version:
                    logger.debug(version)
                    return ERR_SUCCEED
            except Exception as e:
                time.sleep(2)
        logger.error("init engine sdk timeout")
        return ERR_CONNECT_TO_SDK_FAILED

    @callLog
    def launch(self, appid, timeout=60, alert_handler=None):
        if self.__wda_connector is None:
            logger.error("wda connector is not inited... plsease make sure wda is connectable")
            return ERR_WDA_NOT_RUNNING
        session = self.__wda_connector.new_session(bundleid=appid)
        if alert_handler is None:
            alert_handler = self.__default_alert_callback
        for i in range(0, 10):
            time.sleep(3)
            cur_top_app = self.get_top_app()
            logger.info("current top app is :" + cur_top_app + "target is: " + appid)
            if cur_top_app != appid:
                alert_handler(session)
            else:
                break
        return ERR_SUCCEED

    def start_alert_handler(self, handler=None):
        if self.__wda_connector is None:
            logger.error("wda connector is not inited... plsease make sure wda is connectable")
            return ERR_WDA_NOT_RUNNING
        if handler is None:
            handler = self.__default_alert_callback
        logger.info("setting alert handler...")
        self.__wda_connector.get_session().set_alert_callback(handler)
        return ERR_SUCCEED

    def __default_alert_callback(self, session):
        btns = set([u'稍后', u'稍后提醒我', u'不再提醒', u'无线局域网与蜂窝移动网络', u'允许', u'知道了', u'确定', u'好']).intersection(
            session.alert.buttons())
        if len(btns) == 0:
            logger.warn("Alert  not handled, buttons: " + ', '.join(session.alert.buttons()))
            return
        logger.info('alert handled：' + str(list(btns)[0]))
        session.alert.click(list(btns)[0])
        pass

    def get_top_app(self):
        if self.__wda_connector is None:
            logger.error("wda connector is not inited... plsease make sure wda is connectable")
            return None
        return self.__wda_connector.get_top_bundleid()

    # @callLog
    # def foreground(self,appid):
    #     self.wda_connector.get_session(appid).activate(1)

    '''
    For now , just kill the app launched by device interface. It's better to save a map as {appid:session}
    '''

    def kill(self, appid=None):
        self.__wda_connector.close_session(appid)

    def home(self):
        self.__wda_connector.wda_client.home()

    @callLog
    def screenshot(self, localpath=None):
        pngdata = self.__wda_connector.wda_client.screenshot(localpath)
        pngarr = numpy.fromstring(pngdata, numpy.uint8)
        cv_image = cv2.imdecode(pngarr, cv2.IMREAD_UNCHANGED)
        return cv_image

    def __forward(self, local_port, remote_port):
        self.__iproxy.forward(localport=local_port, remoteport=remote_port)

    def __remove_forward(self, local_port):
        self.__iproxy.removeForward(localport=local_port)

    '''
    input text to device
    param : str
    '''

    def text(self, content):
        self.__wda_connector.get_session().send_keys(content)

    '''
    get the current device display size
    return: two values  (width,height)
    '''

    def display_size(self):
        return self.__wda_connector.get_session().window_size()

    '''
    get the current device orientation
    return: enum DeviceOrientation value
    '''

    def orientation(self):
        orientation_map = {'PORTRAIT': DeviceOrientation.PORTRAIT,
                           'LANDSCAPE': DeviceOrientation.LANSCAPE,
                           'UIA_DEVICE_ORIENTATION_PORTRAIT_UPSIDEDOWN': DeviceOrientation.PORTRAIT_UPSIDEDOWN,
                           'UIA_DEVICE_ORIENTATION_LANDSCAPERIGHT': DeviceOrientation.LANDSCAPERIGHT}
        return orientation_map[self.__wda_connector.get_session().orientation]

    '''
    touch at the given position 
    param: x,y : pixel pos  or rate of the current device screen.
    '''

    def touch(self, x, y):
        if 0 < x < 1 and 0 < y < 1:
            display_size = self.display_size()
            x = x * display_size[0]
            y = y * display_size[1]
        logger.info("tap :" + str(x) + str(y))
        self.__wda_connector.get_session().tap(x, y)

    '''
    double touch at the given position 
    param: x,y : pixel pos  or rate of the current device screen.
    '''

    def double_touch(self, x, y):
        if 0 < x < 1 and 0 < y < 1:
            display_size = self.display_size()
            x = x * display_size[0]
            y = y * display_size[1]
        self.__wda_connector.get_session().double_tap(x, y)

    '''
    note:  the param "duration" indicates the touchdown and hold time rather than the moving time.
    param: sx,sy,dx,dy: start and end pixel pos  or rate of the current device screen.
           duration: start coordinate press duration in seconds
    '''

    def drag(self, sx, sy, dx, dy, duration=1):
        if 0 < sx < 1 and 0 < sy < 1 and 0 < dx < 1 and 0 < dy < 1:
            display_size = self.display_size()
            sx = sx * display_size[0]
            sy = sy * display_size[1]
            dx = dx * display_size[0]
            dy = dy * display_size[1]
        self.__wda_connector.get_session().swipe(sx, sy, dx, dy, duration)

    '''
    touch and hold for duration at the given position
    param : x,y : pixel pos  or rate of the current device screen.
            duration: holding seconds
    '''

    def long_press(self, x, y, duration=2):
        if 0 < x < 1 and 0 < y < 1:
            display_size = self.display_size()
            x *= display_size[0]
            y *= display_size[1]
        self.__wda_connector.get_session().tap_hold(x, y, duration)

    '''
    touch the center of the given rectangle bound.
    param: bound: a list as [s,y,width,height].
    '''

    def __touch_bound(self, bound):
        if 0 < bound[0] < 1 and 0 < bound[1] < 1 and 0 < bound[2] < 1 and 0 < bound[3] < 1:
            display_size = self.display_size()
            bound[0] *= display_size[0]
            bound[1] *= display_size[1]
            bound[2] *= display_size[0]
            bound[3] *= display_size[1]
        x, y = bound[0] + bound[2] / 2, bound[1] + bound[3] / 2
        self.touch(x, y)

    def __touch_hold_bound(self, bound, duration=2):
        if 0 < bound[0] < 1 and 0 < bound[1] < 1 and 0 < bound[2] < 1 and 0 < bound[3] < 1:
            display_size = self.display_size()
            bound[0] *= display_size[0]
            bound[1] *= display_size[1]
            bound[2] *= display_size[0]
            bound[3] *= display_size[1]
        x, y = bound[0] + bound[2] / 2, bound[1] + bound[3] / 2
        self.long_press(x, y, duration)
