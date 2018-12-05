# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

import time
import os
import logging
from wpyscripts.httptools.remote_connection import RemoteConnection, Method
from wpyscripts.common.wetest_exceptions import WeTestPlatormError,WeTestInvaildArg

logger = logging.getLogger("wetest")


class Command(object):
    GET_ROTATION = (Method.GET, "rotation")
    CLEAR_APP_DATA = (Method.POST, "clearappdata")
    LAUNCH_APP = (Method.POST, "launchapp")
    TOUCH_CAPTURE = (Method.POST, "touchcapture")
    CURRENT_PACKAGE_NAME = (Method.GET, "currentpackagename")
    RESOLUTION = (Method.GET, "resolution")
    CAPTURE = (Method.POST, "snapshot")
    STOP_UIAUTOMATOR = (Method.GET, "pauseuiautomator")
    START_UIAUTOMATOR = (Method.GET, "resumeuiautomator")
    TOUCH = (Method.POST, "touch")
    GET_TEST_TIME = (Method.GET, "runtime")
    SCENE_TAG = (Method.POST, "scenetag")
    ANDROIDVERSION = (Method.GET, "androidversion")
    MODEL = (Method.GET, "model")
    FORWARD = (Method.POST, "forward")
    REPORT_ERROR=(Method.POST,"reporterror")


class Executor(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = "http://{0}:{1}".format(host, port)
        #self.platform_client = RemoteConnection(url, keep_alive=True)

    def _check_response(self, response):
        """
            平台正确与否通过errorcode来体现，0表示正确
        :param response:
        :return:
        """
        if not response:
            raise WeTestPlatormError("None response")

        if isinstance(response, bool):
            return response

        if not isinstance(response, dict):
            invaild_response = "Invaild response : {0}".format(response)
            raise WeTestPlatormError(invaild_response)

        error_code = response.get("result", 0)
        if error_code == 0:
            return response.get("data", True)  # 如果没有数据，还是会返回，只是不再会有data数据
        else:
            errorMessage = response.get("errorMsg", "platorm api error")
            raise WeTestPlatormError(errorMessage)

    def excute_platform(self, command, params=None):
        """
            如果返回的errorcode为0，没有"data"则返回True，如果data中有数据则返回
        :param command:
        :param params:
        :return:
        """
        platform_client = RemoteConnection(self.url, keep_alive=False)
        start_time = time.time()
        if not isinstance(command, tuple):
            raise WeTestInvaildArg("command is invaild")

        if command[0] == Method.GET:
            response = platform_client.get(command[1], params)
        else:
            response = platform_client.post(command[1], params)
        end_time = time.time()
        logger.debug("Command: {0} Response: {1} time: {2}s".format(command, response, (end_time - start_time)))
        response = self._check_response(response)
        return response

    def get_top_package_activity(self):
        return self.excute_platform(Command.CURRENT_PACKAGE_NAME)

    def get_display_size(self):
        return self.excute_platform(Command.RESOLUTION)

    def get_android_version(self):
        return self.excute_platform(Command.ANDROIDVERSION)

    def get_android_model(self):
        return self.excute_platform(Command.MODEL)

    def get_rotation(self):
        return self.excute_platform(Command.GET_ROTATION)

    def clear_app_data(self, pkgname):
        return self.excute_platform(Command.CLEAR_APP_DATA, {"clearPkgName": pkgname})

    def launch_app(self, pkgname, activity="android.intent.category.LAUNCHER"):
        return self.excute_platform(Command.LAUNCH_APP, {"pkgName": pkgname, "activity": activity})

    def take_screenshot(self):
        return self.excute_platform(Command.CAPTURE)

    def touch_capture(self, width, height, x, y, name="wetest"):
        return self.excute_platform(Command.TOUCH_CAPTURE,
                                    {"name": name, "width": width,
                                     "height": height, "x": x, "y": y})

    def add_scene_tag(self, tag):
        return self.excute_platform(Command.SCENE_TAG, {"tagName": tag})

    def touch_screen(self, width, height, x, y):
        return self.excute_platform(Command.TOUCH, {"width": width, "height": height, "x": x, "y": y})

    def pause_uiautomator(self):
        return self.excute_platform(Command.STOP_UIAUTOMATOR)

    def resume_uiautomator(self):
        return self.excute_platform(Command.START_UIAUTOMATOR)

    def get_runtime(self):
        return self.excute_platform(Command.GET_TEST_TIME)

    def platform_forward(self, remote_port):
        response = self.excute_platform(Command.FORWARD, {"remotePort": remote_port})
        return response

    def report_error(self,message):
        return self.excute_platform(Command.REPORT_ERROR,{"errmsg":message})


def get_platform_client():
    if get_platform_client.instance:
        return get_platform_client.instance
    platform_ip = os.environ.get("PLATFORM_IP", "127.0.0.1")
    platform_port = os.environ.get("PLATFORM_PORT", "40030")
    get_platform_client.instance = Executor(platform_ip, platform_port)
    return get_platform_client.instance


get_platform_client.instance = None
