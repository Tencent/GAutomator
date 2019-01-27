# -*- coding: UTF-8 -*-

import os
from config import Account,TestInfo
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
