# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import time
import traceback
import random
import sys
import os

import wpyscripts.manager as manager
from wpyscripts.common.wetest_exceptions import *

logger = manager.get_logger()
engine = manager.get_engine()
device = manager.get_device()
report = manager.get_reporter()

click_dict = {}

game_package = None
game_activity = None

_display_size = None


def screen_shot_click(element, sleeptime=2, exception=False):
    """
        截图->点击的位置标记红点->点击->sleep指定的时间
    :param element:Element instance or element name
    :param sleeptime: sleep time second
    :param exception: 异常发生时，如果exception为True则抛出异常，如果False不会抛出异常，返回False
    :return:
    """
    if element is None:
        return
    if isinstance(element, str):
        try:
            element = engine.find_element(element)
        except WeTestRuntimeError as e:
            message = "{0} can't find".format(element)
            logger.error(message)
            if exception:
                raise
            else:
                return False
    try:
        bound = engine.get_element_bound(element)
    except WeTestRuntimeError as e:
        bound = None
    if not bound:
        if exception:
            raise WeTestRuntimeError("element can't click {0}".format(element))
        else:
            return False
    logger.debug(bound)
    pos_x = bound.x + bound.width / 2
    pos_y = bound.y + bound.height / 2
    try:
        report.capture_and_mark(pos_x, pos_y, locator_name=element.object_name+"_%s"%time.time())
        #device.ui_device.click(pos_x,pos_y)
        engine.click_position(pos_x, pos_y)
        logger.debug("screen_shot_click_pos x = {0},y = {1},name = {2}".format(pos_x, pos_y, element.object_name))
    except:
        logger.warn("screen_shot_click_pos x = {0},y = {1},name = {2} failed".format(pos_x, pos_y, element.object_name))
        if exception:
            raise

    time.sleep(sleeptime)
    return True


def screen_shot_click_pos(pos_x, pos_y, sleeptime=2, exception=True):
    """
        点击屏幕位置，截图并标记红点
    :param pos_x:x coordinate
    :param pos_y:y coordinate
    :param sleeptime:sleep time after click,sceond
    :param exception:异常发生时，如果exception为True则抛出异常，如果False不会抛出异常，返回False
    :return:
    """
    logger.debug("screen_shot_click_pos x = {0},y = {1},timesleep = {2}".format(pos_x, pos_y, sleeptime))
    try:
        report.capture_and_mark(pos_x, pos_y, "click_%s"%time.time())
        engine.click_position(pos_x, pos_y)
        time.sleep(sleeptime)
    except WeTestRuntimeError as e:
        stack = traceback.format_exc()
        logger.error(stack)
        if exception:
            raise
        else:
            return False
    return True


def find_and_click(*objects):
    """
        只要出现都会点击掉。
    :param objects:
    :return:
    """
    for name in objects:
        try:
            e = engine.find_element(name)
            screen_shot_click(e, sleeptime=0.3)
        except:
            stack = traceback.format_exc()
            logger.warn(stack)


def get_condition_fun(*name):
    """
        主要用于random_click，传入一系列的elements，只要可点击的节点里面有符合的就返回

        应用场景：需要点击某个节点，但是在该界面可能出现弹出框。弹出框不确定的情况下，可以使用
    :param name:
    :return:
    """

    def find_need_element(elements):
        for e, pos in elements:
            if e.object_name in name:
                logger.info("Find element name {0}".format(e.object_name))
                return True
        return False

    return find_need_element


def get_scene_condition_fun(*name):
    """
        主要用于random_click，只要有到达符合的scene，random_click就退出
    :param name:
    :return:
    """
    engine = manager.get_engine()

    def find_need_scene(elements):
        try:
            scene = engine.get_scene()
            if scene in name:
                return True
        except:
            pass
        return False

    return find_need_scene


def get_un_scene_condition_fun(*name):
    def find_un_need_scene(elements):
        try:
            scene = engine.get_scene()
            if scene not in name:
                return True
        except:
            pass
        return False

    return find_un_need_scene


def handle_ungame_activity():
    """
        检测到不是游戏的activity时，使用回退键。因为无法对标准控件做处理。

        注：使用该接口，必须要在游戏界面时调用wait_for_scene()。一般在登陆界面调用，也可以等待过掉动画界面
    :return:
    """
    pkg=game_package or os.environ.get("PKGNAME")
    package_activity = device.get_top_package_activity()
    if package_activity.package_name != pkg:
        report.screenshot()
        device.back()
        time.sleep(3)
        report.screenshot()


def find_elements_tries(name, max_count=10, sleeptime=3):
    """
        找到指定的节点，否者随机点击
    :param name:
    :param max_count:
    :param sleeptime:
    :return:
    """
    for i in range(max_count):
        try:
            element = engine.find_element(name)
        except WeTestRuntimeError as e:
            handle_ungame_activity()

        if element:
            return element
        else:
            time.sleep(sleeptime)
            random_click(get_condition_fun(name))


def find_elment_wait(name, max_count=10, sleeptime=3):
    """
        查找控件

        通常操作后界面可能会发生巨大变化，且变化所需要的时间不确定时一般会使用该接口。如开始游戏，然后等待大厅界面加载完毕。
    :param name:需要等待出现的element的名称
    :param max_count:最大尝试次数，max_count*sleeptime约等于最大等待市场
    :param sleeptime:每次失败后，间隔查找的时间
    :return: Element instance if find,None if not find
    """
    element = None
    for i in range(max_count):
        try:
            element = engine.find_element(name)
        except WeTestRuntimeError as e:
            # 存在抛出异常的可能，比如说切换过程中，游戏可能并不在前台
            logger.warn(e)
            time.sleep(sleeptime)
        if element:
            return element
        else:
            time.sleep(sleeptime)


def wait_for_scene(name, max_count=20, sleeptime=2):
    """
        等待到达某个场景。如游戏拉起后，可能还需要经历一段开场动画，过一段时间后才进入QQ登录界面，可以使用该接口

        该接口同样会，保存游戏的activity

    :param name:
    :return:
    """
    scene = None
    for i in range(max_count):
        try:
            scene = engine.get_scene()
        except Exception as e:
            logger.error(e)
            time.sleep(sleeptime)
        if scene == name:
            # 保存游戏的package和activity
            global game_package, game_activity
            package_activity = device.get_top_package_activity()
            game_package = package_activity.package_name
            game_activity = package_activity.activity
            logger.debug("Save Game Package {0}".format(game_package))
            return True
        time.sleep(sleeptime)
    return False


def find_less_click_element(elements):
    """
        一直等待，直到某个节点消失
    :param elements:
    :return:
    """
    global click_dict
    min_num = 1000
    min_element = None
    min_pos = None
    num = 0
    for e, pos in elements:
        if click_dict.has_key(e.object_name):
            num = click_dict[e.object_name]
        else:
            num = 0
            click_dict.setdefault(e.object_name, 0)
        if num < min_num:
            min_element = e
            min_pos = pos
            min_num = num
    click_dict[min_element.object_name] = min_num + 1
    return min_element, min_pos


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
            logger.warn(stack)

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

def wait_for_package(name):
    """

    :param name:
    :return:
    """
    top_package_activity = None
    for i in range(20):
        try:
            top_package_activity = device.get_top_package_activity()
        except Exception as e:
            stack = traceback.format_exc()
            logger.error(stack)
        if top_package_activity == None:
            time.sleep(1)
            continue
        if top_package_activity.package_name == name:
            logger.debug("Find pakcage {0}".format(top_package_activity.package_name))
            return True
        time.sleep(1)


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


def convert(x, y):
    display_size = device.get_display_size()
    width, height = display_size.width, display_size.height

    x *= width
    y *= height
    return x, y


def tencent_login(scene_name, login_button, sleeptime=10):
    """
        腾讯游戏的登陆方式
    :return:
    """
    # 步骤1，等待到达登录界面
    wait_for_scene(scene_name)

    # 选择QQ登陆
    qq_button = find_elment_wait(login_button, max_count=40, sleeptime=3)
    if qq_button == None:
        logger.debug("Can't Find QQ Login Btn")
        report.screenshot()
        sys.exit(0)
    screen_shot_click(qq_button, 6)

    # 步骤2 ，等待进入QQ登录界面，packagename为com.tencent.mobileqq，如果是微信登录界面package为com.tencent.mm
    wait_for_package("com.tencent.mobileqq")
    report.screenshot()
    device.login_qq_wechat_wait(120)
    report.screenshot()

    # 登陆结束后大部分游戏都需要初始化一段时间
    time.sleep(sleeptime)


def press_relative_screen(x, y, time, name="Press"):
    try:
        global _display_size
        if _display_size == None:
            _display_size = device.get_display_size()
        width, height = _display_size.width, _display_size.height
        x *= width
        y *= height

        report.capture_and_mark(x, y, name)
        engine.press_position(x, y, time)
    except:
        stack = traceback.format_exc()
        logger.warn(stack)


def screen_and_press(bound, time, name):
    try:
        x = bound.x + bound.width / 2
        y = bound.y + bound.height / 2
        report.capture_and_mark(x, y, name)
        engine.press_position(x, y, time)
    except:
        stack = traceback.format_exc()
        logger.warn(stack)
