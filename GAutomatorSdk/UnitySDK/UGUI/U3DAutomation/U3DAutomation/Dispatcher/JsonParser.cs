using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WeTest.U3DAutomation
{
    class JsonParser
    {
        public static string WrapResponse(Command command)
        {
            Cmd cmd = command.cmd;
            Response response = new Response();
            response.cmd = (int)cmd;
            response.status = command.status;
            response.data = command.sendObj;
            string res = null;
            try
            {
                res=JsonMapper.ToJson(response);
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                response.status = ResponseStatus.SUCCESS;
                response.data = null;
                res = JsonMapper.ToJson(response);
            }
            return res;
        }

        public static T Deserialization<T>(Command cmd)
        {
            return JsonMapper.ToObject<T>(cmd.recvObj);
        }



        /// <summary>
        /// 放在主线程中解压，json部分过于耗时，因此可以在其他线程解压好。主线程之间使用即可
        /// 
        /// 这部分的处理逻辑，理应在CommandHandler类里面处理，逻辑被分在了两个不同的部分
        /// </summary>
        /// <param name="cmd"></param>
        /// <returns></returns>
        public static bool PreDeserialization(Command cmd)
        {
            if(cmd==null||cmd.cmd==null){
                return false;
            }
            switch (cmd.cmd)
            {
                case Cmd.HANDLE_TOUCH_EVENTS:
                    TouchEvent[] events = Deserialization<TouchEvent[]>(cmd);
                    cmd.recvObject = events;
                    break;
                default:
                    cmd.recvObject = null;
                    break;
            }
            return true;
        }
    }
}
