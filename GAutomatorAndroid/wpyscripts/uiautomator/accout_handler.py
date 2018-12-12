# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import traceback
import logging

from wpyscripts.uiautomator.uiautomator_manager import *
from wpyscripts.common.wetest_exceptions import *
from wpyscripts.uiautomator.login_getter import *

logger = logging.getLogger("wetest")


class AccountHandler(object):
    def __init__(self, device):
        self.device = device

    def __set_txt_complete(self, uiobject, content, max_try=5):
        """
            在很多情况下，clearTextField 这个函数是无效的。因此采用，一个字一个字删除的方式
        :param uiobject:
        :param content:
        :return:
        """
        txt = uiobject.get_text()
        if txt == content:
            return True
        for i in range(max_try):
            uiobject.click("bottomright")
            for num in range(len(txt) + 3):
                device.press("delete")
            uiobject.set_text(content)
            txt = uiobject.get_text()
            if txt == content:
                return True
        return False

    def __set_password_complete(self, uiobject, content):
        """
            在很多情况下，clearTextField 这个函数是无效的。因此采用，一个字一个字删除的方式
        :param uiobject:
        :param content:
        :return:
        """
        uiobject.click("bottomright")
        for num in range(len(content) + 3):
            device.press("delete")
        uiobject.set_text(content)

    def _set_txt(self, content, uiobject, password=False):
        """
            设置文字内容
        :param resources_id:
        :param content:
        :return:
        """
        if uiobject == None or not uiobject.exists:
            raise UIAutomatorLoginError("Setting text UIObject not exists")

        rotation = self.device.orientation
        if password:
            self.__set_password_complete(uiobject, content)
        else:
            self.__set_txt_complete(uiobject, content)
        if rotation in ("left", "right"):
            # 横屏，通常会将内容输入框全全屏话。输入文字内容后，需要按回退键
            self.device.press("back")

    def click_button(self, button):
        if not button.exists:
            error_info = "Button not exist"
            raise UIAutomatorLoginError(error_info)
        button.click.wait()
        logger.debug("over")

    def _do_watcher(self):
        """
            处理一切弹出框
        :return:
        """
        buttons = self.device(className=u'android.widget.Button')
        for b in buttons:
            if b.exists:
                b.click()

        buttons = self.device(className=u'android.widget.TextView', clickable=True)
        for b in buttons:
            if b.exists:
                b.click()

        return True

    def _try_login(self, account, password, packageName):
        package = self.device.info["currentPackageName"]
        if package != packageName:
            return True
        loggin_elements = is_login()
        for e in loggin_elements:
            print(e.info)
        if loggin_elements:
            self._set_txt(account, loggin_elements[0])
            self._set_txt(password, loggin_elements[1], password=True)
            self.click_button(loggin_elements[2])

        self.device.wait("idle")
        package = self.device.info["currentPackageName"]
        if package != packageName:
            return True

        self._do_watcher()

    def login(self, account, password):
        """

        :return:
        """
        package = self.device.info["currentPackageName"]
        for i in range(3):
            try:
                self._try_login(account, password, package)
            except:
                stack = traceback.format_exc()
                logger.warn(stack)


if __name__ == '__main__':
    device = get_uiautomator()
    handler = AccountHandler(device)
    handler.login("rdgztest_85548", "wetestd")
    # handler._set_txt("2952020173",resourceId="com.tencent.mobileqq:id/account")
    # handler._set_txt("wetesth",password=True,resourceId="com.tencent.mobileqq:id/password")
    # #className="android.widget.Button",resourceId="com.tencent.mobileqq:id/name"
    # keys={"className":"android.widget.Button","resourceId":"com.tencent.mobileqq:id/name"}
    # handler.click_button(**keys)

    # handler.set_txt("2952020173",resourceId="com.yhkd.jztkc:id/AccountEditText")
    # handler.set_txt("wetesth",password=True,resourceId="com.yhkd.jztkc:id/PasswordEidtText")
    # #className="android.widget.Button",resourceId="com.tencent.mobileqq:id/name"
    # keys={"className":"android.widget.Button","resourceId":"android:id/button1"}
    # handler.click_button(**keys)

    # handler._set_txt("2952020173",resourceId="com.tencent.mobileqq:id/account")
    # handler._set_txt("wetesth",password=True,resourceId="com.tencent.mm:id/a7k")
    # #className="android.widget.Button",resourceId="com.tencent.mobileqq:id/name"
    # keys={"className":"android.widget.Button","resourceId":"com.tencent.mobileqq:id/name"}
    # handler.click_button(**keys)
