# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import sys, os, time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

import wpyscripts.manager as manager

engine = manager.get_engine()
logger = manager.get_logger()


def enter_find_elements():
    find_elements_button = engine.find_element("/Canvas/Panel/FindElements")
    engine.click(find_elements_button)
    time.sleep(1)


def enter_main():
    back_button = engine.find_element("/Canvas/Panel/Back")
    engine.click(back_button)
    time.sleep(1)


def test_find_element():
    """
        使用engine.find_element查找游戏中的节点
    :return:
    """
    button = engine.find_element("/Canvas/Panel/Button")
    bound = engine.get_element_bound(button)
    logger.debug("Button : {0},Bound : {1}".format(button, bound))
    engine.click(button)

    button = engine.find_element("Button")
    bound = engine.get_element_bound(button)
    logger.debug("Button : {0},Bound : {1}".format(button, bound))
    engine.click(button)

    button = engine.find_element("Panel/Button")
    bound = engine.get_element_bound(button)
    logger.debug("Button : {0},Bound : {1}".format(button, bound))
    engine.click(button)

    unexited_gameobj = engine.find_element("Test")
    if unexited_gameobj is None:
        logger.debug("Test GameObject not find")

test_find_element()

def test_find_elements_by_name():
    elements = engine.find_elements_path("/Canvas/Panel/VerticalPanel/Item(Clone)")
    for element in elements:
        bound = engine.get_element_bound(element)
        logger.debug("Button : {0},Bound : {1}".format(element, bound))
        # engine.click(bound)

        time.sleep(0.5)
        # _elements = engine.find_elements_path("Panel/VerticalPanel/Item(Clone)")
        # _elements = engine.find_elements_path("VerticalPanel/Item(Clone)")
        # _elements = engine.find_elements_path("Item(Clone)")
        # _elements = engine.find_elements_path("/Canvas/Panel/*/Item(Clone)")


def test_find_elements_by_index():
    elements = engine.find_elements_path("/Canvas/Panel/VerticalPanel/*[1]")
    for element in elements:
        bound = engine.get_element_bound(element)
        logger.debug("Button : {0},Bound : {1}".format(element, bound))
        engine.click(bound)
        time.sleep(0.5)

    elements = engine.find_elements_path("/Canvas/Panel/VerticalPanel/Button[1]")
    assert elements == []


def test_find_elements_by_img():
    elements = engine.find_elements_path("/Canvas/Panel/Image{img=saturn}")
    for element in elements:
        bound = engine.get_element_bound(element)
        logger.debug("Button : {0},Bound : {1}".format(element, bound))
        engine.click(bound)
        time.sleep(0.5)
    engine.click_position(100, 200)
    elements = engine.find_elements_path("/Canvas/Panel{img=saturn}")
    for element in elements:
        bound = engine.get_element_bound(element)
        logger.debug("Button : {0},Bound : {1}".format(element, bound))


def test_find_elements_by_txt():
    elements = engine.find_elements_path("Panel/VerticalPanel/Item(Clone){txt=关卡2}")
    for element in elements:
        bound = engine.get_element_bound(element)
        logger.debug("Button : {0},Bound : {1}".format(element, bound))
        engine.click(bound)
        time.sleep(0.5)

    elements = engine.find_elements_path("Panel/VerticalPanel/Item(Clone){txt=关卡4}")
    if len(elements) > 0:
        bound = engine.get_element_bound(elements[0])
        logger.debug("Button : {0},Bound : {1}".format(elements[0], bound))
        engine.click(elements[0])

test_find_elements_by_txt()

def test_find_elements_by_component():
    elements=engine.find_elements_by_component("UnityEngine.UI.Button,UnityEngine.UI, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null")
    for element in elements:
        bound = engine.get_element_bound(element)
        logger.debug("Button : {0},Bound : {1}".format(element, bound))
        engine.click(bound)
        time.sleep(0.5)


def main():
    enter_find_elements()
    time.sleep(4)
    test_find_elements_by_component()
