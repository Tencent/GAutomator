# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

main.py

main是自动化测试的起点，最大限度的对用户透明。

GAutomator最大的一个特点是，在本地运行与在wetest平台运行测试逻辑代码一致，对用户透明。通过环境变量“PLATFORM_IP”来判定在本地运行还是在wetest平台运行。
在wetest平台上运行的逻辑与本地运行的逻辑不相同。

main.py主要完成包括，清楚QQ、微信、游戏数据，拉起游戏，等待wetest sdk启动等工作。准备工作完成后，会调用testcase.runner.run函数，测试逻辑的起点

本地启动，只运行一台手机的:
usage:
    设置游戏包名，main.py往下，找到找到local_package = os.environ.get("PKGNAME", ""),设置包名，如找到local_package=com.tencent.wetest.demo
     python main.py

运行多台手机:
usage:
    "python main.py --qqname=2952020110 --qqpwd=wetestpwd --engineport=50031 --uiport=19000 --serial=saaaweadf"
    "python main.py --qqname=2952020111 --qqpwd=wetestpwd --engineport=50032 --uiport=19001 --serial=asdfadfadf"

    这两个命令会分别启动在序列号(adb devices查看)的手机上运行自动化.参数详见main()

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import os
import traceback
import time
import getopt
import sys
import optparse
import wpyscripts.manager as manager
from wpyscripts.common.wetest_exceptions import *


local_package = os.environ.get("PKGNAME", "")  # 你需要测试的包名,可以设置默认值


def _prepare_environ():
    if os.environ.get("PLATFORM_IP", None) is None:
        """
            如果本地运行，需要设置登录的账户名和密码
        """
        if not os.environ.get("QQNAME", None):
            os.environ["QQNAME"] = ""
            os.environ["QQPWD"] = ""

        if not os.environ.get("WECHATNAME", None):
            os.environ["WECHATNAME"] = ""
            os.environ["WECHATPWD"] = ""

        env = os.environ.get("PLATFORM_IP")

        if not env:
            # 本地环境
            if not local_package:
                raise WeTestRuntimeError("You must set your game package name,at the top of the file")
            else:
                os.environ["PKGNAME"] = local_package


def _native_prepare():
    # 本地环境准备，清楚数据，拉起游戏
    device = manager.get_device()
    device._clear_qq_account()
    device._clear_user_info(local_package)
    device.launch_app(local_package)
    time.sleep(10)
    return True


def _cloud_prepare():
    # 云端测试，只需要拉起游戏
    reporter = manager.get_reporter()
    device = manager.get_device()
    logger = manager.get_logger()
    try:
        reporter.screenshot()
        res = device.launch_app()
        logger.debug(res)
        reporter.screenshot()
        time.sleep(10)
        return True
    except:
        stack = traceback.format_exc()
        logger.error(stack)
        logger.error("Launch app failure")
        return False


def _prepare():
    # 准备工作
    # 清理QQ、微信账号，清理游戏数据确保每次启动的逻辑是一样的。然后，拉起游戏
    env = os.environ.get("PLATFORM_IP")
    logger = manager.get_logger()
    lanuch_result = False
    if env:
        lanuch_result = _cloud_prepare()
    else:
        lanuch_result = _native_prepare()

    if lanuch_result:
        # 拉起成功，通常游戏会有一段过场动画，这时候并不一定会启动我们这边的sdk，我们需要不断的尝试连接SDK。如果,连接成功获取sdk版本号则游戏已经启动
        logger.debug("Launch package {0} SUCCESS,try to connect U3DAutomation SDK".format(os.environ["PKGNAME"]))
        global engine
        engine = manager.get_engine()
        version = None
        for i in range(30):
            try:
                version = engine.get_sdk_version()
                if version:
                    logger.debug(version)
                    manager.save_sdk_version(version)
                    return True
            except:
                time.sleep(2)
    return False


def _run():
    prepare = _prepare()
    logger = manager.get_logger()
    reporter = manager.get_reporter()
    if not prepare:
        reporter.screenshot()
        logger.error("Connect to sdk fail,please config your game contain sdk or not in the first scene")
        return
    try:
        import testcase.runner as runner
        runner.run()
    except WeTestRuntimeError as e:
        stack = traceback.format_exc()
        logger.exception(stack)


def main():
    """
        在自己的pc上运行时，如果需要操控多台手机，可以通过命令行的方式启动
        关于账号或者密码，只需要设置一种账号类型即可。在有第三方账号的话，会优先使用第三方账号
        --qqname:qq账号，每部手机应该都不一样
        --qqpwd:qq密码
        --wechataccount:微信账号
        --wechatpwd:微信密码
        --othername:其他任何账号
        --otherpwd:其他任何账号的密码

        --engineport:与手机端的sdk服务建立网络映射，填入的为本地的网络端口号（如,50031），不同手机之间要确保不同
        --uiport:与手机端的UIAutomator服务建立网络映射，填入的为本地的网络端口号（如,19008），不同手机之间要确保不同
        --serial:adb devcies能够查看手机的序列号，不同的序列号代表不同的手机

    :return:
    """
    usage = "usage:%prog [options] --qqname= --qqpwd= --engineport= --uiport= --serial="
    parser = optparse.OptionParser(usage)
    parser.add_option("-q", "--qqname", dest="QQNAME", help="QQ Account")
    parser.add_option("-p", "--qqpwd", dest="QQPWD", help="QQ Password")
    parser.add_option("-b", "--wechataccount", dest="WECHATNAME", help="wechat Account")
    parser.add_option("-c", "--wechatpwd", dest="WECHATPWD", help="wechat Password")
    parser.add_option("-e", "--engineport", dest="LOCAL_ENGINE_PORT", help="network port forward engine sdk")
    parser.add_option("-u", "--uiport", dest="UIAUTOMATOR_PORT", help="network port forward uiautomator server")
    parser.add_option("-s", "--serial", dest="ANDROID_SERIAL", help="adb devices android mobile serial")
    parser.add_option("-g", "--othername", dest="OTHERNAME", help="upload account")
    parser.add_option("-f", "--otherpwd", dest="OTHERPWD", help="upload password")
    (options, args) = parser.parse_args()
    try:
        if options.QQNAME:
            os.environ["QQNAME"] = options.QQNAME
        if options.QQPWD:
            os.environ["QQPWD"] = options.QQPWD
        if options.LOCAL_ENGINE_PORT:
            os.environ["LOCAL_ENGINE_PORT"] = options.LOCAL_ENGINE_PORT
        if options.UIAUTOMATOR_PORT:
            os.environ["UIAUTOMATOR_PORT"] = options.UIAUTOMATOR_PORT
        if options.ANDROID_SERIAL:
            os.environ["ANDROID_SERIAL"] = options.ANDROID_SERIAL
        if options.OTHERNAME:
            os.environ["OTHERNAME"] = options.OTHERNAME
        if options.OTHERPWD:
            os.environ["OTHERPWD"] = options.OTHERPWD
        if options.WECHATNAME:
            os.environ["WECHATNAME"] = options.WECHATNAME
        if options.WECHATPWD:
            os.environ["WECHATPWD"] = options.WECHATPWD

        _prepare_environ()
    except getopt.error, msg:
        print("for help use --help")
        return 2

    logger = manager.get_logger()
    try:
        _run()
    except:
        stack = traceback.format_exc()
        logger.exception(stack)
    finally:
        logger.debug("GAutomator End")


if __name__ == "__main__":
    sys.exit(main())
