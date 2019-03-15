# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import time, datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..","..")))

import wpyscripts.manager as manager

engine = manager.get_engine()
logger = manager.get_logger()
device = manager.get_device()
reporter = manager.get_reporter()


def screen_shot_click(element):
    logger.debug("screen_shot_click")
    if element is None:
        return
    bound = engine.get_element_bound(element)
    logger.debug(bound)
    pos_x = bound.x + bound.width / 2
    pos_y = bound.y + bound.height / 2
    reporter.capture_and_mark(pos_x, pos_y, locator_name=element.object_name)
    engine.click_position(pos_x, pos_y)


def enter_find_elements():
    find_elements_button = engine.find_element("/Canvas/Panel/Joystick")
    logger.debug(find_elements_button)
    screen_shot_click(find_elements_button)
    time.sleep(1)


def back_main():
    find_elements_button = engine.find_element("/Canvas/Back")
    logger.debug(find_elements_button)
    screen_shot_click(find_elements_button)
    time.sleep(1)


def convert_pos(x, y):
    display_size = device.get_display_size()
    return x * display_size.width, y * display_size.height


def test_joystick():
    # enter_find_elements()
    time.sleep(2)

    start_time = datetime.datetime.now()
    start_x, start_y = convert_pos(0.124454148, 0.677461147)
    end_x, end_y = convert_pos(0.124454148, 0.5945596)
    engine.swipe_position(start_x, start_y, end_x, end_y, 500)
    engine.press_position(end_x, end_y, 5000)

    logger.debug("Use time : {0}".format(datetime.datetime.now() - start_time))
    start_time = datetime.datetime.now()

    start_x, start_y = convert_pos(0.125909746, 0.68911916)
    end_x, end_y = convert_pos(0.173216879, 0.6968912)
    engine.swipe_position(start_x, start_y, end_x, end_y, 500)
    engine.press_position(end_x, end_y, 5000)

    logger.debug("Use time : {0}".format(datetime.datetime.now() - start_time))
    start_time = datetime.datetime.now()

    start_x, start_y = convert_pos(0.8719068, 0.6852332)
    end_x, end_y = convert_pos(0.874818, 0.5880829)
    engine.swipe_position(start_x, start_y, end_x, end_y, 500)
    engine.press_position(end_x, end_y, 5000)

    logger.debug("Use time : {0}".format(datetime.datetime.now() - start_time))
    back_main()


def test_swipe_and_press():
    time.sleep(2)

    start_x, start_y = convert_pos(0.1197916, 0.796296)
    end_x, end_y = convert_pos(0.1197916, 0.69444)
    start_time = datetime.datetime.now()
    engine.swipe_and_press(start_x, start_y, end_x, end_y, 100, 1000)

    logger.debug("Use time : {0}".format(datetime.datetime.now() - start_time))
    time.sleep(3)


def test_world_bounds():
    person = engine.find_element("/3rd Person Controller/Bip001/Bip001 Pelvis")
    world_bound = engine.get_element_world_bound(person)
    logger.debug(world_bound[0])



if __name__ == "__main__":
    test_swipe_and_press()
    pass