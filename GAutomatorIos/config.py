#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py    
@Contact :   davidzkpu@tencent.com
@License :   (C)Copyright 2020-2021, TIMI-TI-TEST

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/28 5:23 下午   davidzkpu      1.0         NONE
'''

from enum import Enum

class Account(object):
    QQNAME="" #QQ acount
    QQPWD="" #QQ password
    WECHATNAME="" #wechat account
    WECHATPWD="" #wechat passwords


class TestInfo(object):
    PACKAGE="" # test package name
    udid = "" #ios udid

### Engine Type
Unity="unity"
UE4="ue4"

class EngineType(Enum):
    Unity=0,
    UE4=1

EngineType=EngineType.UE4 #Type="unity" # unity or ue4