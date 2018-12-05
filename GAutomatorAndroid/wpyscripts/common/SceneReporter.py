# -*- coding: UTF-8 -*-
import logging
import WeTestApi
import os
import json
from wpyscripts.common import Singleton
import time
import inspect
import traceback
import subprocess
logger = logging.getLogger("wetest")


@Singleton.singleton
class SceneReporter:
    cur_tag="unknown"
    separator1 = '=' * 70
    separator2 = '-' * 70
    errs=[]

    def get_device_time(self):  
        device_time = None
        try:
            timeout = 3
            start = time.time()
            process = subprocess.Popen('adb shell date ',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while process.poll() is None:
                time.sleep(0.2)
                if (time.time() - start) > timeout:
                    os.kill(process.pid, 9)
                    return None
            device_time_str = process.stdout.read().strip()
            logger.info(device_time_str)
            # 转为时间数组
            device_time_transed = device_time_str.split()
            device_time_str = "" + device_time_transed[1] + " " + device_time_transed[2] + " " + device_time_transed[
                3] + " " + device_time_transed[5]
            print(device_time_str)
            timeArray = time.strptime(device_time_str, '%b %d %H:%M:%S %Y')
            # 转为时间戳
            timeStamp = long(time.mktime(timeArray))
            device_time = long(timeStamp * 1000)
            logger.info("device time: " + str(device_time))
        except Exception, e:
            logger.exception(e)
        return device_time

    def reportCurScene(self,tag):
        try:
            if os.environ.get("REPORTURL")==None:
                logger.info("report url is none ,do not report scene ")
                return
            logger.info("report scene :"+tag)
            device_time=self.get_device_time()
            if device_time==None:
                device_time=int(time.time())
            client = WeTestApi.WeTestApi(WeTestApi.authparams, os.environ.get("REPORTURL"))
            resp = client.add_scene_tag(int(os.environ.get("TESTID")), int(os.environ.get("DEVICEID")), tag,device_time)
            logger.info(json.dumps(resp))
            self.cur_tag=tag
        except Exception, e:
            logger.exception(e)


    def reportSceneError(self,title,errorfile):
        # 上报脚本错误
        if os.environ.get("REPORTURL")==None:
            logger.info("report url is none ,do not report scene error")
            return
        logger.info("reportSceneError :" + title +"errorfile : "+errorfile)
        client = WeTestApi.WeTestApi(WeTestApi.authparams, os.environ.get("REPORTURL"))

        device_time=self.get_device_time()
        if device_time==None:
            device_time=int(time.time())
        resp = client.upload_script_error(int(os.environ.get("TESTID")), int(os.environ.get("DEVICEID")), self.cur_tag, title, errorfile,device_time)
        logger.info(json.dumps(resp))

    def reportAtEnd(self):
        self.reportCurScene("")
        self._reportTotalTestCaseResult()


if __name__ == '__main__':
    reporter =SceneReporter()
    print(reporter.get_device_time())