using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace WeTest.U3DAutomation
{
    class AsyncCallBack
    {
        private AutoResetEvent finishEvent = new AutoResetEvent(false);
        private string _returnValue = null;
        private int status = 0;

        public string returnValue
        {
            get
            {
                finishEvent.WaitOne();
                if (status != 0)
                {
                    throw new Exception(_returnValue);
                }
                return _returnValue;
            }
        }

        public string getReturnValueTimeout(int timeout)
        {
            finishEvent.WaitOne(timeout);
            if (status != 0)
            {
                throw new Exception(_returnValue);
            }
            return _returnValue;
        }

        public void callBack(int status, String value)
        {
            this.status = status;
            this._returnValue = value;
            finishEvent.Set();
        }
    }

	class ClientCaller
	{
        public delegate string HandleCallBack(string message);

        public static Socket socket; //长连接
        private static Dictionary<String, HandleCallBack> functions = new Dictionary<String, HandleCallBack>();
        private static readonly object callbackMapLock = new object();
        private static Dictionary<int, CustomHandler.PcCallBack> callbacks = new Dictionary<int, CustomHandler.PcCallBack>();
        private static int seq = 0;//回调递增

        public static void SetRpcMethod(Command command)
        {
            String name = command.recvObj;
            socket = command.socket;
            if (!functions.ContainsKey(name))
            {
                functions.Add(name, null);
                Logger.d("Add RPC name = " + name);
            }
            else
            {
                Logger.w("name = " + name + " has registered");
            }
            command.sendObj = "OK";
            CommandDispatcher.SendCommand(command);
        }

        private static void AddCallBack(int seq,CustomHandler.PcCallBack callBack){
            if(callBack==null){
                return;
            }

            lock (callbackMapLock)
            {
                if (!callbacks.ContainsKey(seq))
                {
                    callbacks.Add(seq, callBack);
                }
            }
        }

        public static void InvokeSeqCallBack(Command command)
        {
            RPCResponseBody rPCResponseBody=JsonParser.Deserialization<RPCResponseBody>(command);
            int seq=rPCResponseBody.seq;
            int status=rPCResponseBody.status;
            String name=rPCResponseBody.name;
            String value=rPCResponseBody.returnValue;
            if(status!=0){
                Logger.w("RPC method call error,reponse = "+command.recvObj);
            }
            CustomHandler.PcCallBack pcCallBack = null;
            lock (callbackMapLock)
            {
                if (callbacks.ContainsKey(seq))
                {
                    pcCallBack=callbacks[seq];
                    callbacks.Remove(seq);
                }
            }

            if (pcCallBack == null)
            {
                Logger.w("RPC method can't find callback function, reponse = "+command.recvObj);
            }

            try
            {
                pcCallBack(status,value);
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message, ex);
            }
        }


        public static void Invoke(string name, string value, CustomHandler.PcCallBack callback)
        {
            if (functions.ContainsKey(name)||socket==null)
            {
                throw new Exception("Not Register Callback");
            }
            Command command = new Command();
            command.cmd = Cmd.RPC_METHOD;
            command.socket = socket;
            RPCRequestBody rpcBody = new RPCRequestBody();
            rpcBody.name = name;
            rpcBody.value = value;
            rpcBody.seq = ++seq;
            command.sendObj = rpcBody;
            AddCallBack(rpcBody.seq, callback);
            CommandDispatcher.SendCommand(command);
        }

        public static string InvokeReturnValue(string name, string value, int timeout)
        {
            AsyncCallBack asyncCallBack = new AsyncCallBack();
            Invoke(name, value, asyncCallBack.callBack);
            string result=asyncCallBack.getReturnValueTimeout(timeout);
            return result;

        }
	}

}
