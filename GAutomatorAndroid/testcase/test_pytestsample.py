#-*- coding: UTF-8 -*-
'''
a demo integrating pytest with gautomator 
run: py.test -q testcase/test_pytestsample.py
'''
from testcase.tools import *
import os
import pytest
import time

# content of test_class.py
from wpyscripts import manager

device = manager.get_device()
logger = manager.get_logger()
engine = manager.get_engine()

from config import TestInfo

local_package = os.environ.get("PKGNAME", TestInfo.PACKAGE)  # the package name you want to test

def setup_module(module):
    device._clear_user_info(local_package) #clear game data (will kill the running game process )
    pass

def teardown_module(module):
    report._report_total()

@report_wetest
def test_launch():
    device.launch_app(local_package)
    connect_success = False
    for i in range(30):
        try:
            version = engine.get_sdk_version()
            if version:
                logger.debug(version)
                connect_success  = True
                break
        except:
            time.sleep(2)
    assert(connect_success)

@report_wetest
def test_find_elements():
    assert(engine.get_scene() == 'main')
    assert(screen_shot_click('FindElements'))
    assert(screen_shot_click('/Canvas/Panel/Back'))
    assert (engine.get_scene() == 'main')

@report_wetest
def test_interaction():
    assert (engine.get_scene() == 'main')
    screen_shot_click('/Canvas/Panel/Interaction')
    element = engine.find_element("/Canvas/Panel/Press")
    assert(element)
    engine.press(element, 2000)
    time.sleep(2)
    engine.press_position(1200, 100, 3000)
    element = engine.find_element("/Canvas/Panel/InputField")
    assert (element)
    engine.input(element, "Run Wpy")
    assert(screen_shot_click('/Canvas/Panel/Back'))
    assert (engine.get_scene() == 'main')

@report_wetest
def test_failtest():
    assert (1==2)

if __name__ == '__main__':
    pytest.main()