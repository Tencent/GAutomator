# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import wpyscripts.tools.traverse.travel as travel
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

def test_travel():
    forbid_names = [
        "/ViewUIDepth_2/Canvas/ManagerInformation/Panel/JumpWindow/RightPanel/Wanjiaxinxi/ChangeServerButton",
        "/ViewUIDepth_2/Canvas/ManagerInformation/Panel/JumpWindow/RightPanel/Wanjiaxinxi/LoginOutButton"]
    travel.explore(forbid_names=forbid_names, mode=0, max_num=30)


test_travel()
