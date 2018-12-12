#-*-coding:utf-8-*-
import logging
import re
import threading

from ga2.common.rpc_thread import RPCReceiveThread
from ga2.common.socket_client import SocketClient
from ga2.common.wetest_exceptions import *
from ga2.device.android.adb_process import AdbTool
from ga2.engine.element import Element
from ga2.engine.protocol import Commands, TouchEvent

logger = logging.getLogger("wetest")


from enum import Enum
class EngineType(Enum):
    Unity=0,
    UE4=1

class VersionInfo(object):
    """
    Attributes:
        engine_version:引擎版本信息,如5.1.0bf
        engine:Unity
        sdk_version:wetest sdk的版本信息
    """

    def __init__(self, engine_version, engine, sdk_version, ui_type):
        self.engine_version = engine_version
        self.engine = engine
        self.sdk_version = sdk_version
        self.ui_type = ui_type

    def __str__(self):
        return "Engine = {0} {1},WeTest SDK = {2},UI={3}".format(self.engine, self.engine_version, self.sdk_version,
                                                                 self.ui_type)


class ElementBound(object):
    """
    Attributes:
        Element在屏幕上显示的位置和大小，(x,y)为中心点坐标系以屏幕左上角为坐标原点
        __________ x
        |
        |
        |
        y
        x:element与屏幕左侧的距离
        y:element与屏幕上边的距离
        width:element的宽
        height:element的高
        visible:是否可视化，在3D物体中
    """

    def __init__(self, x, y, width, height, visible=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible

    def __str__(self):
        return "  point = ({0},{1}) width = {2}  height = {3},visible={4}".format(self.x, self.y, self.width,
                                                                                  self.height, self.visible)

    def __repr__(self):
        return self.__str__()

    def __nonzero__(self):
        return self.visible


class WorldBound(object):
    """
        represents an axis aligned bounding box.
    """

    def __init__(self, _id, _existed):
        self.id = _id
        self.existed = _existed

        # center_x,center_y,center_z,the center of the bounding box
        self.center_x = 0
        self.center_y = 0
        self.center_z = 0

        # the extents of the box,
        self.extents_x = 0
        self.extents_y = 0
        self.extents_z = 0

    def __str__(self):
        return "center = ({0},{1},{2}) extents = ({3},{4},{5})".format(self.center_x, self.center_y, self.center_z,
                                                                       self.extents_x, self.extents_y, self.extents_z)


class GameEngine(object):
    """
        Only support Unity engine at this time
    """

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sdk_version = None
        self.socket = SocketClient(self.address, self.port)

    def get_sdk_version(self):
        """ 获取引擎集成的SDK的版本信息

        获取SDK的版本信息，GameSDKVersionInfo
        :return:
            返回的信息包括引擎版本，引擎和SDK版本信息,class:VersionInfo
            example:
                {‘engine_version’：‘5.1.0bf’，
                ‘engine’：‘Unity’,
                'sdk_version':10}
        :rtype: VersionInfo
        :raise:
            WeTestRuntimeError
        """
        ret = self.socket.send_command(Commands.GET_VERSION )
        engine = ret.get("engine", None)
        sdk_version = ret.get("sdkVersion", None)
        engine_version = ret.get("engineVersion", None)
        ui_type = ret.get("sdkUIType", None)
        version = VersionInfo(engine_version, engine, sdk_version, ui_type)
        return version

    def jump_building(self, name):
        """
            通过jump_building跳转到对应building
        :param name:
            jump_building的参数
        :Usage:
            >>>import wpyscripts.manager as manager
            >>>engine=manager.get_engine()
            >>>button=engine.jump_building()
        :return:
            status:0
        :rtype: Element
        :raise:
        """
        ret = self.socket.send_command(Commands.JUMP_BUILDING, name)
        if ret:
            return 0
        else:
            return None
    #
    # def input_text_set(self, element, text):
    #     """
    #             设置坐标
    #             :param :element,text
    #
    #             :Usage:
    #                 >>>import wpyscripts.manager as manager
    #                 >>>engine=manager.get_engine()
    #                 >>>text=engine.input_text_set(element,text)
    #             :return:成功与否
    #             """
    #     ret = self.socket.send_command(Commands.SET_INPUT_TEXT_VC, {"element": element, "text": text})
    #     if ret:
    #         return ret
    #     else:
    #         return None

    def find_element(self, name):
        """
            通过GameObject.Find查找对应的GameObject
        :param name:
            GameObject.Find的参数
        :Usage:
            >>>engine=GameEngine("127.0.0.1",12345)
            >>>button=engine.find_element('/Canvas/Panel/Button')
        :return:
            a instance of Element if find the GameObject,else return  None
            example:
            {"object_name":"/Canvas/Panel/Button",
            "instance":4257741}
        :rtype: Element
        :raise:
        """
        ret = self.socket.send_command(Commands.FIND_ELEMENTS, [name])
        if ret:
            ret = ret[0]
            if ret["instance"] == -1:
                return None
            else:
                return Element(ret["name"], ret["instance"])
        else:
            return None

    def _get_dump_tree(self):
        """
        获取dump tree
        :return: xml string
        """
        ret = self.socket.send_command(Commands.DUMP_TREE)
        return ret

    def get_scene(self):
        """
            获取当前界面的scene名称
        :Usage:
            >>>import wpyscripts.manager as manager
            >>>engine=manager.get_engine()
            >>>current_scene=engine.get_scene()
        :return:当前scene的名称
        :raise: WeTestRuntimeError
        """
        ret = self.socket.send_command(Commands.GET_CURRENT_SCENE)
        return ret

    # def click(self, locator):
    #     """
    #         点击一个button, checkbox or radio button.
    #         'locator' is an Element locator or ElementBound
    #         如果是一个Element会先去查找Element的位置，然后点击中心点
    #         如果是一个ElementBound则会直接点击，x,y的位置
    #     :param locator:
    #         点击的节点为，节点位置
    #     :Usage:
    #         >>>import wpyscripts.manager as manager
    #         >>>engine=manager.get_engine()
    #         >>>element=engine.find_element('/Canvas/Panel/Button')
    #         >>>bound=engine.get_element_bound(element)
    #         >>>engine.click(bound)
    #
    #         >>>element=engine.find_element('/Canvas/Panel/Button2')
    #         >>>engine.click(element)
    #     :raise WeTestInvaildArg,WeTestRuntimeError
    #     """
    #     if locator is None:
    #         return
    #     if isinstance(locator, Element):
    #         try:
    #             bound = self.get_element_bound(locator)
    #             if bound:
    #                 return self.click_position(bound.x + bound.width / 2, bound.y + bound.height / 2)
    #         except WeTestRuntimeError as e:
    #             logger.error("Get element({0}) bound faild {1}".format(locator, e.message))
    #         return False
    #     elif isinstance(locator, ElementBound) and locator:
    #         try:
    #             return self.click_position(locator.x + locator.width / 2, locator.y + locator.height / 2)
    #         except WeTestRuntimeError:
    #             logger.error("Get element({0}) bound faild".format(locator))
    #         return False
    #     else:
    #         reason = "Click locator = {0},vaild argument is Element or ElementBound".format(locator)
    #         raise WeTestInvaildArg(reason)

    # def press(self, locator, press_time):
    #     """
    #         长按动作
    #     :param locator:is an element locator
    #     :param press_time:按压时间，单位为毫秒
    #
    #     :Usage:
    #         >>>import wpyscripts.manager as manager
    #         >>>engine=manager.get_engine()
    #         >>>element=engine.find_element('/Canvas/Panel/Button')
    #         >>>bound=engine.get_element_bound(element)
    #         >>>engine.press(bound,1000)
    #
    #         >>>element=engine.find_element('/Canvas/Panel/Button2')
    #         >>>engine.press(element,5000)
    #     :raises WeTestInvaildArg,WeTestRuntimeError
    #     """
    #
    #     if locator is None:
    #         return
    #     if isinstance(locator, Element):
    #         try:
    #             bound = self.get_element_bound(locator)
    #             return self.press_position(bound.x + bound.width / 2, bound.y + bound.height / 2, press_time)
    #         except WeTestRuntimeError:
    #             logger.error("Get element({0}) bound faild".format(locator))
    #         return False
    #     elif isinstance(locator, ElementBound):
    #         try:
    #             return self.press_position(locator.x + locator.width / 2, locator.y + locator.height / 2, press_time)
    #         except WeTestRuntimeError:
    #             logger.error("Get element({0}) bound faild".format(locator))
    #         return False
    #     else:
    #         reason = "Press locator = {0},vaild argument is Element or ElementBound".format(locator)
    #         raise WeTestInvaildArg(reason)
    #
