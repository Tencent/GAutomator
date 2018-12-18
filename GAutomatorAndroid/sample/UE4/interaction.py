#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..","..")))

import wpyscripts.manager as manager

engine = manager.get_engine()
logger = manager.get_logger()


def test_click():
    # 点击节点
    element = engine.find_element("ClickBtn")
    bound = engine.get_element_bound(element)
    logger.debug("Button : {0},Bound : {1}".format(element, bound))

    engine.click(bound)
    time.sleep(1)
    engine.click(element)

    # 点击坐标
    time.sleep(2)
    engine.click_position(600.0, 100.0)

def test_press():

    element = engine.find_element("PressBtn")
    engine.press(element, 1000)
    time.sleep(2)
    engine.press_position(1100, 190, 1000)


def test_swipe():
    start_e = engine.find_element("ClickBtn")
    end_e = engine.find_element("PressBtn")
    engine.swipe(start_e, end_e,2000)

    time.sleep(5)

    silder = engine.find_element("Slider_0")
    if silder:
        bound = engine.get_element_bound(silder)
        engine.swipe_position(bound.x+3, bound.y + bound.height / 2.0, bound.x + bound.width, bound.y + bound.height / 2,3000)


def test_get_element_txt():
    e=engine.find_element("TextBlock_0")
    text=engine.get_element_text(e)
    logger.debug("Text = {0}".format(text))

if __name__ == '__main__':
    test_get_element_txt()