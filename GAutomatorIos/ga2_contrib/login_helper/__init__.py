import ga2
from ga2 import Device
from ga2_contrib.login_helper.login_tencent import TencentLoginHelper

'''
try to login qq and wechat
precondition: wechat and qq are installed on your device and the current view belongs to wechat or qq .
return True if successfully login, otherwise return False or None
'''
def login_tencent(account,pwd):
    device = Device.getDefaultDevice()
    if device is None:
        return ga2.ERR_DEVICE_NOT_INITED
    login_helper = TencentLoginHelper(device)
    return login_helper.login_tencent(account,pwd)


