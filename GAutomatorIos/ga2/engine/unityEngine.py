# -*- coding: UTF-8 -*-
from ga2.engine.engine import *
from ga2.engine.uielement import UIElement


class UnityEngine(GameEngine):
    def __init__(self, address, port):
        super(UnityEngine, self).__init__(address, port)
        self._callback_socket = None
        self._callback_functions = {}
        self._callback_thread = None

    def _parse_path(self, path):
        if path is None:
            return None

        nodeInfos = []
        nodes = path.split("/")

        if len(nodes) == 0:
            return None
        elif nodes[0] == '':
            pathNode = {"name": "/", "index": -1, "txt": "", "img": "", "regex": ""}
            nodeInfos.append(pathNode)
            nodes = nodes[1:]
        name_re = re.compile(r"(?P<name>[^[{]+)")
        txt_re = re.compile(r"(txt\s*=\s*(?P<txt>[^,\}]*))")
        img_re = re.compile(r"(img\s*=\s*(?P<img>[^,\}]*))")
        index_re = re.compile(r"\[(?P<index>\d+)\]")
        regex_re = re.compile(r"\{\{(?P<regex>.+)\}\}")
        for node in nodes:
            result = regex_re.search(node)
            if result:
                regex = result.groupdict().get("regex", "")
                name = ""
            else:
                regex = ""
                result = name_re.search(node)
                if result:
                    name = result.groupdict().get("name", "")
                else:
                    name = ""

            result = txt_re.search(node)
            if result:
                txt = result.groupdict().get("txt", "")
            else:
                txt = ""

            result = img_re.search(node)
            if result:
                img = result.groupdict().get("img", "")
            else:
                img = ""
            result = index_re.search(node)
            if result:
                index = result.groupdict().get("index", "-1")
                index = int(index)
            else:
                index = -1
            pathNode = {"name": name, "index": index, "txt": txt, "img": img, "regex": regex}
            nodeInfos.append(pathNode)
        return nodeInfos

    def find_elements_path(self, path):
        """
        表达式匹配获取符合的所有节点
        第一个节点"/"代表从根节点，如果不是代表可以从任意位置开始


        index：代表节点的位置。
             parent
           /      \
         index[0]  index[1]

         name:代表节点名称，"*"代表任意名称
         text:代表节点的文字内容（当前GameObject的挂载的Compenent）
         img:图片名称,sprite或者texture名称


         /Canvas/Panel/Button
         Canvas[0]{txt="hello"}/Button
         /Canvas/Panel/*[1]/Button
        :param path:
            需要查找的路径,/Canvas/Button[0]{txt=Button,img=img}
        :Usage:
            >>>button=engine.find_elements_path('/Canvas/Panel/Button')
            >>>button2=engine.find_elements_path('/Canvas/Panel/*[1]/Button')
            >>>button3=engine.find_elements_path('Canvas/Button{txt=hello}')
        :return:包含instance的Elements对象列表
            example:
            [{"objectName":"/Canvas/Panel/Button",
            "Instance":4257741},{"objectName":"/Canvas/Panel/Button",
            "Instance":4257742}]
        """
        nodeInfos = self._parse_path(path)
        if nodeInfos is None:
            raise WeTestInvaildArg("Error path")

        ret = self.socket.send_command(Commands.FIND_ELEMENT_PATH, nodeInfos)
        elements = []
        for e in ret:
            element = Element(e["name"], e["instance"])
            elements.append(element)

        return elements

    def find_elements_by_component(self, name):
        """
            通过GameObject.FindObjectsOfType(Type.GetType(name))查找对应的GameObject.

            Type.GetType获取不到的话，默认会尝试name,Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null
            及name, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null
        :param name:
            查找的类型的，AssemblyQualifiedName，如WetestManager,U3DAutomation, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null
        :return:
            当前界面中所有挂载改界面的
        """
        ret = self.socket.send_command(Commands.FIND_ELEMENTS_COMPONENT, [name])
        elements = []
        for e in ret:
            element = Element(e["name"], e["instance"])
            elements.append(element)
        return elements

    def get_element_text(self, element):
        """
            获取GameObject文字信息
            NGUI控件则获取UILable、UIInput、GUIText组件上的文字信息
            UGUI控件则获取Text、GUIText组件上的问题信息
        :param element: 查找到的GameObject

        :Usage:
            >>>element=engine.find_element('/Canvas/Panel/Button')
            >>>text=engine.get_element_text(element)
        :return:文字内容
        :raises WeTestInvaildArg,WeTestRuntimeError
        """
        if element is None:
            raise WeTestInvaildArg("Invalid Instance")
        ret = self.socket.send_command(Commands.GET_ELEMENT_TEXT, element.instance)
        return ret

    def get_element_image(self, element):
        """
            获取GameObject图片名称
            NGUI控件则获取UITexture、UISprite、SpriteRenderer组件上的图片名称
            UGUI控件则获取Image、RawImage、SpriteRenderer组件上的图片名称
        :param element: 查找到的GameObject

        :Usage:
            >>>element=engine.find_element('/Canvas/Panel/Button')
            >>>image=engine.get_element_image(element)
        :return:图片名称
        :rtype: str
        :raises WeTestInvaildArg,WeTestRuntimeError
        """
        if element is None:
            raise WeTestInvaildArg("Invalid Instance")
        ret = self.socket.send_command(Commands.GET_ELEMENT_IMAGE, element.instance)
        return ret

    def get_registered_handlers(self):
        """
            获取用户当前注册的自定义的函数集合
        :Usage:
            >>>import wpyscripts.manager as manager
            >>>engine=manager.get_engine()
            >>>function_names=engine.get_registered_handlers()
        :return: []注册的自定义函数名称序列
        :raise WeTestInvaildArg,WeTestRuntimeError
        """
        ret = self.socket.send_command(Commands.GET_REGISTERED_HANDLERS)
        return ret

    def call_registered_handler(self, name, args):
        """
            调用指定的注册的函数，并返回返回值
        :param name:已经注册的函数名称
        :param args:传入函数中的参数，一个不超过1024个字符的参数
        :param timeout:超时时间(超时后直接返回，SDK中对应的函数可能还是会执行完，不会中断)
        :return:
            自定义注册函数的返回值
        :raise WeTestInvaildArg,WeTestRuntimeError
        """
        ret = self.socket.send_command(Commands.CALL_REGISTER_HANDLER, {"name": name, "args": args})
        return ret

    def get_element_bound(self, element):
        """
        获取GameObject在屏幕上的位置和长宽高
        :param element: 查找到的GameObject

        :Usage:
            >>>
            >>>element=engine.find_element('/Canvas/Panel/Button')
            >>>bound=engine.get_element_bound(element)
        :return:屏幕中的位置（x,y），左上角为原点，及长宽
            examples:
            {"x":0.5，
            "y":0.5.0,
            "width":0.2
            "height":0.1}
        :rtype: ElementBound
        :raises WeTestInvaildArg,WeTestRuntimeError
        """
        if element is None:
            raise WeTestInvaildArg("Invaild Instance,element is None")

        ret = self._get_elements_bound([element])
        print(ret)
        if ret:
            result = ret[0]
            if not result["existed"]:
                return None
            else:
                return ElementBound(result["x"], result["y"], result["width"], result["height"], result["visible"])
        return None

    def _get_elements_bound(self, elements):
        send_params = [e.instance for e in elements]
        ret = self.socket.send_command(Commands.GET_ELEMENTS_BOUND, send_params)
        return ret


    def get_touchable_uielements(self, params=None):

        """
            获取当前界面的可点击节点的列表
        :return:
            [(element1,point1),(element2,point2)]
            [({"object_name":"/Canvas/Panel/Button","Instance":4257741},{"x":250,"y":300}),.....]
        :raise WeTestRuntimeError
        """
        ret = self.socket.send_command(Commands.GET_UI_INTERACT_STATUS, params)
        elements = []
        for i in range(0, len(ret["elements"])):
            node = ret["elements"][i]
            element = Element(node["name"], node["instanceid"])
            bound = ElementBound(node["bound"]["x"], node["bound"]["y"], node["bound"]["fWidth"],  node["bound"]["fHeight"])
            elements.append(UIElement(element, bound))
        return elements
    #
    # def get_touchable_elements_bound(self, params=None):
    #
    #     """
    #         获取当前界面的可点击节点的列表
    #     :Usage:
    #         >>>import wpyscripts.manager as manager
    #         >>>engine=manager.get_engine()
    #         >>>buttons=engine.get_touchable_elements_bound()
    #     :return:
    #         [(element1,point1),(element2,point2)]
    #         [({"object_name":"/Canvas/Panel/Button","Instance":4257741},{"x":250,"y":300}),.....]
    #     :raise WeTestRuntimeError
    #     """
    #     ret = self.socket.send_command(Commands.GET_UI_INTERACT_STATUS, params)
    #     elements = []
    #     for i in range(0, len(ret["elements"])):
    #         node = ret["elements"][i]
    #         element = Element(node["name"], node["instanceid"])
    #         bound = ElementBound(node["bound"]["x"], node["bound"]["y"], node["bound"]["fWidth"],
    #                              node["bound"]["fHeight"])
    #         elements.append((element, bound))
    #     return elements

    # def _inject_touch_actions(self, actions, timeout=20):
    #
    #     """
    #         发送touch序列号，touch事件结束之后，才会返回。同步函数
    #     :param actions:
    #     :return:
    #     """
    #     ret = self.socket.send_command(Commands.HANDLE_TOUCH_EVENTS, actions, timeout)
    #     return ret

    # def swipe(self, start_element, end_element, steps=20, duration=1000):
    #     """
    #
    #     :param start_element:
    #     :param end_element:
    #     :param steps:步数，通过控制步数能够控制滑动时长和滑动平滑度，每一步走的耗时在step_sleep为5ms左右。100步时长>500毫。无法做到精确控制，调试确认
    #     :param step_sleep:每个步骤的间隔时长，单位毫秒
    #
    #     :Usage:
    #         >>>import wpyscripts.manager as manager
    #         >>>engine=manager.get_engine()
    #         >>>start_element=engine.find_element('/Canvas/Panel/Button')
    #         >>>end_element=engine.find_element('/Canvas/Panel/Button2')
    #         >>>engine.swipe(start_element,end_element,5000)
    #     :return: WeTestRuntimeError,WeTestInvaildArg
    #     """
    #     start_x = 0
    #     start_y = 0
    #     end_x = 0
    #     end_y = 0
    #     if start_element and isinstance(start_element, Element) and end_element and isinstance(end_element, Element):
    #         ret = self._get_elements_bound([start_element, end_element])
    #         if ret and len(ret) == 2:
    #             result = ret[0]
    #             if not result["existed"] or not result["visible"]:
    #                 reason = "StartElement = {0} not existed or unvisible".format(start_element)
    #                 raise WeTestInvaildArg(reason)
    #             else:
    #                 start_x = result["x"] + result["width"] / 2
    #                 start_y = result["y"] + result["height"] / 2
    #
    #             result = ret[1]
    #             if not result["existed"] or not result["visible"]:
    #                 reason = "EndElement = {0} not existed or unvisible".format(start_element)
    #                 raise WeTestInvaildArg(reason)
    #             else:
    #                 end_x = result["x"] + result["width"] / 2
    #                 end_y = result["y"] + result["height"] / 2
    #     elif start_element and isinstance(start_element, ElementBound) and end_element and isinstance(end_element,
    #                                                                                                   ElementBound):
    #         start_x = start_element.x + start_element.width / 2
    #         start_y = start_element.y + start_element.height / 2
    #         end_x = end_element.x + end_element.width / 2
    #         end_y = end_element.y + end_element.height / 2
    #     else:
    #         reason = "Input start_element = {0},end_element = {1},vaild argument is Element or ElementBound".format(
    #             start_element, end_element)
    #         raise WeTestInvaildArg(reason)
    #
    #     return self.swipe_position(start_x, start_y, end_x, end_y, steps, duration=duration)

    # def swipe_and_press(self, start_x, start_y, end_x, end_y, steps, duration, step_sleep=5):
    #     """
    #     滑动并在结束的地方一直按压
    #     :param start_x: 起始位置x，绝对坐标
    #     :param start_y: 起始位置y，绝对坐标
    #     :param end_x: 结束位置x,绝对坐标
    #     :param end_y:结束位置y，绝对坐标
    #     :param steps: 滑动中间的步骤数，每一步的间隔为5ms，可以用于控制滑动速度和平滑度
    #     :param step_sleep:每个步骤的间隔时长，单位毫秒
    #     :param duration: 结束位置按压时间，单位是毫秒ms
    #
    #     :Usage:
    #         >>>import wpyscripts.manager as manager
    #         >>>engine=manager.get_engine()
    #         >>>engine.swipe_and_press(start_x,start_y,end_x,end_y,50,10000,step_sleep=200)
    #     :raise WeTestInvaildArg,WeTestRuntimeError
    #     """
    #     if steps <= 0:
    #         reason = "steps = {0} is invaild, steps must more than 0".format(steps)
    #         raise WeTestInvaildArg(reason)
    #     start_x = int(start_x)
    #     start_y = int(start_y)
    #     end_x = int(end_x)
    #     end_y = int(end_y)
    #     actions = [{"x": start_x, "y": start_y, "sleeptime": 0, "type": TouchEvent.ACTION_DOWN}]
    #
    #     x_distance = (end_x - start_x) * 1.0 / steps
    #     y_distance = (end_y - start_y) * 1.0 / steps
    #     move_x, move_y = start_x, start_y
    #
    #     for i in range(steps - 1):
    #         move_x += x_distance
    #         move_y += y_distance
    #         actions.append(
    #             {"x": int(move_x), "y": int(move_y), "sleeptime": step_sleep, "type": TouchEvent.ACTION_MOVE})
    #
    #     move_x += x_distance
    #     move_y += y_distance
    #     actions.append(
    #         {"x": int(move_x), "y": int(move_y), "sleeptime": duration, "type": TouchEvent.ACTION_MOVE})
    #
    #     actions.append({"x": int(end_x), "y": int(end_y), "sleeptime": 0, "type": TouchEvent.ACTION_UP})
    #
    #     self._inject_touch_actions(actions, timeout=60)
    #     return True
    #
    # def input(self, locator, text):
    #     """
    #
    #     :param locator: is an element locator
    #     :param text: input的内容
    #
    #     :Usage:
    #         >>>import wpyscripts.manager as manager
    #         >>>engine=manager.get_engine()
    #         >>>element=engine.find_element("/Canvas/Panel/input")
    #         >>>old_txt=engine.input(element,"new text")
    #     :return: "hello world"input控件上原有的内容
    #     :raise WeTestInvaildArg,WeTestRuntimeError
    #     """
    #     if locator and isinstance(locator, Element):
    #         result = self.socket.send_command(Commands.SET_INPUT_TEXT, {"instance": locator.instance, "content": text})
    #         return result
    #     else:
    #         reason = "Input locator = {0},text = {1},vaild argument is Element or ElementBound".format(locator, text)
    #         raise WeTestInvaildArg(reason)

    def get_element_world_bound(self, elements):
        """
            查找节点对应的世界坐标。世界坐标包含，节点的中心位置的x,y,z坐标，及物体离中心点在在x,y,z轴上的大小。
            具体详见：http://docs.unity3d.com/ScriptReference/bound.html
        :param elements: 一个Element或者Element[]，节点应该至少包含Renderer、MeshFilter或Colider组件
        :return: WorldBound[]

        :Usage:
            >>>hero1=engine.find_element("hero1")
            >>>hero2=engine.find_element("hero2")
            >>>bound=engine.get_element_world_bound([hero1,hero2])
        :raise WeTestInvaildArg，WeTestRuntimeError
        """
        if elements is None:
            raise WeTestInvaildArg("Invaild Instance")
        if isinstance(elements, Element):
            elements = [elements]

        if len(elements) == 0:
            raise WeTestInvaildArg("Invaild Instance,search node is error")

        req = [e.instance for e in elements]
        ret = self.socket.send_command(Commands.GET_ELEMENT_WORLD_BOUND, req)

        world_bound = []
        for res in ret:
            world_bound = WorldBound(res["id"], res["existed"])
            if world_bound.existed:
                world_bound.center_x = res["centerX"]
                world_bound.center_y = res["centerY"]
                world_bound.center_z = res["centerZ"]
                world_bound.extents_x = res["extentsX"]
                world_bound.extents_y = res["extentsY"]
                world_bound.extents_z = res["extentsZ"]
                world_bound.append(world_bound)

        return world_bound

    def get_component_field(self, element, component, attribute):
        """
            通过反射的方式获取到GameObject上面组件的属性值。反射查看是否存在Property或者Field名称为attribute
        :param element:已经找到的GameObject对象
        :param component:组件名称
        :param attribute:字段或者属性名称
        :return: 字段或者属性名称toString()之后的string值

        :Usage:
            >>>elements = self.engine.find_elements_path("Sample/Text")
            >>>res = self.engine.get_component_field(elements[0], "Text", "text")
        :raise WeTestInvaildArg，WeTestRuntimeError
        """
        if element is None or component is None or attribute is None:
            raise WeTestInvaildArg("Invaild Instance")

        ret = self.socket.send_command(Commands.GET_OBJECT_FIELD,
                                       {"instance": element.instance, "comopentName": component,
                                        "attributeName": attribute})

        return ret

    def set_camera(self, camera):
        ret = self.socket.send_command(Commands.SET_CAMERA_NAME, [camera])
        return ret

    def get_component_methods(self, element, component):
        """
        通过反射获取组件的方法
        :param element:已经找到的GameObject对象
        :param component:组件名称
        :return:方法的描述，包括方法名称，返回值类型，参数类型
        :Usage:
            >>>element = engine.find_element("Sample")
            >>>methods = engine.get_component_methods(element, "ReflectionTest")
        :raise WeTestInvaildArg，WeTestRuntimeError
        """
        if element is None or component is None:
            raise WeTestInvaildArg("Invaild Instance")

        ret = self.socket.send_command(Commands.GET_COMPONENT_METHODS,
                                       {"instance": element.instance, "comopentName": component})
        return ret

    def call_component_method(self, element, component, method, params):
        """
        通过反射调用组件上的方法
        :param element:已经找到的GameObject对象
        :param component:组件名称
        :param method:方法名称
        :param params:方法参数数组
        :return:方法的返回
        :Usage:
            >>>element = engine.find_element("Sample")
            >>>params = [5, "Hello World"]
            >>>result = engine.call_component_method(element, "ReflectionTest", "TestReflection", params)
        :raise WeTestInvaildArg，WeTestRuntimeError
        """
        if element is None or component is None or method is None:
            raise WeTestInvaildArg("Invaild Instance")

        ret = self.socket.send_command(Commands.CALL_COMPONENT_MOTHOD,
                                       {"instance": element.instance, "comopentName": component,
                                        "methodName": method, "parameters": params})
        return ret

    # def game_script_init(self, path):
    #     """
    #         将gametestlib.dll push到手机上的/data/local/tmp目录下
    #         然后调用gametestlib.dll中的GameTest.Test.init()方法
    #     :param path: gametestlib.dll， inject c# script
    #     :return:
    #     """
    #     logger.debug("push c# test script : {0}".format(path))
    #     result = AdbTool().cmd_wait("push", path, "/data/local/tmp/gametestlib.dll")
    #     logger.debug("push result : {0}".format(result))
    #
    #     ret = self.socket.send_command(Commands.LOAD_TEST_LIB)
    #     return ret
    #
    # def register_game_callback(self, name, func):
    #     if not name or not func:
    #         raise WeTestInvaildArg("Name or Function can't be None")
    #     if not self._callback_socket or not self._callback_functions:
    #         self._callback_socket = SocketClient(self.address, self.port)
    #         event = threading.Event()
    #         self._callback_thread = RPCReceiveThread(self._callback_socket, self._callback_functions, event)
    #         self._callback_thread.start()
    #
    #     self._callback_functions[name] = func
    #     self._callback_socket.send_package(Commands.PRC_SET_METHOD, name)
    #     return self._callback_thread.get_result()
