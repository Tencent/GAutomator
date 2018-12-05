# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import unittest, math, time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..\\..\\")))

from wpyscripts.manager import *

logger = logging.getLogger("wetest")


class UnRealEngineTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UnRealEngineTest, self).__init__(*args, **kwargs)
        self.start_time = None
        self.ui_type = "UGUI"

    def setUp(self):
        self.engine = get_engine("ue4")

    @classmethod
    def setUpClass(cls):
        cls.timeuse = []

    @classmethod
    def tearDownClass(cls):
        for item in cls.timeuse:
            print("{0},{1}".format(item["name"], item["use"]))

    def _start(self):
        self.start_time = time.time()

    def _end(self, name):
        diff = time.time() - self.start_time
        UnRealEngineTest.timeuse.append({"use": diff * 1000, "name": name})

    def test_get_sdk_version(self):
        self._start()
        sdk_info = self.engine.get_sdk_version()
        self._end("get_sdk_version")
        self.ui_type = sdk_info.ui_type
        logger.info(sdk_info)
        # self.assertTrue(cmp(sdk_info.engine_version, "5.1.2f1") == 0, "engine version Error")
        self.assertTrue(cmp(sdk_info.engine, "UE4") == 0, "engine Error")
        self.assertTrue(sdk_info.sdk_version == "1.0.0", "sdkversion Error")

    def test_find_element(self):
        self._start()
        element = self.engine.find_element("Sample")
        self._end("find_element")
        logger.debug(element)

    def test_get_element_bound(self):
        element = self.engine.find_element("Sample")
        logger.debug(element)
        self._start()
        bound = self.engine.get_element_bound(element)
        self._end("get_element_bound")

        logger.info(bound)


    def test_click_position(self):
        element = self.engine.find_element("Sample")
        bound = self.engine.get_element_bound(element)
        self._start()
        result = self.engine.click_position(bound.x + bound.width / 2, bound.y + bound.height / 2)
        self._end("click_position")

        self.assertTrue(result, "Click Error")

    def test_click(self):
        element = self.engine.find_element("Sample")
        self._start()
        result = self.engine.click(element)
        self._end("click")
        # self.assertTrue(result,"Click Element error")

        time.sleep(4)
        element = self.engine.find_element("Sample")
        bound = self.engine.get_element_bound(element)
        result = self.engine.click(bound)
        # self.assertTrue(result,"Click ElementBound error")

    def test_swipe(self):
        start_element = self.engine.find_element("Press")
        end_element = self.engine.find_element("Click")

        # 根据元素按压
        result = self.engine.swipe(start_element, end_element, 100)
        self.assertTrue(result)

        # 根据位置按压
        start_bound = self.engine.get_element_bound(start_element)
        end_bound = self.engine.get_element_bound(end_element)
        self._start()
        result = self.engine.swipe_position(start_bound.x, start_bound.y, end_bound.x, end_bound.y, 500, 2000)
        self._end("swipe_position 2000ms")

        result = self.engine.swipe(start_bound, end_bound, 500, 2000)

    def test_get_current_scene(self):
        self._start()
        scene = self.engine.get_scene()
        self._end("get_scene")

        logger.debug("Scene:{0}".format(scene))
