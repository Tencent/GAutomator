"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

__author__ = 'yifengcai'

from wpyscripts import manager
from wpyscripts.tools.traverse.layerelem import TouchElem, ViewLayer

from __libs.util import MobileDevice


device = manager.get_device()
engine = manager.get_engine()
d = MobileDevice().get_dev()

def print_display_size():
    display_size = device.get_display_size()
    width, height = display_size.width, display_size.height
    print("screen size is: %d, %d" % (width, height))

def print_game_activity():
    package_activity = device.get_top_package_activity()
    print("Game package and activity is (%s, %s)" % (package_activity.package_name, package_activity.activity))

def print_current_layer():
    elements = engine.get_touchable_elements()
    scene_name = engine.get_scene()
    
    curr_layer = ViewLayer()
    for e, _ in elements:
        te = TouchElem(scene_name, e)
        curr_layer.add_element(te)
    curr_layer.sort_elems_by_name()
    
    print("current layer: %s" % curr_layer.fullstr())


def print_uiauto_xml():
    info = d.info
    print(info)


if __name__ == "__main__":
#     print_display_size()
#     print_game_activity()
#     print_current_layer()
    
    print_uiauto_xml()

