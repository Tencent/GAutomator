# -*- coding: UTF-8 -*-
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

logger = logging.getLogger("wetest")


class DeviceTest(unittest.TestCase):
    def setUp(self):
        self.device = get_device()

    # def test_get_display_size(self):
    #     size = self.device.get_display_size()
    #     if size:
    #         logger.debug("width : {0},height : {1}".format(size.width, size.height))
    #
    # def test_get_top_package_activity(self):
    #     top_activity = self.device.get_top_package_activity()
    #     if top_activity:
    #         logger.debug(top_activity)

    def test_pop_box_monitor(self):
        self.device.start_handle_popbox()
        time.sleep(60)
        self.device.stop_handle_popbox()
        time.sleep(60)


        # def test_login_qq(self):
        #     self.device._clear_qq_account()
        #     result=self.device.login_qq_wechat_wait()
        #     if result:
        #         logger.debug("Login OK")
        #     else:
        #         logger.debug("Login error")


        # def test_launch_app(self):
        #     pid,launchtime=self.device._launch_app("com.tencent.buggame")
        #     logger.debug("pid = {0},launchtime = {1}".format(pid,launchtime))
