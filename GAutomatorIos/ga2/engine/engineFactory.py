
from ga2.engine.engine import *
from ga2.engine.unityEngine import *
class EngineFactory:
    __engineTypeMap = {EngineType.Unity: UnityEngine}

    @staticmethod
    def registerNewEngineType( engine_type, connector_type):
        EngineFactory.__engineTypeMap[engine_type]=connector_type


    @staticmethod
    def createEngine(engine_type, address, port):
        if engine_type not in EngineFactory.__engineTypeMap.keys():
            return None
        return EngineFactory.__engineTypeMap[engine_type](address, port)



