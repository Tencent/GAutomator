# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

import wpyscripts.manager as manager

engine = manager.get_engine()
logger = manager.get_logger()


def test_click():
    # 点击节点
    element = engine.find_element("/Canvas/Panel/Click")
    bound = engine.get_element_bound(element)
    logger.debug("Button : {0},Bound : {1}".format(element, bound))

    engine.click(bound)
    time.sleep(1)
    engine.click(element)

    # 点击坐标
    time.sleep(2)
    engine.click_position(600.0, 100.0)


def test_press():
    element = engine.find_element("/Canvas/Panel/Press")
    engine.press(element, 5000)
    time.sleep(2)
    engine.press_position(1200, 100, 3000)


def test_swipe():
    start_e = engine.find_element("/Canvas/Panel/Press")
    end_e = engine.find_element("/Canvas/Panel/Click")
    engine.swipe(start_e, end_e, 50,2000)

    time.sleep(5)

    silder = engine.find_element("/Canvas/Panel/Slider")
    if silder:
        bound = engine.get_element_bound(silder)
        engine.swipe_position(bound.x, bound.y + bound.height / 2.0, bound.x + bound.width, bound.y + bound.height / 2,
                              100,3000)


def test_input():
    element = engine.find_element("/Canvas/Panel/InputField")
    engine.input(element, "Run Wpy")


def test_get_touchable_elements():
    e = engine.find_element("/Canvas/Panel/Close")
    engine.click(e)

    elements = engine.get_touchable_elements()
    for e, pos in elements:
        logger.debug("Button : {0},Bound : {1}".format(e, pos))

    time.sleep(2)
    engine.click_position(elements[0][1]["x"], elements[0][1]["y"])


def test_get_component_methods():
    element = engine.find_element("Sample")
    methods = engine.get_component_methods(element, "ReflectionTest")
    logger.debug(methods)


def test_call_component_method():
    element = engine.find_element("Sample")
    params = []
    params.append(5)
    params.append("Hello World")
    result = engine.call_component_method(element, "ReflectionTest", "TestReflection", params)
    logger.debug(result)


test_get_touchable_elements()
