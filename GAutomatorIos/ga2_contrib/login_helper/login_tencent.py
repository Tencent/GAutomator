# -*- coding: UTF-8 -*-
import time
import os
import ga2
from ga2.common.logger_config import logger

from ga2.device.iOS.wdaManager import WdaManager

class TencentLoginHelper:

    QQ_BUNDLE_ID="com.tencent.mqq"
    WECHAT_BUNDLE_ID="com.tencent.xin"

    def __init__(self,device):
        self.device=device
        pass

    '''
        login tencent according to current application
        return True/False indicating success/fail
    '''
    def login_tencent(self,account,password):
        if self.device is None:
            logger.error("login_tencent: device is none...")
            return ga2.ERR_LOGIN_FAILED
        top_app=self.device.get_top_app()
        logger.info("top bundle id: "+self.device.get_top_app())
        if top_app==TencentLoginHelper.QQ_BUNDLE_ID:
            return self.login_qq(account=account,password=password)
        elif top_app==TencentLoginHelper.WECHAT_BUNDLE_ID:
            return self.login_wechat(account=account,password=password)
        else:  #sometimes there are alerts, try to login both qq and wechat
            if self.login_qq(account=account,password=password)==ga2.ERR_LOGIN_FAILED:
                return self.login_wechat(account=account, password=password)
            return ga2.ERR_SUCCEED


    def login_qq(self,account,password):
        account=os.environ.get("OTHERNAME",os.environ.get("QQNAME",account))
        password=os.environ.get("OTHERPWD",os.environ.get("QQPWD",password))
        session=self.device.wda_session()

        if session(className='Button', name=u'取消').exists and session(className='Button', nameContains=u'打开').exists:
            session(className='Button', name=u'打开').get().tap()
            logger.info("打开...")
            time.sleep(1)

        self.device.start_alert_handler()
        if session(className='NavigationBar', name=u'QQ一键登录').exists and session(className='Button', nameContains=u'登录').exists:
            session(className='Button', name=u'登录').get().tap()
            return ga2.ERR_SUCCEED

        if session(className='Button', name=u'授权并登录').exists :
            session(className='Button', name=u'授权并登录').get().tap()
            time.sleep(2)
            return ga2.ERR_SUCCEED

        #first time to login
        if session(className='Button', name=u'新用户').exists and session(className='Button', nameContains=u'登录').exists:
            session(className='Button', name=u'登录').get().tap()
            time.sleep(1)
        if session(className='TextField', name=u'帐号').exists:
            session(className='TextField', name=u'帐号').get().tap()
            time.sleep(1)
            session(className='TextField', name=u'帐号').get().set_text(account)
            time.sleep(1)
            session(className='SecureTextField', value=u'密码').tap()
            time.sleep(1)
            session(className='SecureTextField', value=u'密码').set_text(password)
            time.sleep(1)
            session(className='Button', name=u'登录按钮').get().tap()
            if session(className='StaticText', name=u'登录失败').exists:
                return ga2.ERR_LOGIN_FAILED
            if session(className='NavigationBar', name=u'绑定手机号码').exists:
                session(className='Button', name=u'关闭').get().tap()
                if session(className='StaticText', name=u'确定关闭吗？').exists:
                    session(className='Button', name=u'关闭').get().tap()
            if session(className='Button', name=u'取消').exists and session(className='Button',
                                                                          nameContains=u'打开').exists:
                session(className='Button', name=u'打开').get().tap()
                logger.info("打开...")
                time.sleep(1)
            time.sleep(2)
            return ga2.ERR_SUCCEED
        return ga2.ERR_LOGIN_FAILED

    def login_wechat(self,account,password):
        account=os.environ.get("OTHERNAME",os.environ.get("WECHATNAME",account))
        password=os.environ.get("OTHERPWD",os.environ.get("WECHATPWD",password))
        session = self.device.wda_session()
        if session(className='Button', name=u'取消').exists and session(className='Button', nameContains=u'打开').exists:
            session(className='Button', name=u'打开').get().tap()
            logger.info("打开...")
            time.sleep(1)
        self.device.start_alert_handler()
        if session(className='Button', name=u'注册').exists and session(className='Button', nameContains=u'登录').exists:
            logger.info(u'注册 found')
            session(className='Button', name=u'登录').get().tap()
            time.sleep(1)
        if session(className='Button', name=u'用微信号/QQ号/邮箱登录').exists :
            session(className='Button', name=u'用微信号/QQ号/邮箱登录').tap()
            time.sleep(1)
        if session(className='TextField', value=u'微信号/QQ号/邮箱').exists:
            session(className='TextField', value=u'微信号/QQ号/邮箱').get().tap()
            time.sleep(1)
            session(className='TextField', value=u'微信号/QQ号/邮箱').get().set_text(account)
            time.sleep(1)
            session(className='SecureTextField', value=u'请填写密码').tap()
            time.sleep(1)
            session(className='SecureTextField', value=u'请填写密码').set_text(password)
            time.sleep(1)
            session(className='Button', name=u'登录').get().tap()
            time.sleep(3)
            if session(className='Alert', name=u'帐号或密码错误，请重新填写。').exists:
                return ga2.ERR_LOGIN_FAILED
            if session(className='Button', name=u'取消').exists and session(className='Button',
                                                                          nameContains=u'打开').exists:
                session(className='Button', name=u'打开').get().tap()
                logger.info("打开...")
                time.sleep(1)
            return ga2.ERR_SUCCEED
        return ga2.ERR_LOGIN_FAILED