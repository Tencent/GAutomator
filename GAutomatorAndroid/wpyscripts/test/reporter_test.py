#-*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'


import unittest

from wpyscripts.manager import *

logger=logging.getLogger("wetest")

class ReportTest(unittest.TestCase):
    def setUp(self):
        self.report=get_reporter()

    def test_add_tag(self):
        self.report.add_start_scene_tag("GameStart")
        self.report.add_end_scene_tag("GameStart")

    def test_capture_and_mark(self):
        self.report.capture_and_mark(1416.97973633,830.564605713)


    def test_screen_shot(self):
        logger.debug("test_screen_shot")
        self.report.screenshot()

    def test_report_error(self):
        self.report.report("a"=="b",u"测试",u"adfa")
        self.report.report("a"=="a",u"测试2",u"adfas 测试3")
        self.report._report_total()
