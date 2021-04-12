from ga2.automation.by import By
from ga2.common.constants import *
from ga2.common.logger_config import logger
from ga2.common.utils import callLog
from ga2.device.device import Device
from ga2.common.utils import *
from ga2.cloud.reporter import Reporter
from ga2.common.WebDriverWait import WebDriverWait
from config import Account


class AutomationHelper:

    def __init__(self, device=None):
        if device is None:
            device = Device.getDefaultDevice()
        self.device = device
        self.scale = 0
        self.UNscale = 0.0
        self.ue4_device = []

    @callLog
    def computetarget(self, param):
        '''
        坐标映射
        :param param:
        :return:
        '''
        engine = self.device.engine_connector()
        if self.device is None or engine is None:
            return None
        self.ue4_device = engine.get_device_info() if self.ue4_device == [] else self.ue4_device
        self.scale = max(self.device.screenshot_format().size) / max(
            self.device.display_size()) if self.scale == 0 else self.scale

        if self.UNscale == 0.0:
            size = self.device.screenshot_format().size
            self.UNscale = size[0] / self.ue4_device[0]['y']
        targetPos = (
            (param['x'] + param['width'] / 2) * self.UNscale / self.scale,
            (param['y'] + param['height'] / 2) * self.UNscale / self.scale)
        if isInCloudMode():
            Reporter().screenshot_with_mark(self.device.display_size()[0], self.device.display_size()[1], targetPos[0],
                                            targetPos[1])
        return targetPos

    @callLog
    def get_version(self, method, timeout):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "get_engine_version")}
        if method not in method_map:
            logger.error("invalid find method :" + method)
            return None
        return method_map.get(method)(timeout)

    @callLog
    def wait_element(self, method, param, timeout):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "wait_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid find method :" + method)
            return None
        return method_map.get(method)(param, timeout)

    @callLog
    def get_dumptree(self, method, timeout):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "wait_engine_dump_tree")}
        if method not in method_map:
            logger.error("invalid find method :" + method)
            return None
        return method_map.get(method)(timeout)

    @callLog
    def touch_element(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "touch_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid touch method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def swipe_screen(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "swipe_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid swipe method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def move_joystick(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "joystick_move")}
        if method not in method_map:
            logger.error("invalid move method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def swipe_hold_screen(self, method, param):
        '''
            Written by davidzkpu
        :param method: method name
        :param param:  dict
        :return:
        '''
        method_map = {By.NAME_IN_ENGINE: getattr(self, "swipe_hold")}
        if method not in method_map:
            logger.error("invalid hold method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def long_press_element(self, method, param, duration=2):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "long_press_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid long press method :" + method)
            return None
        return method_map.get(method)(param, duration)

    @callLog
    def double_touch_element(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "double_touch_engine_element_by_name")}
        if method not in method_map:
            logger.error("invalid double touch method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def get_element_text(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "get_element_engine_text_by_name")}
        if method not in method_map:
            logger.error("invalid get_txt method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def tencent_login(self, method):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "wait_engine_tencent_login")}
        if method not in method_map:
            logger.error("invalid loging method :" + method)
            return None
        return method_map.get(method)()

    @callLog
    def screen_shot(self, method, param):
        '''

        '''
        method_map = {By.NAME_IN_ENGINE: getattr(self, "screen_engine_shot")}
        if method not in method_map:
            logger.error("invalid screenshot method :" + method)
            return None
        return method_map.get(method)(param)

    @callLog
    def multifingers_swip(self, method, param):
        method_map = {By.NAME_IN_ENGINE: getattr(self, "multi_fingers_control")}
        if method not in method_map:
            logger.error("invalid screenshot method :" + method)
            return None
        return method_map.get(method)(param)

    ##################################################################

    @callLog
    def get_engine_version(self, timeout):
        if self.device and self.device.engine_connector():
            element = None
            try:
                element = WebDriverWait(timeout, 2).until(self.device.engine_connector().get_sdk_version)
            except Exception as e:
                logger.warn("get engine version timeout")
            return element
        return None

    @callLog
    def wait_engine_element_by_name(self, name, timeout):
        if self.device and self.device.engine_connector():
            element = None
            try:
                element = WebDriverWait(timeout, 2).until(self.device.engine_connector().find_element, name)
            except Exception as e:
                logger.warn("element wait timeout:" + name)
            return element
        return None

    @callLog
    def wait_engine_dump_tree(self, timeout):
        if self.device and self.device.engine_connector():
            element = None
            try:
                element = WebDriverWait(timeout, 2).until(self.device.engine_connector()._get_dump_tree)
            except Exception as e:
                logger.warn("getdumptree timeout")
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
        bound = engine._get_elements_UE4_bound([element])
        targetPos = self.computetarget(bound[0])
        self.device.touch(targetPos[0], targetPos[1])

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

    @callLog
    def swipe_engine_element_by_name(self, param):
        if not self.device or not self.device.engine_connector():
            return None
        engine = self.device.engine_connector()
        self.device.drag(param['fx'], param['fy'], param['tx'], param['ty'], param['duration'])

    @callLog
    def swipe_hold(self, param):
        '''
        written by davidzkpu
        :param param: dict
        :return:
        '''
        if not self.device or not self.device.engine_connector():
            return None
        engine = self.device.engine_connector()
        self.device.drag_hold(param['fx'], param['fy'], param['tx'], param['ty'], param['dragduration'],
                              param['holdduration'], param['velocity'])

    @callLog
    def joystick_move(self, param):
        '''
        swipe joystick

        :param dict
        :param distance: the distance for joystick swipe
        :param stickname: jotstick_name
        :param duration: hold name
        :param velocity: swip speed
        :param style: value=left,right,up,down
        :return:
        '''

        if not self.device or not self.device.engine_connector():
            return None
        engine = self.device.engine_connector()
        element = engine.find_element(param['stickname'])
        if element is None:
            logger.error("long press element is none in long_press_engine_element_by_name")
            return None
        ret = engine.get_element_bound(element)
        if not ret:
            return False
        targetpos = self.computetarget(ret)
        switch = {'left': lambda x: [x[0] - param['distance'], x[1]],
                  'right': lambda x: [x[0] + param['distance'], x[1]],
                  'up': lambda x: [x[0], x[1] - param['distance']],
                  'down': lambda x: [x[0], x[1] + param['distance']]
                  }

        topos = switch.get(param['style'], lambda: False)(targetpos)
        self.device.drag_hold(targetpos[0], targetpos[1], topos[0], topos[1], 1, param['duration'], param['velocity'])
        return

    @callLog
    def get_element_engine_text_by_name(self, name):
        if not self.device or not self.device.engine_connector():
            return None
        engine = self.device.engine_connector()
        element = engine.find_element(name)

        if element is None:
            logger.error("touch element is none in touch_engine_elem")
            return None
        res = engine.get_element_text(element)

        return res

    @callLog
    def wait_engine_tencent_login(self):
        '''

        :param name:
        :return:
        '''
        if self.device and self.device.engine_connector():
            self.device.wda_session().tap(200, 200)
            time.sleep(1)
            while True:
                if self.device.wda_session()(className='Button', name=u'好').exists:
                    self.device.wda_session()(className='Button', name=u'好').tap()
                    time.sleep(1)
                    continue
                if self.device.wda_session()(className='Button', name=u'允许').exists:
                    self.device.wda_session()(className='Button', name=u'允许').tap()
                    time.sleep(1)
                    continue
                if self.device.wda_session()(className='StaticText', name=u'同意').exists:
                    self.device.wda_session()(className='StaticText', name=u'同意').tap()
                    time.sleep(1)
                break

            time.sleep(1)
            if self.device.wda_session()(name=u'允许').exists:
                self.device.wda_session()(cname=u'允许').tap()

            time.sleep(1)
            if self.device.wda_session()(name=u'同意').exists:
                self.device.wda_session()(name=u'同意').tap()

            time.sleep(1)
            if self.device.wda_session()(className='TextField', name=u'帐号').exists:
                self.device.wda_session()(className='TextField', name=u'帐号').set_text(Account.QQNAME)

            time.sleep(1)
            if self.device.wda_session()(className='SecureTextField', name=u'密码').exists:
                self.device.wda_session()(className='SecureTextField', name=u'密码').set_text(Account.QQPWD)

            time.sleep(1)
            if self.device.wda_session()(className='Button', name=u'登录按钮').exists:
                self.device.wda_session()(className='Button', name=u'登录按钮').tap()

            time.sleep(2)
            if self.device.wda_session()(className='StaticText', value=u'确定').exists:
                self.device.wda_session()(className='StaticText', value=u'确定').tap()

            time.sleep(1)
            if self.device.wda_session()(className='Button', name=u'QQ授权登录').exists:
                self.device.wda_session()(className='Button', name=u'QQ授权登录').tap()

            time.sleep(1)
            if self.device.wda_session()(className='Button', name=u'完成QQ授权').exists:
                self.device.wda_session()(className='Button', name=u'完成QQ授权').tap()

    @callLog
    def screen_engine_shot(self, param):
        '''

        '''
        if not self.device or not self.device.engine_connector():
            return None
        self.device.screenshot(param)
        return

    @callLog
    def multi_fingers_control(self, param):
        '''
        多指控制
        Args:
            param:array[dict(x1,y1,x2,y2,dur)......]
            每个dict代表一个手指的滑动操作，多指通过多个dict表示
            x1,y1为按压初始坐标，x2,y2为滑动终止坐标，dur为滑动时长（ms）
        Returns:
        '''
        wda = self.device.wda_session()
        actions = []
        for item in param:
            action = []
            action.append(wda.actionmember(action='press', x=item['x1'], y=item['y1']))
            action.append(wda.actionmember(action='wait', ms=item['dur']))
            action.append(wda.actionmember(action='moveTo', x=item['x2'], y=item['y2']))
            actions.append(action)
        wda.perform(actions)
