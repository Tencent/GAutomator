# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

main.py

A feature of GAutomator is , the code are almost same when running on WeTest Cloud and locally.
 The Environment Varaible PLATFORM_IP indicates whether the script is running on WeTest Cloud or local.
What main.py does :  prepare for test ( launch the game and connect to GAutomator SDK), and GetInto testcase.runner.run() 

To run it  with single device:
usage:
     get into the config.py and set your packagename , engine type, and account info to login in game 
     python main.py

To run it locally with multiple devices:
usage:
    "python main.py --qqname=2952020110 --qqpwd=wetestpwd --engineport=50031 --uiport=19000 --serial=saaaweadf"
    "python main.py --qqname=2952020111 --qqpwd=wetestpwd --engineport=50032 --uiport=19001 --serial=asdfadfadf"
    
    the scripts will be runned with the devices individually.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import os
import traceback
import time
import getopt
import sys
import optparse
from config import Account,TestInfo
import wpyscripts.manager as manager
from wpyscripts.common.wetest_exceptions import *

local_package = os.environ.get("PKGNAME", TestInfo.PACKAGE)  # the package name you want to test

def _prepare_environ():
    if os.environ.get("PLATFORM_IP", None) is None:
        """
            if the script is runned locally ,account and password should be set
        """
        if not os.environ.get("QQNAME", None):
            os.environ["QQNAME"] = Account.QQNAME
            os.environ["QQPWD"] = Account.QQPWD

        if not os.environ.get("WECHATNAME", None):
            os.environ["WECHATNAME"] = Account.WECHATNAME
            os.environ["WECHATPWD"] = Account.WECHATPWD

        env = os.environ.get("PLATFORM_IP")

        if not env:
            # 本地环境
            if not local_package:
                raise WeTestRuntimeError("You must set your game package name,at the top of the file")
            else:
                os.environ["PKGNAME"] = local_package

def _native_prepare():
    # clear qq/wechat/app data and launch the app
    device = manager.get_device()
    device._clear_qq_account()
    device._clear_user_info(local_package)
    device.launch_app(local_package)
    time.sleep(10)
    return True

def _cloud_prepare():
    # test in cloud, just launch the app
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
    #clear qq,wechat and game datax on device to make sure a stable test environment, and then launch the game.
    env = os.environ.get("PLATFORM_IP")
    logger = manager.get_logger()
    lanuch_result = False
    if env:
        lanuch_result = _cloud_prepare()
    else:
        lanuch_result = _native_prepare()

    if lanuch_result:
        #launch success. in general , a game may have a loading phase in which the sdk has not been launched. So we try to connect SDK in a loop.
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
        when testing several phones on your local PC, you could run the py by cmd
        you only need to set one type of account. "othername and other pwd" will be used preferentially if multiple types are provided.
        --qqname:qqaccount 
        --qqpwd:qq password
        --wechataccount:wechat account
        --wechatpwd:wechat password
        --othername:any other accounts
        --otherpwd: password of othername
        --engineport:  the forward port mapping to the sdk port in device. the parameters for each device should be individually provided.
        --uiport:the forward port mapping to the uiautomator port in device. the parameters for each device should be individually provided.
        --serial: serial number of the target device. you could get it by "adb devices -l"

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
    except getopt.error as msg:
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
