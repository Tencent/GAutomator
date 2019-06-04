#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'


class Account(object):
    QQNAME="" #QQ acount
    QQPWD="" #QQ password
    WECHATNAME="" #wechat account
    WECHATPWD="" #wechat password


class TestInfo(object):
    PACKAGE="com.tencent.GAutomatorSdk" # test package name

### Engine Type
Unity="unity"
UE4="ue4"

class Engine(object):
    Unity="unity"
    UE4="ue4"

EngineType=Engine.Unity #Type="unity" # unity or ue4