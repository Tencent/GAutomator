from ga2.automation.automationHelper import AutomationHelper

from ga2.device.iOS.iOSDevice import *


def init_device(type, serial):
    if type == DeviceType.DEVICE_IOS:
        if isInCloudMode():
            serial = os.environ.get("IOS_SERIAL", serial)
        device = IOSDevice(serial)
        if device is not None:
            Device.setDefault(device)
        return device
    else:
        logger.error("devicetype is not supported for now : " + str(type))
        return None


def launch_app(appid, timeout=60):
    if Device.getDefaultDevice() is None:
        logger.error(" you must init a device before launch app")
        return ERR_DEVICE_NOT_INITED
    return Device.getDefaultDevice().launch(appid, timeout)


def init_engine_sdk(enginetype=None, local_engine_port=None, timeout=60):
    if Device.getDefaultDevice() is None:
        logger.error(" you must init a device before init_engine_sdk")
        return ERR_DEVICE_NOT_INITED
    return Device.getDefaultDevice().init_engine_sdk(enginetype, local_engine_port, timeout)


def touch_element(method, param):
    return AutomationHelper().touch_element(method, param)

def move_joystick(method, param):
    '''
    根据摇杆名称上下左右定向移动
    Written by david
    move the joystick to controll the pawn
    :param method:
    :param param: dict
    :return:
    '''
    return AutomationHelper().move_joystick(method, param)

# def touch_xy(method,x,y):
#     return AutomationHelper().touch_xy(method, x, y)

def swip_screen(method, param):
    '''
    滑动操作
    :param method:
    :param param: dict(fx=,fy,tx=,ty=,dragduration=)
    :return:
    '''
    return AutomationHelper().swipe_screen(method, param)

def swip_hold(method, param):
    '''
    滑动操作2.0
    Written by davidzkpu
    :param method:
    :param param:  dict(fx=,fy,tx=,ty=,dragduration=,holdduration=,velocity=)
                from coordinate(fx,fy) for dragduration time to coordinate (tx,ty) for holdduration time in velocity speedc
    :return:
    '''
    return AutomationHelper().swipe_hold_screen(method, param)

def wait_element(method, param, timeout=10):
    '''
    根据控件名称获取控件大小
    :param method:
    :param param:
    :param timeout:
    :return:
    '''
    return AutomationHelper().wait_element(method, param, timeout)

def get_dumptree(method,timeout=10):
    '''
    获取控件元素
    :param method:
    :param timeout:
    :return:
    '''
    return AutomationHelper().get_dumptree(method, timeout)


def double_touch_element(method, param):
    '''
    根据控件名称双击
    :param method:
    :param param: elementname
    :return:
    '''
    return AutomationHelper().double_touch_element(method, param)


def long_press_element(method, param, duration=2):
    '''
    根据控件名称长按
    :param method:
    :param param: elementname
    :param duration: 长按时长
    :return:
    '''
    return AutomationHelper().long_press_element(method, param, duration)

def get_text(method, param):
    '''
    根据控件名称获取其内容
    :param method:
    :param param:
    :return:
    '''
    return AutomationHelper().get_element_text(method, param)

def tencent_login(method):
    '''
    QQ login
    :param method:
    :return:
    '''
    return AutomationHelper().tencent_login(method)

def screen_shot(method, param):
    '''
    截图
    :param method:
    :param param: 本地路径
    :return:
    '''
    return AutomationHelper().screen_shot(method, param)

def multi_fingers_swipe(method, params):
    '''
    多指滑动操作
    :param method:
    :param params: param:array[dict(x1,y1,x2,y2,dur)......]
            每个dict代表一个手指的滑动操作，多指通过多个dict表示
            x1,y1为按压初始坐标，x2,y2为滑动终止坐标，dur为滑动时长（ms）
    :return:
    '''
    return AutomationHelper().multifingers_swip(method, params)

#
# '''
# find the center of  engine element on device specified by its name in the engine
# return the element found , otherwise return None
# '''
# def find_by_engine_name(name):
#     return AutomationHelper().find_engine_element_by_name(name)
#
# '''
# touch the center of  engine element on device specified by its name in the engine
# return the element found , otherwise return None
# '''
# def touch_by_engine_name(name):
#     return AutomationHelper().touch_engine_element_by_name(name)
#
# '''
# touch and hold the center of  engine element on device specified by its name in the engine
# return the element found , otherwise return None
# '''
# def touch_hold_by_engine_name(name,duration=2):
#     return AutomationHelper().touch_hold_engine_element_by_name(name,duration)
