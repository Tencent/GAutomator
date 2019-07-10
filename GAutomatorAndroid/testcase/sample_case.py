#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import datetime
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
print(sys.path)
from testcase.tools import *

def scene_enter(button, *args, **kwargs):
    """
        decorator of getting into scene
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
        decorater of setting scene tag
    :param tag:
    :param args:
    :param kwargs:
    :return:
    """

    def real_decorator(fun):
        def wrapped(*args, **kwargs):
            report.add_scene_tag(tag)
            try:
                fun()
            except:
                raise
            finally:
                pass
                #report.add_scene_tag(tag+" end")

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
        simple sample
    :return:
    """
    logger.debug("Start test find elements")
    for index in range(1,6):
        name="level{0}Btn".format(index)
        e=engine.find_element(name)
        time.sleep(1)
        if e:
            logger.info("find element :" + str(e))
        screen_shot_click(e)

    report.screenshot()

@scene_enter("Joystick")
@set_scene_tag("Joystick")
def test_joystick():
    person_joystick = engine.find_element("/3rd Person Controller")
    world_bound = engine.get_element_world_bound(person_joystick)
    bound=engine.get_element_bound(person_joystick)
    print(world_bound[0])

  #  joystick_move = move_joystick=engine.find_element("Move_Turn_Joystick")
  #  joystick_camera = engine.find_element("cameraController")
  #   bound = engine.get_element_bound(joystick_move)
    print("joystick bound:" , bound)
    pt = (bound.x + bound.width / 2, bound.y + bound.height / 2)
    print("person:",pt)
    display_size=device.get_display_size()
    display_size=(display_size.width,display_size.height)
    pt2_start= (display_size[0]*0.8719068, display_size[1]*0.6852332)
    pt2_end = (display_size[0]*0.868818,display_size[1]* 0.7830829)
    for i in range(0,5):
        device.touchDown(0,pt[0],pt[1])
        device.touchDown(1, pt2_start[0], pt2_start[1])
        device.touchMove(0, pt[0]+50,pt[1]+50)
        device.touchMove(1, pt2_end[0], pt2_end[1])
        report.screenshot()
        time.sleep(5)
        report.screenshot()
        device.touchUp(0)
        device.touchUp(1)
        time.sleep(5)
    logger.info("multi touch test finished")



def main():
  #  test()
    test_joystick()
    e = engine.find_element("FindElements")
    print(e)
    screen_shot_click(e)
    elems = engine.find_elements_path("/Canvas/Panel/VerticalPanel[0]")
    print(elems)

    time.sleep(3)
 #   test_find_elements()

if __name__ == '__main__':
    main()
    device.touchDown(0,300,300)
    time.sleep(3)
    device.touchUp(0)
