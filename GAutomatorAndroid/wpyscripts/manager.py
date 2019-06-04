# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

    PLATFORM_IP，判断是云端（CLOUD）、本地运行

    对用户来说，只需要通过manmager获取的device,platorm和engine进行操作即可。如果是云端的则可以直接在云平台上运行
"""

__author__ = 'minhuaxu wukenaihesos@gmail.com'

import logging

from wpyscripts.wetest.device import *
from wpyscripts.wetest.engine import *
from wpyscripts.wetest.reporter import *
from wpyscripts.common.wetest_exceptions import *
import wpyscripts.common.adb_process as adb
import wpyscripts.common.platform_helper as platform
from config import Engine,EngineType
from wpyscripts.common.utils import screensnap_thread
import wpyscripts.uiautomator.uiautomator_manager as uiauto

env = os.environ.get("PLATFORM_IP")
hostip = os.environ.get("PLATFORM_IP", "127.0.0.1")
platform_port = os.environ.get("PLATFORM_PORT")

_local_mode = None

_local_engine_port = os.environ.get("LOCAL_ENGINE_PORT", "53001")  # 本地模式时与engine forward的端口号


_uiautomator_port = "19008"

_engine_address = None
_platorm_address = None
_test_id = None
_package_name = None

_uiautomator_inited = False

logger = logging.getLogger(__name__)


def get_device():
    """
        单例，多次获取的是同一个实例对象
        根据运行在本地还是wetest云端，创建不同的实现。在本地运行创建NativeDevice实现类，在wetest平台创建CloudDevice。

        创建Device类的时候，首先会启动UIAutomator服务（https://github.com/xiaocong/uiautomator）
    :return: Device实例
    """
    if get_device.instance:
        return get_device.instance

    ui_device = uiauto.get_uiautomator()
    pkgname = os.environ.get("PKGNAME")
    launch_activity = os.environ.get("LAUNCHACTIVITY", None)
    serial = os.environ.get("ANDROID_SERIAL")
    if not serial:
        serial = os.environ.get("ADB_SERIAL")

    if env:
        get_device.instance = CloudDevice(serial, pkgname, launch_activity, ui_device)
    else:
        get_device.instance = NativeDevice(serial, ui_device)
    return get_device.instance


get_device.instance = None


def _platform_forward(remote_port):
    """
        在wetest平台运行时，forward映射的端口交由平台分配并且实现映射
    :param remote_port:
    :return:
    """
    platform_client = platform.get_platform_client()
    response = platform_client.platform_forward(remote_port)
    return response["localPort"]


def get_engine(engine_type=EngineType, port=None):
    """
        singleton instance , get the instance of GameEngine 。(only support unity or ue4 for now)
    :param engine_type:
    :param port: sdk forward port . if not set, the port will be set by Environment Variables
    :return: GameEngine instance
    """
    if get_engine.instance:
        return get_engine.instance
    local_port = None
    if env:
        result = _platform_forward(int(unity_sdk_port))
        local_port = result
    else:
        local_engine_port = os.environ.get("LOCAL_ENGINE_PORT", "53001")  # 本地模式时与engine forward的端口号
        res = forward(local_engine_port, unity_sdk_port)
        logger.info(res)
        local_port = int(local_engine_port)
    logger.info("host: {0} port: {1}".format(hostip, local_port))

    ui_device = uiauto.get_uiautomator()
    if engine_type == "unity":
        get_engine.instance = UnityEngine(hostip, local_port,ui_device)
    elif engine_type == "ue4":
        get_engine.instance=UnRealEngine(hostip,local_port,ui_device)
    else:
        raise ValueError("No {0} engine type".format(engine_type))
    return get_engine.instance
get_engine.instance = None

def get_reporter():
    """
        单例，获取Report实例对象.本地运行均为空实现，只有在wetest平台运行时才会有相应的效果
    :return:
    """
    if get_reporter.instance:
        return get_reporter.instance
    if env:
        get_reporter.instance = CloudReporter()
        return get_reporter.instance
    else:
        return NativeReporter()


get_reporter.instance = None


def get_logger():
    if env:
        return logging.getLogger('wetest')
    else:
        return logging.getLogger('wetest')


def get_testcase_logger():
    if env:
        return logging.getLogger('testcase')
    else:
        return logging.getLogger('testcase')


class time_snap(object):
    def __init__(self, interval=10, times=30):
        self.times = times
        self.interval = interval
        self.report = get_reporter()
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
                logger.warning(stack)
            finally:
                stop.set()

        return wrapped


def save_sdk_version(version):
    """
        收集现有版本使用情况，可以针对性的去除你不想被我们收集的数据。
    :param version: SDK版本
    :return:
    """
    try:
        import urllib
        import socket
        import hashlib
        url = "http://wetest.qq.com/cloudapi/api_v2/gautomator"
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        pkg = os.environ["PKGNAME"]

        # 只收集SDK版本情况，游戏包名MD5加密不可逆向
        hash_pkg = hashlib.md5(pkg.encode("utf-8"))
        hash_pkg = hash_pkg.hexdigest()
        script_version = "3.0.0"
        version_info = ""
        if version:
            version_info = str(version)
        values = {"pkg": hash_pkg, "ip": ip_address, "name": hostname, "scriptversion": script_version,
                  "sdkversion": version_info}
        if six.PY2:
            import urllib2
            data = urllib.urlencode(values)
            f = urllib2.urlopen(url, data)
        else:
            data = urllib.parse.urlencode(values)
            f = urllib.request.urlopen(url, data.encode("utf-8"))
        print(f.read())
    except:
        traceback.print_exc()
