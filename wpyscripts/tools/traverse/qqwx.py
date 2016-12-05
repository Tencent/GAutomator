"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

__author__ = 'yifengcai'

import time

import wpyscripts.manager as manager
import wpyscripts.uiautomator.uiautomator_manager as m

uiauto = m.get_uiautomator()

logger = manager.get_logger()
device = manager.get_device()


QQ_PACKAGE_NAME = "com.tencent.mobileqq"
WX_PACKAGE_NAME = "com.tencent.mm"


def check_qq_wx_package():
    top_package = uiauto.info["currentPackageName"]
    logger.debug("top package is %s", top_package)
    
    if top_package == QQ_PACKAGE_NAME or top_package == WX_PACKAGE_NAME:
        return True
    else:
        return False


def handle_qq_wx_package():
    top_package = uiauto.info["currentPackageName"]
    logger.info("current in qq/wx package: %s, try to login first", top_package)
    
    ret = device.login_qq_wechat_wait(120)
    if ret:
        # login successfully, and current not in qq/wx package
        return
    
    # still in qq/wx package, try to push back
    # logger.info("still in qq/wx package, push 'back'")
    # device.back()
    # time.sleep(3)
    if not check_qq_wx_package():
        return
    
    # still in qq/wx package, do custom actions
    logger.info("still in qq/wx package, do custom actions")
    qq_wx_custom_actions(top_package)
    
    
def qq_wx_custom_actions(top_package):
    pass
        
        
    


