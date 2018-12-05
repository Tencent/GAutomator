using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace WeTest.U3DAutomation
{
    class Command
    {
        public Socket socket; 
        public object sendObj; //返回的实例，需要json可序列化
        public string recvObj; //GAutomator客户端发送过来的json字符串
        public object recvObject; //GAutomator客户端发送的json反序列化的object实例
        public Cmd cmd; //命令类型
        public ResponseStatus status; //结果status

        public Command(Cmd cmd, Socket socket)
        {
            this.cmd = cmd;
            this.socket = socket;
            status = ResponseStatus.SUCCESS;
        }

        public Command()
        {

        }
    }
}
