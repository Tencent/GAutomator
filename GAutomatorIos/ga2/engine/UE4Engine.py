# -*- encoding: utf-8 -*-
from ga2.engine.engine import *
from ga2.engine.uielement import UIElement


class UE4Engine(GameEngine):
    def __init__(self, address, port):
        super(UE4Engine, self).__init__(address, port)
        self._callback_socket = None
        self._callback_functions = {}
        self._callback_thread = None

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
        ret = self.socket.send_command(Commands.GET_ELEMENT_TEXT, element.object_name)
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
        ret = self.socket.send_command(Commands.GET_ELEMENT_IMAGE, element.object_name)
        return ret

    def _get_elements_UE4_bound(self, elements):
        '''
                获取ue4游戏中控件信息
        :param elements: 查找到的GameObject
        :return: 屏幕中的位置（x,y），左上角为原点，及长宽
            examples:
            {"x":0.5，
            "y":0.5.0,
            "width":0.2
            "height":0.1}
        :rtype: ElementBound
        :raises WeTestInvaildArg,WeTestRuntimeError
        '''
        if elements is None:
            raise WeTestInvaildArg("Invaild Instance,element is None")

        send_params = [e.object_name for e in elements]
        ret = self.socket.send_command(Commands.GET_ELEMENTS_BOUND, send_params)
        return ret

    def send_UE4_GM(self, params):
        '''
            发送gm指令
        :param params: array contians(classname,funcname,cmd,param)
        :return:
        '''
        if params is None:
            raise WeTestInvaildArg("Invaild Instance,element is None")
        ret = self.socket.send_command(Commands.CALL_REGISTER_HANDLER, params)
        return ret

    def get_character_swip(self, params):
        '''
            开启射线检测
        :param flag: 【"float:检测距离"，"float:定时时间"，"bool:是否循环"】
        :return:
        '''
        if params is None:
            raise WeTestInvaildArg("Invaild Instance,element is None")
        ret = self.socket.send_command(Commands.GET_CHARACTER_SWIP, params)
        return ret

    def set_change_rotator(self, params):
        '''
            设置人物转向值
        :param flag: 调用参数 float
        :return:
        '''
        if params is None:
            raise WeTestInvaildArg("Invaild Instance,element is None")
        ret = self.socket.send_command(Commands.SET_CHANGEROTATOR, params)
        return ret

    def get_character_scale(self):
        '''
            获取旋转倍数，配合set_change_rotator实现（例如90度=params*rotator）
        :param flag:
        :return:float
        '''
        ret = self.socket.send_command(Commands.GET_SCALE)
        return ret

    def get_bound(self):
        '''
            获取物体大小
        :param flag:
        :return:[x,y,z]
        '''

        ret = self.socket.send_command(Commands.GET_BOUND)
        return ret

    def set_character_forward(self, params):
        '''
            设置人物前进距离
        :param flag: distance:int
        :return:
        '''
        if params is None:
            raise WeTestInvaildArg("Invaild Instance,element is None")
        ret = self.socket.send_command(Commands.SET_LOCATION, params)
        return ret

    def get_character_rotation(self):
        '''
            获取角色当前旋转角度
        :param flag:
        :return:[roll,pitch,yall]
        '''
        ret = self.socket.send_command(Commands.GET_CHARACTER_ROTATION)
        return ret

    def set_character_location(self, params):
        '''
            角色瞬移
        :param flag: float[X;Y]
        :return:
        '''
        if params is None:
            raise WeTestInvaildArg("Invaild Instance,element is None")
        ret = self.socket.send_command(Commands.SET_CHARACTER, params)
        return ret

    def get_device_info(self):
        '''
            获取设备信息
        '''
        ret = self.socket.send_command(Commands.GET_EQUIPMENT_INFO)
        return ret
