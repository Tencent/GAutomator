from ga2.automation.by import By
from ga2.common.constants import *
from ga2.common.logger_config import logger
from ga2.common.utils import callLog
from ga2.device.device import Device
from ga2.common.utils import *
from ga2.cloud.reporter import Reporter
from ga2.common.WebDriverWait import WebDriverWait

class AutomationHelper:

    def __init__(self, device=None):
        if device is None:
            device = Device.getDefaultDevice()
        self.device = device

    @callLog
    def wait_element(self, method, param,timeout):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "wait_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid find method :" + method)
            return None
        return method_map.get(method)(param, timeout)

    @callLog
    def touch_element(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "touch_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid touch method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def long_press_element(self, method, param, duration=2):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "long_press_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid touch method :" + method)
            return None
        return method_map.get(method)(param, duration)

    @callLog
    def double_touch_element(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "double_touch_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid touch method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def wait_engine_element_by_name(self, name, timeout):
        if self.device and self.device.engine_connector():
            element = None
            try:
                element = WebDriverWait(timeout,2).until(self.device.engine_connector().find_element,name)
            except Exception as e:
                logger.warn("element wait timeout:" + name)
            return element
        return None

    @callLog
    def touch_engine_element_by_name(self, name):
        if not self.device or not self.device.engine_connector():
            return None
        engine = self.device.engine_connector()
        element = engine.find_element(name)
        if element is None:
            logger.error("touch element is none in touch_engine_elem")
            return None
        bound = engine.get_element_bound(element)
        targetPos = (bound.x + bound.width / 2, bound.y + bound.height / 2)
        if isInCloudMode():
            (width, height) = self.device.display_size()
            Reporter().screenshot_with_mark(width, height,targetPos[0],targetPos[1])

        self.device.touch(targetPos[0],targetPos[1])

        return element

    @callLog
    def long_press_engine_element_by_name(self, name, duration=2):
        if not self.device or not self.device.engine_connector():
            return None
        engine = self.device.engine_connector()
        element = engine.find_element(name)
        if element is None:
            logger.error("long press element is none in long_press_engine_element_by_name")
            return None
        bound = engine.get_element_bound(element)
        targetPos = (bound.x + bound.width / 2, bound.y + bound.height / 2)
        if isInCloudMode():
            (width, height) = self.device.display_size()
            Reporter().screenshot_with_mark(width, height, targetPos[0], targetPos[1])
        self.device.long_press(targetPos[0], targetPos[1], duration)
        return element

    @callLog
    def double_touch_engine_element_by_name(self, name):
        if not self.device or not self.device.engine_connector():
            return None
        engine = self.device.engine_connector()
        element = engine.find_element(name)
        if element is None:
            logger.error("double touch  element is none in double_touch_engine_element_by_name")
            return None
        bound = engine.get_element_bound(element)
        targetPos = (bound.x + bound.width / 2, bound.y + bound.height / 2)
        if isInCloudMode():
            (width, height) = self.device.display_size()
            Reporter().screenshot_with_mark(width, height, targetPos[0], targetPos[1])

        self.device.double_touch(targetPos[0], targetPos[1])
        return element

        # @callLog
    # def login_tencent(self,account,password):
    #     if  self.login_helper:
    #         return self.login_helper.login_tencent(account=account,password=password)
    #     else:
    #         logger.error("login_helper is not inited...")
    #     return ERR_LOGIN_FAILED

