# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
import time
import logging
import re
import traceback
import uiautomator_manager as m
import login_getter as getter
import os
from wpyscripts.common.adb_process import *
from wpyscripts.common.utils import time_snap

logger = logging.getLogger("wetest")
uiauto = m.get_uiautomator()

def __click_by_step__(obj, step, number):
    if obj.exists:
        info = obj.info
        local_x = (info['bounds']['left'] + info['bounds']['right']) / 2
        local_y = info['bounds']['bottom']
        for y in range(local_y, local_y + step * number, step):
            uiauto.click(local_x, y)
        return

def _login_edit_box(account, pwd):
    logger.info("login edit box...")
    logins = getter.get_login()
    logger.info("after get login...")
    if logins and len(logins) > 0:
        try:
            local_step = 10
            local_range = 20
            local_x = uiauto.info['displayWidth']
            user_edit = logins[0]
            info = user_edit.info
            local_y = (info['bounds']['top'] + info['bounds']['bottom']) / 2
            user_edit.clear_text()
            user_tmp = user_edit.get_text()
            if len(user_tmp) > 0 and "QQ" not in user_tmp and u"用户名" not in user_tmp and u"手机号" not in user_tmp and "/" not in user_tmp:
                # click the x point
                for i in range(0, local_range):
                    package_name = get_current_pkgname()
                    if package_name != None and package_name != "com.tencent.mm" and package_name != "com.tencent.mobileqq":
                        logger.info("break login_edit_box because package not in tencent...  " + package_name)
                        return
                    uiauto.click(local_x - i * local_step, local_y)
                    logger.info(
                        "click the usr x point. local_x is " + str(local_x - i * local_step) + ". local_y is " + str(
                            local_y))
             #  uiauto.wait.idle()
                # user_edit.set_text(account)
            excute_adb_process("shell input text " + account)
            logger.info("accont:" + account)

            #   uiauto.wait.update()
              # logger.info("src and dest content.")
              # logger.info(user_edit.get_text())
            # pwd
            pwd_edit = logins[1]
            info = pwd_edit.info
            local_y = (info['bounds']['top'] + info['bounds']['bottom']) / 2
            for j in range(0, local_range):
                uiauto.click(local_x - j * local_step, local_y)
                logger.info(
                    "click the pwd x point. local_x is " + str(local_x - j * local_step) + ". local_y is " + str(
                        local_y))
            uiauto.wait.idle()
            excute_adb_process("shell input text " + pwd)
           # pwd_edit.set_text(pwd)
            logger.info("set pwd : " + pwd)
            time.sleep(1)
            login_button = logins[2]
            login_button.click.wait()
            logger.info("login_button.click()")
            return 1
        except Exception as e:
            logger.info(e)
            stack = traceback.format_exc()
            logger.error(stack)
    else:
        logger.error("Can not get username/password elements")
        return -1
    return 0

def _afterlogin():
    time.sleep(2)
    if uiauto(text=u'开启消息推送', className=u'android.widget.TextView').exists:
        height = uiauto.info["displayHeight"]
        width = uiauto.info["displayWidth"]
        x = width / 2
        for y in range(int(height * 4 / 5),int( height * 1 / 5), int(-1 * height / 50)):
            if uiauto(text=u'开启消息推送', className=u'android.widget.TextView').exists:
                uiauto.wait.idle()
                uiauto.click(x, y)
                logger.info(str(x) + ", " + str(y))
                x = width / 10
                y = height / 10
                uiauto.wait.idle()
                uiauto.click(x, y)
                logger.info(str(x) + ", " + str(y))
    if uiauto(text=u'马上绑定',className=u'android.widget.Button').exists:
        logger.info("处理马上绑定页面 ..")
        if uiauto(text=u'关闭', className=u'android.widget.TextView').exists:
            uiauto(text=u'关闭', className=u'android.widget.TextView').click()
        elif uiauto(resourceId=u'com.tencent.mobileqq:id/ivTitleBtnLeft', className=u'android.widget.TextView').exists:
            uiauto(resourceId=u'com.tencent.mobileqq:id/ivTitleBtnLeft', className=u'android.widget.TextView').click()
        else:
            logger.info("处理马上绑定页面失败")


def _login_qq():
    # qq
    try:
        if uiauto(text=u'登录失败', className=u'android.widget.TextView').exists and uiauto(text=u'确定',
                                                                                        className=u'android.widget.TextView').exists:
            btn = uiauto(text=u'确定', className=u'android.widget.TextView')
            if uiauto(text=u'请输入帐号(错误码: 3103)', className=u'android.widget.TextView').exists:
                __click_by_step__(btn, 20, 15)
                pass
            elif uiauto(text=u'请输入密码(错误码: 3104)', className=u'android.widget.TextView').exists:
                __click_by_step__(btn, 20, 15)
            else:
                uiauto.wait.idle()
                btn.click()
            logger.info("this. 登录失败")

        elif uiauto(text=u'QQ登录').exists \
                and uiauto(text=u'重新拉取授权信息', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'重新拉取授权信息', className=u'android.widget.Button').click()
            logger.info("this.QQ登录")

        elif uiauto(text=u'QQ登录').exists \
                and uiauto(text=u'授权并登录', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'授权并登录', className=u'android.widget.Button').click()
            logger.info("this. 授权并登录")

        elif uiauto(text=u'QQ登录').exists \
                and uiauto(text=u'登录', className='android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'登录', className='android.widget.Button').click()
            logger.info("this. QQ登录")

        elif uiauto(text=u'输入验证码').exists \
                and uiauto(className=u'android.widget.EditText').exists \
                and uiauto(text=u'取消').exists:
            uiauto.wait.idle()
            uiauto(text=u'取消').click()
            logger.info("this. 输入验证码")

    except Exception as e:
        logger.info(e)

def _login_wx():
    time.sleep(10)
    try:
        if uiauto(className=u'com.tencent.smtt.webkit.WebView').exists or uiauto(
                className=u'android.webkit.WebView').exists \
                or uiauto(className=u'android.view.View'):
            height = uiauto.info["displayHeight"]
            width = uiauto.info["displayWidth"]
            x = width / 2
            if uiauto(text=u'微信登录').exists:
                logger.info("微信登录 found")
                for y in range(height * 4 / 5, height * 1 / 5, -1 * height / 50):
                    uiauto.wait.idle()
                    uiauto.click(x, y)
                    logger.info(str(x) + ", " + str(y))
        elif uiauto(text=u'微信登录', className=u'android.widget.TextView').exists \
                and 1 == uiauto(className=u'android.widget.Button').count \
                and 1 == uiauto(className=u'android.widget.Image').count \
                and 0 == uiauto(className=u'android.widget.EditText').count:
            logger.info("微信登录 found...")
            uiauto.wait.idle()
            uiauto(className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'通讯录', className=u'android.widget.TextView').exists \
                and uiauto(text=u'发现', className=u'android.widget.TextView').exists:
            uiauto.wait.idle()
            uiauto.press.back()
            logger.info("press back.")

        elif uiauto(text=u'帐号或密码错误，请重新填写。', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'抱歉，出错了', className=u'android.widget.TextView').exists \
                and uiauto(className=u'com.tencent.smtt.webkit.WebView').exists \
                and uiauto(description=u'返回').exists:
            uiauto.wait.idle()
            uiauto(description=u'返回').click()
            logger.info("this.")

        elif uiauto(text=u'该用户不存在', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'你操作频率过快，请稍后重试', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'填写验证码', className=u'android.widget.TextView').exists \
                and uiauto(text=u'继续', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto.press.back()
            logger.info("this.")

        elif uiauto(textStartsWith=u'当前帐号的使用存在异常', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(textStartsWith=u'你登录的微信需要进行好友验证', className=u'android.widget.TextView').exists \
                and uiauto(text=u'取消', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'取消', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(textStartsWith=u'微信帐号不能为空', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")
        elif uiauto(textStartsWith=u'确认登录', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确认登录', className=u'android.widget.Button').click()
            logger.info("click 确认登录")
    except Exception as e:
        logger.info(e)

def _prelogin_qq():
    logger.info("tryp to prelogin qq")
    try:
        if uiauto(textMatches=u'登(\\s)?录', className=u'android.widget.Button').exists and uiauto(text=u'新用户', className=u'android.widget.Button').exists and not uiauto(className=u'android.widget.EditText').exists:
            logger.info("pre login qq")
            uiauto.wait.idle()
            uiauto(textMatches=u'登(\\s)?录', className=u'android.widget.Button').click()
    except Exception as e:
            logger.exception(e)

def _prelogin_wechat():
    logger.info("tryp to prelogin wechat")
    try:
        if uiauto(text=u'登录', className=u'android.widget.Button').exists and uiauto(text=u'注册', className=u'android.widget.Button').exists and not uiauto(className=u'android.widget.EditText').exists:
            logger.info("pre login wechat")
            uiauto.wait.idle()
            uiauto(text=u'登录', className=u'android.widget.Button').click()
        if uiauto(text=u'用微信号/QQ号/邮箱登录', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'用微信号/QQ号/邮箱登录', className=u'android.widget.Button').click()

    except Exception as e:
        logger.info(e)

@retry_if_fail()
def get_current_pkgname():
    package_name = None
    def reconnectUiautomator():
        if os.environ.get("UIAUTOMATORPORT") is None:
            logger.info("uiautomator get currentPackageName failed...restart uiautomator")
            m.init_uiautomator()
        else:
            logger.info("uiautomator get currentPackageName failed...sleep to wait platform reconnecting")
            time.sleep(10)  # m.restartPlatformDialogHandler()
    try:
        package_name = uiauto.info["currentPackageName"]
        if package_name is None:
            reconnectUiautomator()
    except Exception as e:
        reconnectUiautomator()
        try:
            package_name = uiauto.info["currentPackageName"]
        except Exception as e:
            logger.exception(e)
    if package_name:
        logger.info("packagename : "  + package_name)
    return package_name


@time_snap(interval=9, times=19)
def login_tencent(account, pwd, timeout=180):
    start_time = time.time()
    end_time = start_time
    logger.info("login tencent...")

    while end_time - start_time < timeout:
        # 在密码框界面之前可能会有另一个跳转界面需要处理
        package_name = get_current_pkgname()

        if package_name == "com.tencent.mobileqq":
            _prelogin_qq()
        elif package_name == "com.tencent.mm":
            _prelogin_wechat()
        _login_edit_box(account, pwd)
        if package_name == "com.tencent.mobileqq":
            _login_qq()
            _afterlogin()
        elif package_name == "com.tencent.mm":
            _login_wx()
        elif package_name is not None and time.time()-start_time>15 :
            logger.info("login success. package: "+package_name)
            return True
        else:
            logger.info("get current pkg failed")
        end_time = time.time()
    return False

if __name__ == "__main__":
    #print get_login()
    login_tencent("2952018575", "1234")
