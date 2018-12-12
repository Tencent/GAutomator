# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import traceback
import time
import threading
import logging
import wpyscripts.manager as manager

logger = logging.getLogger("wetest")


def screensnap_thread(report, stop, times, interval):
    logger.info("time_snap Start")
    for i in range(times):
        if stop.is_set():
            logger.debug("end")
            return
        try:
            logger.debug("auto screen shot")
            report.screenshot()
            stop.wait(interval)
        except:
            stack = traceback.format_exc()
            logger.warn(stack)


class time_snap(object):
    def __init__(self, interval=10, times=30):
        self.times = times
        self.interval = interval
        self.report = manager.get_reporter()
        self.snap_thread = None

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            stop = threading.Event()
            try:
                self.snap_thread = threading.Thread(target=screensnap_thread,
                                                    args=(self.report, stop, self.times, self.interval))
                self.snap_thread.start()
                fn(*args, **kwargs)
            except:
                stack = traceback.format_exc()
                logger.warn(stack)
            finally:
                stop.set()

        return wrapped
