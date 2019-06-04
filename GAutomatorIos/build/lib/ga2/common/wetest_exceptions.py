# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'
import six
if six.PY2:
    from exceptions import RuntimeError


class WeTestRuntimeError(RuntimeError):
    """
        与引擎、平台设备交互过程中遇到不可忽略的错误时抛出
    """
    pass


class WeTestEnvironmentError(WeTestRuntimeError):
    """
        环境变量设置有问题
    """
    pass


class WeTestPlatormError(WeTestRuntimeError):
    """
        平台连接错误
    """
    pass


class NetError(WeTestRuntimeError):
    """
        网络相关错误，初始化失败、网络断开连接
    """
    pass


class WeTestInvaildArg(WeTestRuntimeError):
    """
        错误的输入接口
    """
    pass


class WeTestSDKError(WeTestRuntimeError):
    """
        SDK错误
    """
    pass


class WeTestSDKTimeOut(WeTestRuntimeError):
    """
        SDK超时错误
    """
    pass


class WeTestInvaildSdkVersion(WeTestRuntimeError):
    """
        当前wpyscripts不支持对应的SDK
    """


class SceneTagError(WeTestRuntimeError):
    """
        性能数据设置标签错误
    """


class LoginError(WeTestRuntimeError):
    """
        登陆出错，比如QQ或微信没有账号密码等
    """


class UIAutomatorError(WeTestRuntimeError):
    """
        调用UIAutomator时错误
    """


class UIAutomatorLoginError(WeTestRuntimeError):
    """
        登录时出错
    """
