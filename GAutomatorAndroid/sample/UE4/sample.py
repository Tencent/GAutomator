#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..","..")))

from testcase.tools import *


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

    sample_button = engine.find_element("Sample")
    logger.debug("Button : {0}".format(sample_button))
    logger.debug("Button Bound: {0}".format(engine.get_element_bound(sample_button)))
    screen_shot_click(sample_button)

@scene_enter("FindElements")
@set_scene_tag("FindElements")
def test_find_elements():
    """
        主要覆盖测试report的内容
    :return:
    """
    logger.debug("Start test find elements")
    for index in range(1,6):
        name="level{0}Btn".format(index)
        e=engine.find_element(name)
        screen_shot_click(e)

    report.screenshot()


if __name__ == '__main__':
    test()
    #test_find_elements()