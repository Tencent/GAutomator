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
        public object sendObj;
        public string recvObj;
        public object recvObject;
        public Cmd cmd;
        public ResponseStatus status;

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
