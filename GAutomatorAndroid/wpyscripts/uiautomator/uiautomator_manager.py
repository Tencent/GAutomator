#-*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'
import six
import sys
if six.PY2:
    reload(sys)
    sys.setdefaultencoding("utf-8")
import atexit
from libs.uiauto.uiautomator import AutomatorDevice
from wpyscripts.common.adb_process import *

logger=logging.getLogger("wetest")

_device_port=9008
_uiautomator_port = os.environ.get("UIAUTOMATOR_PORT","19008")


def restartPlatformDialogHandler():
    try:
        kill_uiautomator()
        time.sleep(8)  # wait for platform to relaunch uiautomator
        get_uiautomator().setdialogtextpattern(
            u'(^(完成|关闭|好|好的|确定|确认|安装|下次再说|暂不删除)$|(.*(?<!不|否)(忽略|允(\s)?许|同意)|继续|稍后|暂不|下一步).*)')
        get_uiautomator().setdialogtextgrouppattern(
            u'((建议.*清理)|是否卸载|卸载后)&&&(取消|以后再说|下载再说);是否发送错误报告&&&否;为了给您提供丰富的图书资源&&&取消;简化备份恢复流程&&&(以后再说|下次再说)')
        pkgfilter = ""
        if os.environ.get('PKGNAME'):
            pkgfilter = u'(?=(^(?!' + os.environ.get("PKGNAME") + u"$)))"
            get_uiautomator().setdialogpkgpattern(
            pkgfilter + u'^(?!(com.tencent.mm|com.tencent.mqq|com.tencent.mobileqq)$).*')
            get_uiautomator().setPermissionMonitor(True)
        time.sleep(1)
    except Exception as e:
        logger.exception(e)

def write_dialog_config(config_path):
    if os.environ.get("PKGNAME") is None:
        return
    content=""
    # with open(config_path,"r") as f:
    #     content=f.read()

    textpattern=u'(^(完成|关闭|好|好的|确定|确认|安装|下次再说|暂不删除)$|(.*(?<!不|否)(忽略|允(\s)?许|同意)|继续|稍后|暂不|下一步).*)'
    textGroupPattern=u'((建议.*清理)|是否卸载|卸载后)&&&(取消|以后再说|下载再说);是否发送错误报告&&&否;为了给您提供丰富的图书资源&&&取消;简化备份恢复流程&&&(以后再说|下次再说)'
    pkgfilter=""
    if os.environ.get('PKGNAME'):
        pkgfilter = u'(?=(^(?!' + os.environ.get("PKGNAME") + u"$)))"
    pkgattern =pkgfilter + u'^(?!(com.tencent.mm|com.tencent.mqq|com.tencent.mobileqq)$).*'
    content += "textpattern=" + textpattern + "\n"
    content += "textGroupPattern=" + textGroupPattern + "\n"
    content += "pkgattern=" + pkgattern +"\n"
    content += "needDialogHandler=true" +"\n"

    with open(config_path, "w") as f:
        f.write(content)

def init_uiautomator_with_dialoghandler():
    """
        初始化uiautomator
    :return:
    """
    file_path = os.path.split(os.path.realpath(__file__))[0]
    uiautomator_stub_path = os.path.abspath(
        os.path.join(file_path,"..","third","libs","uiAutomator","DialogHandler_polling.jar"))
    #adb=AdbTool()
    config_path= os.path.abspath(
        os.path.join(file_path,"..","third","libs","uiAutomator","wetest_dialog_config.properties"))
    write_dialog_config(config_path)
    ret = excute_adb_process("push {0} /data/local/tmp".format(uiautomator_stub_path))
    if "no devices/emulators found" in ret or "device offline" in ret:
        return None
    excute_adb_process("push {0} /data/local/tmp".format(config_path))
    excute_adb_process("shell am force-stop com.tencent.wetest.rc.rc_uiautomatorstub")
    kill_uiautomator()
    logger.debug("Start UIAutomator")
    #os.system("adb shell ps")
    remove_forward(_uiautomator_port)
    forward(_uiautomator_port, _device_port)
    uiautomator_process = excute_adb_process_daemon("shell uiautomator runtest DialogHandler_polling.jar -c com.github.uiautomatorstub.Stub",shell=True ,needStdout=False)
 #   uiautomator_process = excute_adb_process_daemon("shell uiautomator runtest DialogHandler.jar -c com.github.uiautomatorstub.Stub", shell=True)
    #call_adb_shell("adb forward tcp:{0} tcp:{1} && adb shell uiautomator runtest uiautomator_stand_stub.jar -c com.github.uiautomatorstub.Stub".format(_uiautomator_port,_device_port))
    # call_adb_shell(["shell","uiautomator","runtest","/data/local/tmp/uiautomator_stand_stub.jar","-c","com.github.uiautomatorstub.Stub","--nohup"])#--nohup
    time.sleep(2)

   # os.system("adb shell ps")

def init_uiautomator():
    """
        初始化uiautomator
    :return:
    """
    kill_uiautomator()
    file_path = os.path.split(os.path.realpath(__file__))[0]
    uiautomator_stub_path = os.path.abspath(
        os.path.join(file_path, "..","third","libs","uiAutomator","uiautomator-stub.jar"))
    # adb=AdbTool()
    logger.debug(excute_adb_process("push " + uiautomator_stub_path + " /data/local/tmp"))
    remove_forward(_uiautomator_port)
    forward(_uiautomator_port,_device_port)
    logger.debug("Start UIAutomator")
    uiautomator_process = excute_adb_process_daemon("shell uiautomator runtest uiautomator-stub.jar -c com.github.uiautomatorstub.Stub", shell=True )
    time.sleep(2)


def _init():
    port = os.environ.get("UIAUTOMATORPORT")
    if port:
        return int(port)
    else:
        """
            本地，初始化UiAutomator
        """
        init_uiautomator()
       #  init_uiautomator_with_dialoghandler()
        atexit.register(kill_uiautomator)
        return int(_uiautomator_port)

def get_uiautomator():
    if get_uiautomator.instance:
        return get_uiautomator.instance
    else:
        port=_init()
        get_uiautomator.instance = AutomatorDevice(None, port, os.environ.get("PLATFORM_IP", "127.0.0.1"), None)
        return get_uiautomator.instance

get_uiautomator.instance=None
