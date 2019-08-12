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
            logger.warning(stack)


def retry_if_fail(retry_times = 3, total_seconds = 60 ):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            for i in range(0,retry_times):
                if not ret and ret != 0:
                    logger.error("retry_if_fail detect failing, wait and retry...")
                    time.sleep(total_seconds/retry_times)
                    ret = func(*args, **kwargs)
                else:
                    return ret
            if not ret:
                logger.error("still fail after retry")
        return inner_wrapper

    return wrapper
