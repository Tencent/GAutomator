# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

__author__ = 'minhuaxu wukenaihesos@gmail.com'

import unittest, math, time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..\\..\\")))

from wpyscripts.manager import *

logger = logging.getLogger("wetest")


def scene_enter(button, *args, **kwargs):
    def real_decorator(fun):
        def wrapped(*args, **kwargs):
            engine = get_engine()
            enter = engine.find_element(button)
            engine.click(enter)
            time.sleep(2)
            fun(*args, **kwargs)
            time.sleep(2)
            back = engine.find_element("Back")
            engine.click(back)
            time.sleep(4)

        return wrapped

    return real_decorator


class GameEngineTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameEngineTest, self).__init__(*args, **kwargs)
        self.start_time = None
        self.ui_type = "UGUI"

    def setUp(self):
        self.engine = get_engine()


    @classmethod
    def setUpClass(cls):
        cls.timeuse = []

    @classmethod
    def tearDownClass(cls):
        for item in cls.timeuse:
            print("{0},{1}".format(item["name"], item["use"]))

        engine=get_engine()

    # def test_test(self):
    #     button=self.engine.find_element("QQ")
    #     bound=self.engine.get_element_bound(button)
    #     self.engine.click(button)
    #     logger.debug("{0}".format(bound.__str__()))

    def _start(self):
        self.start_time = time.time()

    def _end(self, name):
        diff = time.time() - self.start_time
        GameEngineTest.timeuse.append({"use": diff * 1000, "name": name})

    def test_get_sdk_version(self):
        self._start()
        sdk_info = self.engine.get_sdk_version()
        self._end("get_sdk_version")
        self.ui_type = sdk_info.ui_type
        logger.info(sdk_info)
        # self.assertTrue(cmp(sdk_info.engine_version, "5.1.2f1") == 0, "engine version Error")
        self.assertTrue(cmp(sdk_info.engine, "Unity3D") == 0, "engine Error")
        self.assertTrue(sdk_info.sdk_version == "1.5.0", "sdkversion Error")

    def test_find_element(self):
        self._start()
        element = self.engine.find_element("Sample")
        self._end("find_element")
        logger.debug(element)

    def test_find_elments_by_components(self):
        self._start()
        elements = self.engine.find_elements_by_component("CustomTester")
        self.assertTrue(len(elements) == 1, "Find error")
        self._end("find_elements_by_component")

    def test_get_element_bound(self):
        element = self.engine.find_element("Sample")
        self._start()
        bound = self.engine.get_element_bound(element)
        self._end("get_element_bound")

        logger.info(bound)

    def test_click_position(self):
        element = self.engine.find_element("Sample")
        bound = self.engine.get_element_bound(element)
        self._start()
        result = self.engine.click_position(bound.x + bound.width / 2, bound.y + bound.height / 2)
        self._end("click_position")

        self.assertTrue(result, "Click Error")

    def test_click(self):
        element = self.engine.find_element("Sample")
        self._start()
        result = self.engine.click(element)
        self._end("click")
        # self.assertTrue(result,"Click Element error")

        time.sleep(4)
        element = self.engine.find_element("Sample")
        bound = self.engine.get_element_bound(element)
        result = self.engine.click(bound)
        # self.assertTrue(result,"Click ElementBound error")

    @scene_enter("Interaction")
    def test_press(self):
        # 按压节点
        element = self.engine.find_element("Press")
        self._start()
        result = self.engine.press(element, 2000)
        self._end("press 2000ms")
        self.assertTrue(result)

        # 按压ElementBound
        bound = self.engine.get_element_bound(element)
        result = self.engine.press(bound, 3000)
        self.assertTrue(result)

    @scene_enter("Interaction")
    def test_swipe(self):
        start_element = self.engine.find_element("Press")
        end_element = self.engine.find_element("Click")

        # 根据元素按压
        result = self.engine.swipe(start_element, end_element, 100)
        self.assertTrue(result)

        # 根据位置按压
        start_bound = self.engine.get_element_bound(start_element)
        end_bound = self.engine.get_element_bound(end_element)
        self._start()
        result = self.engine.swipe_position(start_bound.x, start_bound.y, end_bound.x, end_bound.y, 500, 2000)
        self._end("swipe_position 2000ms")

        result = self.engine.swipe(start_bound, end_bound, 500, 2000)

    @scene_enter("FindElements")
    def test_get_touchable_element(self):
        self._start()
        elements = self.engine.get_touchable_elements()
        self._end("get_touchable_element")
        self.assertEqual(len(elements), 9)

        self._start()
        elements = self.engine.get_touchable_elements(["LuaButton, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null",
                                                       "UISprite, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null"])
        self._end("get_touchable_element")
        self.assertEqual(len(elements), 9)

    @scene_enter("FindElements")
    def test_get_touchable_element_bound(self):
        self._start()
        scene, elements = self.engine.get_touchable_elements_bound()
        self._end("get_touchable_elements_bound")
        self.assertEqual(len(elements), 9)
        self.assertEqual(scene, "FindElements")

        self._start()
        scene, elements = self.engine.get_touchable_elements_bound(["LuaButton, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null"])
        self._end("get_touchable_element")
        self.assertEqual(len(elements), 9)

    def test_get_current_scene(self):
        self._start()
        scene = self.engine.get_scene()
        self._end("get_scene")

        logger.debug("Scene:{0}".format(scene))
        self.assertEqual(scene, "main")

    @scene_enter("Interaction")
    def test_input(self):
        e = self.engine.find_element("/Canvas/Panel/InputField")
        self._start()
        old_content = self.engine.input(e, "Hello Wetest")
        self._end("input")
        self.assertEqual(old_content, "Hello wpyscripts")

        # self.assertRaises(WeTestSDKError, self.engine.get_element_text, e)

        e = self.engine.find_element("/Canvas/Panel/InputField/Text")
        str = self.engine.get_element_text(e)
        self.assertEqual(str, "Hello Wetest")

    @scene_enter("FindElements")
    def test_find_elements_path(self):
        self._start()
        elements = self.engine.find_elements_path("/Canvas/Panel/Sample")
        self._end("find_elements_path /root")
        self.assertEqual(len(elements), 0)

        self._start()
        items = self.engine.find_elements_path("Item(Clone)")
        self._end("find_elements_path all")
        self.assertEqual(len(items), 5)

        self._start()
        items = self.engine.find_elements_path("Image{img=saturn}")
        self._end("find_elements_path img")
        self.assertEqual(len(items), 1)

        self._start()
        items = self.engine.find_elements_path("Button{txt=Button}")
        self._end("find_elements_path txt")
        self.assertEqual(len(items), 2)

        self._start()
        items = self.engine.find_elements_path("/Canvas/Panel/VerticalPanel/Item(Clone)[2]")
        self._end("find_elements_path index")
        self.assertEqual(len(items), 1)

        items = self.engine.find_elements_path("VerticalPanel/Item(Clone)[2]")
        self.assertEqual(len(items), 1)

        items = self.engine.find_elements_path("Item(Clone)[2]")
        self.assertEqual(len(items), 1)

    def test_get_element_bound(self):
        element = self.engine.find_element("Sample")
        self._start()
        bound = self.engine.get_element_bound(element)
        logger.debug(bound)
        self._end("get_element_bound")
        # self.assertEqual(bound.width, 250.0)
        # self.assertEqual(bound.height, 80.0)

    def test_get_registered_handlers(self):
        self._start()
        result = self.engine.get_registered_handlers()
        self._end("get_registered_handlers")
        self.assertTrue("test" in result)

    def test_call_registered_handler(self):
        self._start()
        result = self.engine.call_registered_handler("test", "python call test")
        self._end("call_registered_handler")
        self.assertEqual("python call test Response", result)

    @scene_enter("Joystick")
    def test_get_world_bound(self):
        elements = self.engine.find_elements_path("Bip001 Pelvis")
        self._start()
        bounds = self.engine.get_element_world_bound(elements)
        self._end("get_element_world_bound")
        self.assertEqual(len(bounds), 1)

    @scene_enter("Joystick")
    def test_swipe_and_press(self):
        start_x, start_y = 200, 300
        end_x, end_y = 400, 500
        self.engine.swipe_and_press(start_x, start_y, end_x, end_y, 100, 2000, step_sleep=200)

    def test_get_element_text(self):
        e = self.engine.find_element('/Canvas/Panel/Sample/Text')

        self._start()
        text = self.engine.get_element_text(e)
        self._end("get_element_text")
        self.assertEqual(text, "Sample")

    def test_get_element_img(self):
        e = self.engine.find_element('/Canvas/Panel/Sample')

        self._start()
        text = self.engine.get_element_image(e)
        self._end("get_element_image")
        self.assertEqual(text, "bt_bg")

    def test_get_component_field(self):
        elements = self.engine.find_elements_path("Sample/Text")
        sdk_info = self.engine.get_sdk_version()
        ui_type = sdk_info.ui_type
        self._start()
        if ui_type == "UGUI":
            res = self.engine.get_component_field(elements[0], "Text", "text")
            self._end("get_component_field")
            self.assertEqual(res, "Sample")

            e = self.engine.find_element("Panel")
            res = self.engine.get_component_field(e, "MainControl", "bollon")
            self.assertEqual(res, "Bollon (UnityEngine.RectTransform)")
        else:
            res = self.engine.get_component_field(elements[0], "UILabel", "text")
            self._end("get_component_field")
            self.assertEqual(res, "Sample")

            e = self.engine.find_element("Panel")
            res = self.engine.get_component_field(e, "MainControl", "bollon")
            self.assertEqual(res, "Bollon (UnityEngine.GameObject)")

    def test_set_camera(self):
        pass
        # elements = self.engine.find_elements_path("UICamera")
        # self._start()
        # bounds = self.engine.get_element_world_bound(elements)
        # self._end("get_element_world_bound")

        # print self.engine.set_camera("CharModeCamera")
        # bounds = self.engine.get_element_bound(elements[0])
        # print(bounds)

    def test_get_component_methods(self):
        element = self.engine.find_element("Sample")
        self._start()
        methods = self.engine.get_component_methods(element, "Button")
        logger.debug(methods)
        self._end("get_component_methods")

    def test_call_component_method(self):
        element = self.engine.find_element("Sample")
        params = []
        params.append(5)
        params.append("Hello World")
        self._start()
        result = self.engine.call_component_method(element, "ReflectionTest", "TestReflection", params)
        logger.debug(result)
        self._end("call_component_method")

    def test_find_elements_path2(self):
        self._start()
        elements = self.engine.find_elements_path("/Canvas/Panel/{{(.*(S|s).*)}}/Text")
        logger.debug(elements)
        self._end("find_elements_path /root")

    def test_find_elements_path3(self):
        self._start()
        elements = self.engine.find_elements_path("/Canvas/Panel/{{Click|Slider}}/{{Text|Background}}")
        for element in elements:
            bound = self.engine.get_element_bound(element)
            logger.debug("Element : {0},Bound : {1}".format(element, bound))
        self._end("find_elements_path /root")

    @scene_enter("Joystick")
    def test_game_script_init(self):
        file_path = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(file_path, "gametestlib.dll")
        result = self.engine.game_script_init(path)
        logger.debug("init result : ".format(result))

        result = self.engine.get_registered_handlers()
        logger.debug("registered functions : {0}".format(result))

        result = self.engine.call_registered_handler("showColider", "")

    def test_register_game_callback(self):
        def _print_fun(v):
            print "game call"
            print "value = "+v
            return "_print_fun call return value"

        def _print_fun_returnvalue(v):
            print "game call return value"
            print "value = "+v
            return "_print_fun_returnvalue call return value"

        result = self.engine.register_game_callback("test", _print_fun)
        logger.debug("register game callback {0}".format(result))
        result = self.engine.register_game_callback("testReturn", _print_fun_returnvalue)
        logger.debug("register game callback {0}".format(result))

        callPcButton=self.engine.find_element("CallPC")

        for i in range(100):
            self.engine.click(callPcButton)



if __name__ == '__main__':
    unittest.main()
