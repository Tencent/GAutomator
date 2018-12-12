# -*- coding: UTF-8 -*-
from ga2.engine.engine import *
from ga2.engine.engineFactory import EngineFactory

#define an engine type
EngineType.MY_ENGINE=101


#define an engine connector
class MyEngine(GameEngine):
    def __init__(self, address, port):
        super(MyEngine, self).__init__(address, port)

    def get_element_bound(self, element):
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


    def get_element_text(self, element):
        if element is None:
            raise WeTestInvaildArg("Invalid Instance")
        ret = self.socket.send_command(Commands.GET_ELEMENT_TEXT, element.object_name)
        return ret

    def get_pos_text(self, x, y):
        ret = self.socket.send_command(Commands.GET_POS_TEXT, [float(x), float(y)])
        if ret:
            return ret
        else:
            return None

#register engine connector
EngineFactory.registerNewEngineType(EngineType.MY_ENGINE,MyEngine)