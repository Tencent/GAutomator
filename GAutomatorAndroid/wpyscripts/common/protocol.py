# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com,alexkan kanchuanqi@gmail.com'


class Commands(object):
    GET_VERSION = 100  # 获取版本号
    FIND_ELEMENTS = 101  # 查找节点
    FIND_ELEMENT_PATH = 102  # 模糊查找
    GET_ELEMENTS_BOUND = 103  # 获取节点的位置信息
    GET_ELEMENT_WORLD_BOUND = 104  # 获取节点的世界坐标
    GET_UI_INTERACT_STATUS = 105  # 获取游戏的可点击信息，包括scene、可点击节点，及位置信息
    GET_CURRENT_SCENE = 106  # 获取Unity的Scene名称
    GET_ELEMENT_TEXT = 107  # 获取节点的文字内容
    GET_ELEMENT_IMAGE = 108  # 获取节点的图片名称
    GET_REGISTERED_HANDLERS = 109  # 获取注册的函数的名称
    CALL_REGISTER_HANDLER = 110  # 调用注册的函数
    SET_INPUT_TEXT = 111  # input控件更换文字信息
    GET_OBJECT_FIELD=112 # 通过反射获取gameobject中component的属性值
    FIND_ELEMENTS_COMPONENT=113 #获取所有包含改组件的gameobject
    SET_CAMERA_NAME=114 #设置渲染的最佳的Camera
    GET_COMPONENT_METHODS = 115  # 反射获取组件上的方法
    CALL_COMPONENT_MOTHOD = 116  # 通过反射调用组件的函数
    LOAD_TEST_LIB=117 #初始化testlib服务

    PRC_SET_METHOD=118#注册python端的方法
    RPC_METHOD = 119#游戏内的接口可调用，python端的方法

    #######################/
    HANDLE_TOUCH_EVENTS = 200  # 发送down move up

    DUMP_TREE = 300

class TouchEvent(object):
    ACTION_DOWN = 0
    ACTION_UP = 1
    ACTION_MOVE = 2

    def __init__(self, x, y, sleeptime, type):
        self.x = x
        self.y = y
        self.sleeptime = sleeptime
        self.type = type
