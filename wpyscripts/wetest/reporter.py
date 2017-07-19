# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

    与平台相关的内容，使用之后会集中反映在测试报告之中

    1、性能数据获取
    2、性能数据打标签
    3、QQ登陆
"""

__author__ = 'minhuaxu wukenaihesos@gmail.com'
import time
import traceback
import logging
import os
import inspect

from wpyscripts.common.adb_process import excute_adb
from wpyscripts.common.wetest_exceptions import *

import wpyscripts.common.platform_helper as platform

logger = logging.getLogger("wetest")


class Reporter(object):

    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self):
        self.errs=[]

    def add_start_scene_tag(self, scene):
        """
            云测时会在测试报告的性能数据上打上开始标签，便于区分。本地时不起作用
        :param scene:标签名称
        :return:
        """
        logger.warn("add_start_scene_tag unimplement,implemented in cloud mode")

    def add_end_scene_tag(self, scene):
        """
            云测时会在测试报告的性能数据上打上结束标签，便于区分。本地时不起作用。报告上会标记开始和结束的内容
        :param scene:标签名称
        :return:
        """
        logger.warn("add_end_scene_tag unimplement,implemented in cloud mode")

    def capture_and_mark(self, x, y, locator_name=None):
        """
            在云测时，会对手机界面截图并在截图上标记。
            应该配合touch一起使用，在使用该方法后再进行touch操作。这样能够保证标记点击位置
            usage:
                platorm.capture_and_mark(10,23)
                device.touch(10,23)
        :param x:屏幕的x坐标
        :param y:屏幕的y坐标
        :return:
        """
        logger.warn("capture_and_mark unimplement,implemented in cloud mode")

    def screenshot(self):
        """
        截图
        :return:
        """
        logger.warn("capture_and_mark unimplement,implemented in cloud mode")

    def _report_total(self):
        if not self.errs:
            return

        result_dir=os.environ.get("UPLOADDIR",".")
        try:
            with open(os.path.abspath(os.path.join(result_dir, "_wetest_testcase_result.txt")), 'w') as f:
                for testcase_name,message in self.errs:
                    if message:
                        result=u"{0} ... ERROR\n".format(testcase_name)
                    else:
                        result=u"{0} ... ok\n".format(testcase_name)
                    f.write(result.encode("utf-8"))
                for testcase_name,message in self.errs:
                    if message:
                        result=u"{0}\nERROR: {1}\n{2}\n{3}\n\n".format(self.separator1,testcase_name,self.separator2,message)
                        f.write(result.encode("utf-8"))
        except Exception as e:
            stack=traceback.format_exc()
            logger.error(stack)

    def report(self,result,test_case_name, message=""):
        """
            错误信息判断报告。调用的过程中，会在日志中输出。脚本运行结束时，runner.run中，会调用
            _report_total(),将所有的判断结果输出到_wetest_testcase_result.txt中。如果result为false，断言错误时，除了输出message和test_case_name之外
            GAutomator还会加上调用堆栈

            注：test_case_name与message的编码方式应该一致，都是ascii或者utf-8.如果包含中文需要用UTF-8编码
        :param result:报告的内容是否有误,True,False
        :param test_case_name:报告错误的名称（尽可能简短）
        :param message:具体的信息。

        :Usage:
            >>>import wpyscripts.manager as manager
            >>>report.report(True,"testName","test first content")

            >>>report.report("a"=="b",u"test中文",u"测试中文内容")
        :return:
        """
        curframe=inspect.currentframe()
        calframe=inspect.getouterframes(curframe,2)
        test_case_name=u"{0} ({1})".format(test_case_name,calframe[1][3])
        if not result:
            stack="".join(traceback.format_stack())
            stack=unicode(stack,"utf-8")
            _message=u"{0}{1}\n".format(stack,message)
            message_log=u"\n{0}\nERROR: {1}\n{2}\n{3}".format(self.separator1,test_case_name,self.separator2,_message)
        else:
            _message=None
            message_log=u"\n{0} ... ok".format(test_case_name)

        self.errs.append((test_case_name,_message))
        logger.warn(message_log)



class CloudReporter(Reporter):
    def __init__(self):
        Reporter.__init__(self)
        self.scene_tag = None
        self.platform_client = platform.get_platform_client()
        self.image_id = 10000  # 脚本的截图的Image id从10000外开始

    def _scene_tag(self, tag):
        try:
            self.platform_client.add_scene_tag(tag)
            return True
        except:
            stack = traceback.format_exc()
            logger.error(stack)
            return False

    def add_start_scene_tag(self, scene):
        """
            云测时会在测试报告的性能数据上打上开始标签，便于区分。本地时不起作用
        :param scene:标签名称
        :return:
        """
        if scene and isinstance(scene, str):
            if self.scene_tag is not None:
                reason = "{0} tag is still not end,you can not start a new scene tag".format(self.scene_tag)
                raise SceneTagError(reason)
            result = self._scene_tag(scene)
            if result:
                self.scene_tag = scene
                return True
            else:
                return False

        else:
            raise WeTestInvaildArg("scene tag can't be None")

    def add_end_scene_tag(self, scene):
        """
            云测时会在测试报告的性能数据上打上结束标签，便于区分。本地时不起作用。报告上会标记开始和结束的内容
        :param scene:标签名称
        :return:
        """
        if scene and isinstance(scene, str):
            if self.scene_tag != scene:
                reason = "no start tag {0},you can not add a end scene tag".format(scene)
                raise SceneTagError(reason)
            result = self._scene_tag(scene)
            if result:
                self.scene_tag = None
                return True
            else:
                return False
        else:
            raise WeTestInvaildArg("scene tag can't be None")

    def _get_display_size(self):
        """
        设计的不太合理，capture and mark不应该脚本请求时附带屏幕的宽高
        :return:
        """
        response = self.platform_client.get_display_size()
        return response["width"], response["height"]

    def capture_and_mark(self, x, y, locator_name="point"):
        """
            在云测时，会对手机界面截图并在截图上标记。
            应该配合touch一起使用，在使用该方法后再进行touch操作。这样能够保证标记点击位置
            usage:
                platorm.capture_and_mark(10,23)
                device.touch(10,23)
        :param x:屏幕的x坐标
        :param y:屏幕的y坐标
        :return:
        """
        try:
            self.image_id += 1
            width, height = self._get_display_size()
            response = self.platform_client.touch_capture(width, height, x, y, locator_name)
            if response:
                return response
        except:
            stack = traceback.format_exc()
            logger.error(stack)

    def screenshot(self):
        """
            截图
        :return:
        """
        try:
            self.image_id += 1
            response = self.platform_client.take_screenshot()
            if response:
                return response
        except:
            stack = traceback.format_exc()
            logger.error(stack)


class NativeReporter(Reporter):
    def __init__(self):
        Reporter.__init__(self)
        # <GA>/../screenshot/
        self.currentpath = os.path.abspath(__file__)
        self.targetpath = os.path.join(os.path.dirname(self.currentpath), "..","..","..","screenshot")
        if not os.path.isdir(self.targetpath):
            os.makedirs(self.targetpath)

    def screenshot(self):
        name = time.time()
        cap = "adb shell /system/bin/screencap -p /data/local/tmp/{0}.png".format(name)
        pull = "adb pull /data/local/tmp/{0}.png {1}/{0}.png".format(name,self.targetpath)
        clear = "adb shell rm /data/local/tmp/{0}.png".format(name)
        os.system(cap)
        os.system(pull)
        os.system(clear)
        logger.debug('capture screen and save to file:{0}'.format(name))

    def capture_and_mark(self, x, y, locator_name="point"):
        locator_name = locator_name if locator_name else "point"
        locator_name = self._escape_path(locator_name)

        cap = "adb shell /system/bin/screencap -p /data/local/tmp/{0}.png".format(locator_name)
        pull = "adb pull /data/local/tmp/{0}.png {1}/{0}.png".format(locator_name,self.targetpath)
        clear = "adb shell rm /data/local/tmp/{0}.png".format(locator_name)
        os.system(cap)
        os.system(pull)
        os.system(clear)
        logger.debug('capture screen and save to file:{0}'.format(locator_name))
        return locator_name

    def _escape_path(self, pathstr):
        pathstr = pathstr.lstrip("/\\")     # remove leading / and \
        pathstr = pathstr.replace("/", "_")
        pathstr = pathstr.replace("\\", "_")

        return pathstr
