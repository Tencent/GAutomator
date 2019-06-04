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

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..","..")))

import wpyscripts.manager as manager

engine = manager.get_engine()
logger = manager.get_logger()


def enter_find_elements():
    find_elements_button = engine.find_element("FindElements")
    engine.click(find_elements_button)
    time.sleep(1)


def enter_main():
    back_button = engine.find_element("Back")
    engine.click(back_button)
    time.sleep(1)


def test_find_element():
    """
        使用engine.find_element查找游戏中的节点
    :return:
    """
    button = engine.find_element("Button_0")
    bound = engine.get_element_bound(button)
    logger.debug("Button : {0},Bound : {1}".format(button, bound))
    engine.click(button)

    button = engine.find_element("Button_1")
    bound = engine.get_element_bound(button)
    logger.debug("Button : {0},Bound : {1}".format(button, bound))
    engine.click(button)

    unexited_gameobj = engine.find_element("Test")
    if unexited_gameobj is None:
        logger.debug("Test GameObject not find")


def main():
    version = engine.get_sdk_version()
    print(version)
    enter_find_elements()
    time.sleep(4)
    test_find_element()


if __name__ == '__main__':
    main()