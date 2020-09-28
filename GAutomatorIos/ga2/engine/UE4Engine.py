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