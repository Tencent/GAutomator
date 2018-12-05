import random
import ga2

import time
import logging
import ga2_contrib

logger=logging.getLogger("iOSTestTutorial")

'''
local test steps:
1. start your webdriveragent test project on device 
2.iproxy xxxxx 8100 device_udid
3. start to edit and run your code 
'''

TEST_PKG_NAME = "com.tencent.qqchschess"

udid="cfc4572ed764c40b1913a1b03150566e22baad9b"

qqname="2952021417"
qqpwd="test9759"
wechatname="wxid_vylcfztoytih12"
wechatpwd="wetest657341"

# ## login\_tencent
# automatically login qq/wechat on device. iPad or login by webview are not supported for now.
# ### precondition
# 1. a device is inited (init_device is called)
# 2. the wechat/qq is installed on deivce
# 3. the current view is qq/wechat login view.
#
# ### input
# * account : the qq/wechat  account
# * password : the qq/wechat  password
#
# ### output
# returns ERR\_SUCCEED(0) if succeed

'''
a sample to login wechat/qq, 
if you want to use wda client to do automation on native app , the login_tencent module is a sample.
'''
def login_test():
    ga2_contrib.login_tencent(wechatname,wechatpwd)

#if you want to test specefic scene,  call connect_to_engine instead of launch

device = ga2.init_device(ga2.DeviceType.DEVICE_IOS,udid)#get the instance of device
ga2.launch_app(TEST_PKG_NAME)
ga2.init_engine_sdk(enginetype=ga2.EngineType.Unity, local_engine_port="42222")

#device.start_alert_handler()
time.sleep(3)
device.touch(0.5,0.75)
login_test()
time.sleep(1)
device.touch(0.5,0.75)
logger.info("iOSDevice_LoginTest end")

#device.iproxy.removeAllForwards()


