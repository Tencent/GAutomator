# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..","..")))

from testcase.tools import *
from wpyscripts.manager import time_snap


def scene_enter(button, *args, **kwargs):
    """
        进入某个scene的，修饰符
    :param button:
    :param args:
    :param kwargs:
    :return:
    """

    def real_decorator(fun):
        def wrapped(*args, **kwargs):
            enter = engine.find_element(button)
            screen_shot_click(enter)
            fun(*args, **kwargs)
            time.sleep(2)
            back = engine.find_element("Back")
            screen_shot_click(back)

        return wrapped

    return real_decorator


def set_scene_tag(tag, *args, **kwargs):
    """
        函数两侧打标签
    :param tag:
    :param args:
    :param kwargs:
    :return:
    """

    def real_decorator(fun):
        def wrapped(*args, **kwargs):
            report.add_start_scene_tag(tag)
            try:
                fun()
            except:
                raise
            finally:
                report.add_end_scene_tag(tag)

        return wrapped

    return real_decorator


def test():
    version = engine.get_sdk_version()
    logger.debug("Version Information : {0}".format(version))

    scene = engine.get_scene()
    logger.debug("Scene :   {0}".format(scene))

    sample_button = engine.find_element("/Canvas/Panel/Sample")
    logger.debug("Button : {0}".format(sample_button))
    logger.debug("Button Bound: {0}".format(engine.get_element_bound(sample_button)))
    screen_shot_click(sample_button)


def start():
    sample = engine.find_element("Sample")
    screen_shot_click(sample)


@scene_enter("FindElements")
@set_scene_tag("FindElements")
def test_find_elements():
    """
        主要覆盖测试report的内容
    :return:
    """
    items = engine.find_elements_path("/Canvas/Panel/VerticalPanel/Item(Clone)")
    for item in items:
        screen_shot_click(item, 3)

    report.screenshot()


@scene_enter("Interaction")
def test_interaction():
    """
        主要测试下device内容
    :return:
    """
    press_relative_screen(0.6363, 0.0925, 5000)

    time.sleep(3)

    silder = engine.find_element("/Canvas/Panel/Slider")
    if silder:
        bound = engine.get_element_bound(silder)
        engine.swipe_position(bound.x, bound.y + bound.height / 2.0, bound.x + bound.width, bound.y + bound.height / 2,
                              3000)

    game_activity = device.get_top_package_activity()
    logger.debug(game_activity)
    report.screenshot()

    rotation = device.get_rotation()
    logger.debug(rotation)
    report.screenshot()

    time.sleep(3)


def convert_pos(x, y):
    display_size = device.get_display_size()
    return x * display_size.width, y * display_size.height


def test_joystick():
    # enter_find_elements()
    time.sleep(2)

    start_time = datetime.datetime.now()
    start_x, start_y = convert_pos(0.124454148, 0.677461147)
    end_x, end_y = convert_pos(0.124454148, 0.5945596)
    engine.swipe_and_press(start_x, start_y, end_x, end_y, 100, 4000,step_sleep=50)
    engine.press_position(end_x, end_y, 5000)

    logger.debug("Use time : {0}".format(datetime.datetime.now() - start_time))
    start_time = datetime.datetime.now()

    start_x, start_y = convert_pos(0.125909746, 0.68911916)
    end_x, end_y = convert_pos(0.173216879, 0.6968912)
    engine.swipe_and_press(start_x, start_y, end_x, end_y, 200, 3000,step_sleep=40)
    engine.press_position(end_x, end_y, 5000)

    logger.debug("Use time : {0}".format(datetime.datetime.now() - start_time))
    start_time = datetime.datetime.now()

    start_x, start_y = convert_pos(0.8719068, 0.6852332)
    end_x, end_y = convert_pos(0.874818, 0.5880829)
    engine.swipe_and_press(start_x, start_y, end_x, end_y, 200, 2000,step_sleep=40)
    engine.press_position(end_x, end_y, 5000)

    logger.debug("Use time : {0}".format(datetime.datetime.now() - start_time))


@time_snap(interval=5, times=120)
@scene_enter("Joystick")
def test_joysctick_perform():
    report.screenshot()
    report.add_start_scene_tag("Without")
    for i in range(30):
        time.sleep(10)
        report.screenshot()
    report.add_end_scene_tag("Without")
    time.sleep(10)

    person = engine.find_element("/3rd Person Controller/Bip001/Bip001 Pelvis")
    report.add_start_scene_tag("Operaction")
    # 模拟告诉请求，查看对性能的影响
    for i in range(30):
        world_bound = engine.get_element_world_bound(person)
        logger.debug(world_bound[0])
        time.sleep(1)
        # report.screenshot()
        test_joystick()
    report.add_end_scene_tag("Operaction")


def main():
    # report.screenshot()
    # start()
    # test_find_elements()

    test_interaction()
    report.report(True,u"report_test",u"Report test error 中文")
    test_joysctick_perform()


if __name__ == '__main__':
    main()
