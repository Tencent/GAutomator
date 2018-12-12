#-*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

__author__ = 'minhuaxu wukenaihesos@gmail.com'

import os

os.environ["ENGINE_PORT"]="40002"
os.environ["PLATORM_PORT"]="63699"
os.environ["TESTID"]="183747"
os.environ["PACKAGE_NAME"]="com.tencent.tmgp.NBAM"

import unittest

from wpyscripts.manager import *

logger=logging.getLogger("wetest")

class DeviceTest(unittest.TestCase):

    def setUp(self):
        self.device=get_device()


    # def test_get_display_size(self):
    #     size=self.device.get_display_size()
    #     if size:
    #         logger.debug("width : {0},height : {1}".format(size.width,size.height))


    def test_get_top_package_activity(self):
        top_activity=self.device.get_top_package_activity()

        if top_activity:
            logger.debug(top_activity)


    # def test_login_qq_wechat_wait(self):
    #     self.device.login_qq_wechat_wait()
    #
    # def test_clear_qq_account(self):
    #     pid,launchtime=self.device._launch_app()
    #     logger.debug("Pid: {0},Launch time : {1}".format(pid,launchtime))
    #
    # def test_clear_qq(self):
    #     self.device._clear_qq_account()
    #
    #
    # def test_clear_user_info(self):
    #     self.device._clear_user_info()

    # def test_launch_app(self):
    #     self.device._launch_app()

