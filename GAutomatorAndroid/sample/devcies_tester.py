# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import sys, os, time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

import wpyscripts.manager as manager

engine = manager.get_engine()
logger = manager.get_logger()
device = manager.get_device()


def test_get_display_size():
    display_size = device.get_display_size()
    logger.debug(display_size)

    rotation = device.get_rotation()
    logger.debug("Rotation : {0}".format(rotation))


def test_get_top_package_activity():
    top_activity = device.get_top_package_activity()
    logger.debug(top_activity)


def test_back():
    device.back()

# def test_multitouch():
#     device.touchDown(0,pt[0],pt[1])
#     device.touchDown(1, pt2_start[0], pt2_start[1])
#     device.touchMove(0, pt[0]+50,pt[1]+50)
#     device.touchMove(1, pt2_end[0], pt2_end[1])
#     time.sleep(5)
#     device.touchUp(0)
#     device.touchUp(1)


test_get_display_size()
test_get_top_package_activity()