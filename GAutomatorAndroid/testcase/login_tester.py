#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from testcase.tools import *

def tencent_login1(login_button, sleeptime=10):
    """
        腾讯游戏的登陆方式
    :return:
    """
    # 选择QQ登陆
    qq_button = find_element_wait(login_button, max_count=40, sleeptime=3)
    if qq_button == None:
        logger.debug("Can't Find QQ Login Btn")
        report.screenshot()
        sys.exit(0)
    screen_shot_click(qq_button, 6)

    # 步骤2 ，等待进入QQ登录界面，packagename为com.tencent.mobileqq，如果是微信登录界面package为com.tencent.mm
    wait_for_package("com.tencent.mobileqq")
    report.screenshot()
    device.login_qq_wechat_wait(120)
    report.screenshot()

    # 登陆结束后大部分游戏都需要初始化一段时间
    time.sleep(sleeptime)

def handle_dialog():
    for i in range(10):
        closeBtn=engine.find_element("closeBtn")
        if closeBtn:
            screen_shot_click(closeBtn)
        else:
            logger.debug("No Dialog any more")
            break



def login_test_main():
    tencent_login1("m_loginQQ")

    logger.debug("wait for select server")
    time.sleep(5)
    handle_dialog()

    m_btnStartGame=engine.find_element("m_btnStartGame")
    screen_shot_click(m_btnStartGame)

    m_loginBtn=engine.find_element("m_loginBtn")
    screen_shot_click(m_loginBtn)
