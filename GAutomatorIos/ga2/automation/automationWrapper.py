from ga2.automation.automationHelper import AutomationHelper

from ga2.device.iOS.iOSDevice import *


def init_device(type,serial):
    if type==DeviceType.DEVICE_IOS:
        if isInCloudMode():
            serial = os.environ.get("IOS_SERIAL",serial)
        device=IOSDevice(serial)
        if device is not None:
            Device.setDefault(device)
        return device
    else:
        logger.error("devicetype is not supported for now : "+str(type))
        return None

def launch_app(appid,timeout=60):
    if Device.getDefaultDevice() is  None:
        logger.error(" you must init a device before launch app")
        return ERR_DEVICE_NOT_INITED
    return Device.getDefaultDevice().launch(appid, timeout)


def init_engine_sdk(enginetype=None,local_engine_port=None,timeout=60):
    if Device.getDefaultDevice() is  None:
        logger.error(" you must init a device before init_engine_sdk")
        return ERR_DEVICE_NOT_INITED
    return Device.getDefaultDevice().init_engine_sdk(enginetype,local_engine_port,timeout)


def touch_element(method,param):
    return AutomationHelper().touch_element(method,param)


def wait_element(method,param,timeout=10):
    return AutomationHelper().wait_element(method,param,timeout)


def double_touch_element(method,param):
    return AutomationHelper().double_touch_element(method,param)


def long_press_element(method,param,duration=2):
    return AutomationHelper().long_press_element(method,param,duration)
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
