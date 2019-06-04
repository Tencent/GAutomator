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
from ga2.cloud.httptools.remote_connection import RemoteConnection, Method
from ga2.common.wetest_exceptions import WeTestPlatormError,WeTestInvaildArg


logger = logging.getLogger(__name__)


class Command(object):

    TOUCH_CAPTURE = (Method.POST, "touchcapture")
    CAPTURE = (Method.POST, "snapshot")
    # GET_SCREEN_IMAGE = (Method.GET, "screenimage")
    FORWARD = (Method.POST, "forward")
    RESTORE_WDA = (Method.POST, "restorewda")

class Executor(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = "http://{0}:{1}".format(host, port)
        #self.platform_client = RemoteConnection(url, keep_alive=True)

    def _check_response(self, response):
        """
            errorcode==0 means success
            :param response:
            :return the data in response:
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
        :param command:
        :param params:
        :return if errorcode is 0, return the data or True if data is None :
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

        if response and isinstance(response,dict) and "data" in response:
            if "imageData" in response["data"]:
                response = self._check_response(response)
                return response
        logger.debug("Command: {0} Response: {1} time: {2}s".format(command, response, (end_time - start_time)))
        response = self._check_response(response)
        return response

    def take_screenshot(self):
        return self.excute_platform(Command.CAPTURE)

    def restore_wda(self, port):
        return self.excute_platform(Command.RESTORE_WDA, {"port":port})

    def touch_capture(self, width, height, x, y, name="wetest"):
        return self.excute_platform(Command.TOUCH_CAPTURE,
                                    {"name": name, "width": width,
                                     "height": height, "x": x, "y": y})

    # def get_screenimage(self):
    #     return self.excute_platform(Command.GET_SCREEN_IMAGE)

    def platform_forward(self, remote_port):
        return self.excute_platform(Command.FORWARD,{"remotePort": remote_port})

def get_platform_client():
    if get_platform_client.instance:
        return get_platform_client.instance
    platform_ip = os.environ.get("PLATFORM_IP", "127.0.0.1")
    platform_port = os.environ.get("PLATFORM_PORT", "40030")
    get_platform_client.instance = Executor(platform_ip, platform_port)
    return get_platform_client.instance


get_platform_client.instance = None
