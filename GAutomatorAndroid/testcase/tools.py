# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

from config import Engine,EngineType

from wpyscripts.tools.basic_operator import engine
from wpyscripts.tools.basic_operator import device
from wpyscripts.tools.basic_operator import report
from wpyscripts.tools.basic_operator import screen_shot_click,screen_shot_click_pos
from wpyscripts.tools.basic_operator import screen_shot_click


if EngineType == Engine.UE4:
    from wpyscripts.tools.ue_engine_api import *
elif EngineType == Engine.Unity:
    from wpyscripts.tools.unity_engine_api import *
