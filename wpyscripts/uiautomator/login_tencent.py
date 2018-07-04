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
            while None == re.search(account, user_edit.get_text(), re.IGNORECASE):
                # click the x point
                for i in range(0, local_range):
                    uiauto.wait.idle()
                    uiauto.click(local_x - i * local_step, local_y)
                    logger.info(
                        "click the usr x point. local_x is " + str(local_x - i * local_step) + ". local_y is " + str(
                            local_y))
                uiauto.wait.idle()
                user_edit.set_text(account)
                uiauto.wait.update()
                # user
                logger.info("src and dest content.")
                logger.info(user_edit.get_text())
                logger.info(account)
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
            pwd_edit.set_text(pwd)
            logger.info("set pwd : " + pwd)
            # login
            uiauto.wait.idle()
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
    try:
        if uiauto(text=u'登 录', className=u'android.widget.Button').exists and uiauto(text=u'新用户', className=u'android.widget.Button').exists and not uiauto(className=u'android.widget.EditText').exists:
            logger.info("pre login qq")
            uiauto.wait.idle()
            uiauto(text=u'登 录', className=u'android.widget.Button').click()
    except Exception, e:
            logger.info(e)

def _prelogin_wechat():
    try:
        if uiauto(text=u'登录', className=u'android.widget.Button').exists and uiauto(text=u'注册', className=u'android.widget.Button').exists and not uiauto(className=u'android.widget.EditText').exists:
            logger.info("pre login wechat")
            uiauto.wait.idle()
            uiauto(text=u'登录', className=u'android.widget.Button').click()
        if uiauto(text=u'用微信号/QQ号/邮箱登录', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'用微信号/QQ号/邮箱登录', className=u'android.widget.Button').click()

    except Exception, e:
        logger.info(e)


@time_snap(interval=5, times=12)
def login_tencent(account, pwd, timeout=120):
    start_time = time.time()
    end_time = start_time
    logger.info("login tencent...")

    while end_time - start_time < timeout:
        # 在密码框界面之前可能会有另一个跳转界面需要处理
        package_name = uiauto.info["currentPackageName"]
        if package_name == "com.tencent.mobileqq":
            _prelogin_qq()
        elif package_name == "com.tencent.mm":
            _prelogin_wechat()
        _login_edit_box(account, pwd)
        if package_name == "com.tencent.mobileqq":
            _login_qq()
        elif package_name == "com.tencent.mm":
            _login_wx()
        elif package_name is not None:
            logger.info("login success.")
            return True
        else:
            logger.info("get current pkg failed")
        end_time = time.time()
    return False

if __name__ == "__main__":
    #print get_login()
    login_tencent("2952020383", "wetesth")
