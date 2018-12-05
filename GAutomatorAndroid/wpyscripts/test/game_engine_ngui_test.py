# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import unittest, math

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
            time.sleep(2)

        return wrapped

    return real_decorator


class GameEngineTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameEngineTest, self).__init__(*args, **kwargs)
        self.start_time = None

    def setUp(self):
        self.engine = get_engine()

    @classmethod
    def setUpClass(cls):
        cls.timeuse = []

    @classmethod
    def tearDownClass(cls):
        for item in cls.timeuse:
            print("{0},{1}".format(item["name"], item["use"]))

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

    # def test_test(self):
    #     button=self.engine.find_element("QQ")
    #     bound=self.engine.get_element_bound(button)
    #     self.engine.click(button)
    #     logger.debug("{0}".format(bound.__str__()))
    #
    def test_get_sdk_version(self):
        self._start()
        sdk_info = self.engine.get_sdk_version()
        self._end("get_sdk_version")

        logger.info(sdk_info)
        # self.assertTrue(cmp(sdk_info.engine_version, "5.1.2f1") == 0, "engine version Error")
        self.assertTrue(cmp(sdk_info.engine, "Unity3D") == 0, "engine Error")
        self.assertTrue(sdk_info.sdk_version == "1.0.0", "sdkversion Error")

    def test_find_element(self):
        self._start()
        element = self.engine.find_element("Control - Simple Button")
        self._end("find_element")
        logger.debug(element)

    def test_get_element_bound(self):
        element = self.engine.find_element("Sprite")
        self._start()
        bound = self.engine.get_element_bound(element)
        self._end("get_element_bound")

        logger.info(bound)

    def test_click_position(self):
        element = self.engine.find_element("Control - Simple Button")
        bound = self.engine.get_element_bound(element)
        self._start()
        result = self.engine.click_position(bound.x + bound.width / 2, bound.y + bound.height / 2)
        self._end("click_position")

        self.assertTrue(result, "Click Error")

    def test_get_element_bound(self):
        element = self.engine.find_element("Control - Simple Button")

        self._start()
        bound = self.engine.get_element_bound(element)
        self._end("get_element_bound")

        logger.info(bound)

    def test_click(self):
        element = self.engine.find_element("Control - Simple Button")
        self._start()
        result = self.engine.click(element)
        self._end("click")
        self.assertTrue(result, "Click Element error")

        time.sleep(4)
        element = self.engine.find_element("Control - Simple Button")
        bound = self.engine.get_element_bound(element)
        self._start()
        result = self.engine.click(bound)
        self._end("click")
        self.assertTrue(result, "Click ElementBound error")

    def test_press(self):
        # 按压节点
        element = self.engine.find_element("Control - Simple Button")
        self._start()
        result = self.engine.press(element, 2000)
        self._end("press 2000ms")
        self.assertTrue(result)

        # 按压ElementBound
        bound = self.engine.get_element_bound(element)
        result = self.engine.press(bound, 3000)
        self.assertTrue(result)

    def test_swipe(self):
        start_element = self.engine.find_element("Control - Simple Popup List")
        end_element = self.engine.find_element("Control - Simple Button")

        # 根据元素按压
        # result=self.engine.swipe(start_element,end_element,100)
        # self.assertTrue(result)

        # 根据位置按压
        start_bound = self.engine.get_element_bound(start_element)
        end_bound = self.engine.get_element_bound(end_element)
        self._start()
        result = self.engine.swipe_position(start_bound.x, start_bound.y, end_bound.x, end_bound.y, 500, 2000)
        self._end("swipe_position 2000ms")

    def test_get_touchable_element(self):
        self._start()
        elements = self.engine.get_touchable_elements(["LuaButton, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null","UISprite, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null"])
        self._end("get_touchable_element")

        print(elements)

        elements = self.engine.get_touchable_elements()
        self._end("get_touchable_element")

        print(elements)

    def test_get_touchable_element_bound(self):
        self._start()
        scene, elements = self.engine.get_touchable_elements_bound()
        self._end("get_touchable_elements_bound")
        self.assertEqual(len(elements), 21)
        self.assertEqual(scene, "Example 0 - Control Widgets")

    def test_get_current_scene(self):
        self._start()
        scene = self.engine.get_scene()
        self._end("get_scene")

        logger.debug("Scene:{0}".format(scene))
        self.assertEqual(scene, "Example 0 - Control Widgets")

    def test_input(self):
        e = self.engine.find_element("Control - Simple Input Field")
        self._start()
        old_content = self.engine.input(e, "Hello Wetest")
        self._end("input")
        self.assertEqual(old_content, "")

        e = self.engine.find_element("Control - Simple Input Field")
        str = self.engine.get_element_text(e)
        self.assertEqual(str, "Hello Wetest")

    def test_find_elements_path(self):
        self._start()
        elements = self.engine.find_elements_path("/UI Root/Camera/Anchor/Panel/Sprite/Label")
        self._end("find_elements_path /root")
        self.assertEqual(len(elements), 1)

        self._start()
        items = self.engine.find_elements_path("Label")
        self._end("find_elements_path all")
        self.assertEqual(len(items), 16)

        self._start()
        items = self.engine.find_elements_path("Sprite{img=Window}")
        self._end("find_elements_path img")
        self.assertEqual(len(items), 1)

        self._start()
        items = self.engine.find_elements_path("Control - Simple Button{txt=Button}")
        self._end("find_elements_path txt")
        self.assertEqual(len(items), 1)

        self._start()
        items = self.engine.find_elements_path("/UI Root/Camera/Anchor/Panel/*[4]")
        self._end("find_elements_path index")
        self.assertEqual(len(items), 1)

        items = self.engine.find_elements_path("Camera/Anchor/Panel/*[4]")
        self.assertEqual(len(items), 1)

        items = self.engine.find_elements_path("Sprite[0]")
        self.assertEqual(len(items), 1)

    def test_get_element_bound(self):
        element = self.engine.find_element("Control - Simple Button")
        self._start()
        bound = self.engine.get_element_bound(element)
        self._end("get_element_bound")
        print(bound)

    def test_get_registered_handlers(self):
        self._start()
        result = self.engine.get_registered_handlers()
        self._end("get_registered_handlers")
        self.assertEqual(["test"], result)

    def test_call_registered_handler(self):
        self._start()
        result = self.engine.call_registered_handler("test", "python call test")
        self._end("call_registered_handler")
        self.assertEqual("python call test Response", result)

    def test_get_element_text(self):
        e = self.engine.find_element('Control - Simple Button/Label')

        self._start()
        text = self.engine.get_element_text(e)
        self._end("get_element_text")
        self.assertEqual(text, "Button")

    def test_get_element_img(self):
        e = self.engine.find_element('Sprite')

        self._start()
        text = self.engine.get_element_image(e)
        self._end("get_element_image")
        self.assertEqual(text, "Window")

    def test_get_component_field(self):
        elements = self.engine.find_elements_path("Control - Simple Button/Label")
        self._start()
        res = self.engine.get_component_field(elements[0], "UILabel", "text")
        self._end("get_component_field")
        self.assertEqual(res, "Button")

        element = self.engine.find_element("Camera")
        res = self.engine.get_component_field(element, "UICamera", "hoveredObject")
        print(res)

    # def test_get_element_text(self):
    #     e = self.engine.find_elements_path('Sprite/Label')
    #     text = self.engine.get_element_text(e[0])
    #     logger.info(text)


    def test_get_element_image(self):
        e = self.engine.find_element('Sprite')
        text = self.engine.get_element_image(e)
        logger.info(text)

        # def test_get_dump_tree(self):
        #     xml = self.engine.get_dump_tree()
        #     logger.info(xml)

        # def test_get_elements_by_position(self):
        #     element = self.engine.find_element("Sample")
        #     bound = self.engine.get_element_bound(element)
        #     logger.info(bound[0])
        #     elements = self.engine.find_elements_by_position(bound[0]["x"]+bound[0]["width"]/2, bound[0]["y"]+bound[0]["height"]/2)
        #     for e in elements:
        #         logger.info(e)
