# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import os
from wpyscripts.tools.baisc_operater import *
import wpyscripts.tools.traverse.travel as travel

logger = manager.get_testcase_logger()


# 帮助文档及内容
# ==========================QQ登陆过程示例================================================
# def login_qq():
#     """
#         腾讯系游戏，通过QQ登陆
#
#         从拉起游戏出现QQ和微信登陆按钮--->QQ账号密码输入登陆-->登陆完成
#     :return:
#     """
#     tencent_login(scene_name="EmptyScene",login_button="/BootObj/CUIManager/Form_Login/LoginContainer/pnlMobileLogin/btnGroup/btnQQ",sleeptime=3)


# ==========================随机遍历过程================================================
# forbid_names = ["/ViewUIDepth_2/Canvas/ManagerInformation/Panel/JumpWindow/RightPanel/Wanjiaxinxi/ChangeServerButton",
#                 "/ViewUIDepth_2/Canvas/ManagerInformation/Panel/JumpWindow/RightPanel/Wanjiaxinxi/LoginOutButton"]
def random_search_test():
    log_dir = os.environ.get("UPLOADDIR")
    if log_dir:
        log_dir = os.path.join(log_dir, "policy.log")
    else:
        log_dir = "policy.log"
    logger.info("run random search in testcase runner")
    travel.explore(log_dir, [], mode=0, max_num=3000)


def run():
    """
        业务逻辑的起点
    """
    try:
        # random_search_test()
        # import testcase.sample as sample
        # sample.main()
        pass
    except Exception as e:
        traceback.print_exc()
        stack = traceback.format_exc()
        logger.error(stack)
        report.report(False,"Game Test",e.message)
    finally:
        report._report_total()
        report.screenshot()
