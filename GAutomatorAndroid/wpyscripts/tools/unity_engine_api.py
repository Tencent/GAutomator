#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from .basic_operator import *

def get_random_choice_by_weight(elements_name):
    """
        根据权重从已知的节点中，随机选择一个
        {("name1":5),("name2":1)}这个表示，随机选择的时候，name1被选到的概率是name2的五倍
    :param elements_name:
    :return:
    """
    elements = []
    dict = {}
    for name, weight in elements_name:
        try:
            e = engine.find_element(name)
            pos = engine.get_element_bound(e)
            tuple = (e, pos.x + pos.width / 2, pos.y + pos.height / 2)
            dict[name] = tuple
            for i in range(weight):
                elements.append(name)
        except:
            stack = traceback.format_exc()
            logger.warning(stack)

    def random_choice_by_weight(update=False):
        name = random.choice(elements)
        e, x, y = dict.get(name)
        if update:
            try:
                e = engine.find_element(name)
                pos = engine.get_element_bound(e)
                dict[name] = (e, pos.x + pos.width / 2, pos.y + pos.height / 2)
                return name, e, pos.x + pos.width / 2, pos.y + pos.height / 2
            except:
                pass
        return name, e, x, y

    return random_choice_by_weight


def random_click(fun=None, forbid_elements=(), max_num=1000, sleep=2):
    """
        随机点击界面上的可操作控件。直到调用fun返回true位置
    :param fun: 如果fun调用返回True，则随机点击结束
    :param forbid_elements: 禁止点击的组件列表(如退出键)
    :param max_num:最大点击次数
    :param sleep:每次点击后的睡眠时间
    :return:
    """
    logger.debug("Random click")
    elements = engine.get_touchable_elements(["LuaButton, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null"])
    for i in range(max_num):
        if elements is None or len(elements) <= 0:
            time.sleep(1)
            elements = engine.get_touchable_elements(["LuaButton, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null"])
            continue
        if fun and fun(elements):
            logger.info("Find need elements")
            return
        elements = filter(lambda e: e[0].object_name not in forbid_elements, elements)
        e, pos = find_less_click_element(elements)
        if pos is None:
            continue
        screen_shot_click_pos(pos["x"], pos["y"])
        time.sleep(sleep)
        elements = engine.get_touchable_elements(["LuaButton, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null"])


def get_random_click(fun=None, forbid_elements=(), max_num=1000, sleep=2):
    def random_click():
        logger.debug("Random click")
        elements = engine.get_touchable_elements()
        for i in range(max_num):
            if len(elements) <= 0:
                time.sleep(1)
                elements = engine.get_touchable_elements()
                continue
            if fun and fun(elements):
                logger.info("Find need elements")
                return
            elements = filter(lambda e: e[0].object_name not in forbid_elements, elements)
            e, pos = find_less_click_element(elements)
            if pos is None:
                continue
            screen_shot_click_pos(pos["x"], pos["y"])
            time.sleep(sleep)
            elements = engine.get_touchable_elements()

    return random_click

def swipe_and_press_relative(start_x, start_y, end_x, end_y, steps, duration, display_size=None):
    """
        根据屏幕的相对坐标进行滑动点击，一般用于摇杆类操作。android手机屏幕尺寸种类较多。用归一化的坐标系，有利于适配屏幕尺寸
        usage:swipe_and_press_relative(0.1275, 0.7932, 0.2512, 0.3037, 200, 3000)
    :param start_x:[0,1]，0代表屏幕最左边,1代表屏幕最右边(width)
    :param start_y:[0,1],0代表屏幕最上边，1代表屏幕底边(height)
    :param end_x:
    :param end_y:
    :param steps:
    :param duration:
    :return:
    """
    if display_size == None:
        display_size = device.get_display_size()
    width, height = display_size.width, display_size.height

    start_x *= width
    start_y *= height
    end_x *= width
    end_y *= height

    logger.debug("Start ({0},{1}) End ({2},{3}) duration {4}".format(start_x, start_y, end_x, end_y, duration))
    engine.swipe_and_press(start_x, start_y, end_x, end_y, steps, duration)