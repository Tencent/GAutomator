using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WeTest.U3DAutomation
{
    [Serializable]
    enum ResponseStatus
    {
        SUCCESS = 0,
        NO_SUCH_CMD = 1,//发送的命令不可识别
        UNPACK_ERROR = 2,//发生的body数据，json反序列化失败
        UN_KNOW_ERROR = 3,//一般是在执行任务的过程中抛出异常，未预料的问题
        GAMEOBJ_NOT_EXIST = 4,//gameobject 不存在
        COMPONENT_NOT_EXIST = 5,//component 不存在
        NO_SUCH_HANDLER = 6,//没有该自定义的handler

        REFLECTION_ERROR = 7,//反射获取某个对象时出错
        NO_SUCH_RESOURCE=8,//没有所需的资源内容

    }

    [Serializable]
    class Response
    {
        public int cmd;
        public ResponseStatus status = ResponseStatus.SUCCESS;
        public object data;
    }
}
