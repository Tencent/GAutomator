# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

    GAutomator底层框架
"""
version_info = (2, 6, 0)
version = '2.6.0'
release = '2.6.0'

__version__ = release  # PEP 396
__author__='minhuaxu wukenaihesos@gmail.com,alexkan kanchuanqi@gmail.com,yifengcai'


import logging,os
LOG_FILE = 'python_log.log'


def makesure_dir_exist(path):
    existed=os.path.exists(path)
    if existed:
        return True
    else:
        os.mkdir(path)



handler = logging.StreamHandler()
fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter

logger = logging.getLogger()    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler

log_dir=os.environ.get("UPLOADDIR")
file_path = os.path.split(os.path.realpath(__file__))[0]
if log_dir:
    file_path=os.path.abspath(os.path.join(log_dir,"python_log.log"))
else:
    log_name="../../python_log_{0}.log".format(os.environ.get("ADB_SERIAL",""))
    file_path=os.path.abspath(os.path.join(file_path,log_name))
file_handler=logging.FileHandler(file_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)