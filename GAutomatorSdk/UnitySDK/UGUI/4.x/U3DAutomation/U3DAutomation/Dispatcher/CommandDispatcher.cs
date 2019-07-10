using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;

namespace WeTest.U3DAutomation
{
    class CommandDispatcher
    {
        public static readonly int UIAUTOMATION_SERVER_PORT = 27019;
        public static readonly int MAX_CONNECT = 5;//探索测试精灵一个，录制一个，执行一个，下一个游戏启动时尝试关闭该游戏，空余一个
        public static readonly int MAX_RETRY = 4;

        private static Thread sendThread;

        private static int socketCount=0;
        private static bool stop = false;
        private static Socket serverSocket;

        private static Queue<Command> commandQueue = new Queue<Command>();//接收队列
        private static BlockQueue<Command> sendQueue = new BlockQueue<Command>();//发送队列


        public static void CloseServerSocket()
        {
            CloseSocket(serverSocket);
        }


        private static bool Create(int port, int blocklog)
        {
            IPEndPoint ipEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);

            serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            try
            {
                serverSocket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);;
                serverSocket.Bind(ipEndPoint);
                serverSocket.Listen(blocklog);
                serverSocket.BeginAccept(new AsyncCallback(Accept), serverSocket);
                return true;
            }
            catch (System.Exception ex)
            {
                Logger.e("Exception" + ex);
            }
            return false;
        }

        /// <summary>
        /// 关闭上一个游戏，上一个游戏打开了27018端口
        /// </summary>
        private static void ClosePreGame()
        {
            IPAddress[] IPs = Dns.GetHostAddresses("127.0.0.1");

            Socket s = new Socket(AddressFamily.InterNetwork,
                SocketType.Stream,
                ProtocolType.Tcp);
            s.Connect(IPs[0], UIAUTOMATION_SERVER_PORT);

            Command killCmd = new Command();
            killCmd.cmd = Cmd.EXIT;
            killCmd.status = ResponseStatus.SUCCESS;
            string data = JsonParser.WrapResponse(killCmd);

            byte[] byteData = Encoding.ASCII.GetBytes(data);
            byte[] sendByteData = new byte[byteData.Length + 4];
            byte[] lengthByte = BitConverter.GetBytes(byteData.Length);
            Buffer.BlockCopy(lengthByte, 0, sendByteData, 0, 4);
            Buffer.BlockCopy(byteData, 0, sendByteData, 4, byteData.Length);
            try
            {
                s.Send(sendByteData);
            }
            catch (Exception ex)
            {
                Logger.d(ex.ToString());
            }
            finally
            {
                s.Close();
            }
        }

        private static void RecvThread()
        {
            Logger.d("Start RecvThread");
            for (int i = 0; i < MAX_RETRY; ++i)
            {
                try
                {
                    if (!Create(UIAUTOMATION_SERVER_PORT, MAX_CONNECT))
                    {
                        Logger.d("Try to close pre game");
                        ClosePreGame();
                        Thread.Sleep(500);
                    }
                    else
                    {
                        break;
                    }
                }
                catch (System.Exception ex)
                {
                    Logger.e(ex.Message + " " + ex.StackTrace);
                }
            }
        }

        private static void SendThread()
        {
            while (!stop || sendQueue.Count!= 0)
            {
                Command cmd = sendQueue.Dequeue();
                string sendData = null;
                try
                {
                    sendData = JsonParser.WrapResponse(cmd);
                    Send(cmd.socket, sendData);
                }
                catch (System.Exception ex)
                {
                    Logger.e(ex.Message + " " + ex.StackTrace);
                    try
                    {
                        Send(cmd.socket, "{\"status\":3,\"cmd\":0,\"data\":\"JsonParser.WrapResponse Exception: " + ex.Message + " " + ex.StackTrace + "\"}");
                        Debug.Log(ex.Message + " " + ex.StackTrace);
                        cmd.socket.Close();
                    }
                    catch (System.Exception e)
                    {
                        Logger.e(e.Message + " " + e.StackTrace);
                    }
                }
            }
        }

        public static void Accept(IAsyncResult result)
        {
            Socket serverSocket = (Socket)result.AsyncState;


            Logger.d("Accept one Client " + (++socketCount));
            //已经Accept客户端之后就停止Accept;  
            Socket receiverSocket = serverSocket.EndAccept(result);

            //开始Receive;  
            StateObject state = new StateObject();
            state.m_CurSocket = receiverSocket;
            receiverSocket.BeginReceive(state.m_Buffer, 0, StateObject.m_BufferSize, 0, new AsyncCallback(ReceiveCallBack), state);
            serverSocket.BeginAccept(Accept, serverSocket);
        }

        public static void ReceiveCallBack(IAsyncResult result)
        {
            String content = String.Empty;
            StateObject state = (StateObject)result.AsyncState;
            Socket receiverSocket = state.m_CurSocket;
            try
            {
                SocketError error;
                int byteRead = receiverSocket.EndReceive(result,out error);

                if (byteRead > 0)
                {
                    //获取数据长度;
                    if (state.datalength == 0)
                    {
                        byte[] datalengtharr = new byte[4];
                        Buffer.BlockCopy(state.m_Buffer, 0, datalengtharr, 0, 4);
                        state.datalength = BitConverter.ToInt32(datalengtharr, 0);
                        Logger.d("byte[0]: " + datalengtharr[0] + " byte[1]: " + datalengtharr[1] + "byte[2]: " + datalengtharr[2] + " byte[3]: " + datalengtharr[3]);
                        Logger.d("receive data length = " + state.datalength);
                        //获取数据主体,如果就发一个4字节的直接抛异常，断开连接
                        byte[] dataarr = new byte[byteRead - 4];
                        Buffer.BlockCopy(state.m_Buffer, 4, dataarr, 0, byteRead - 4);
                        state.m_StringBuilder.Append(Encoding.UTF8.GetString(dataarr, 0, byteRead - 4));
                        state.recvedSize = byteRead - 4;
                    }
                    else
                    {
                        byte[] dataarr = new byte[byteRead];
                        Buffer.BlockCopy(state.m_Buffer, 0, dataarr, 0, byteRead);
                        state.m_StringBuilder.Append(Encoding.UTF8.GetString(dataarr, 0, byteRead));
                        
                        state.recvedSize += byteRead;
                    }

                    //判断数据长度，是否接收完全;  
                    if (state.recvedSize>=state.datalength)
                    {
                        parse(state);

                        StateObject newState = new StateObject();
                        newState.m_CurSocket = receiverSocket;

                        receiverSocket.BeginReceive(newState.m_Buffer, 0, StateObject.m_BufferSize, 0, new AsyncCallback(ReceiveCallBack), newState);
                    }
                    else
                    {
                        //数据没有接收完，继续接收;
                        int needsize=state.datalength-state.recvedSize;
                        int recvsize = needsize < StateObject.m_BufferSize?needsize:StateObject.m_BufferSize;
                        receiverSocket.BeginReceive(state.m_Buffer, 0, recvsize, 0, new AsyncCallback(ReceiveCallBack), state);
                    }
                }
                else
                {
                    Logger.w("Recv socket error,error code = " + error);
                    CloseSocket(receiverSocket);
                }
            }
            catch (Exception ex)
            {
                Logger.w(ex.Message+" "+ex.StackTrace);
            }

        }
        private static void Send(Socket handler, String data)
        {
            Logger.d("send :" + data);
            byte[] byteData = Encoding.UTF8.GetBytes(data);
            byte[] sendByteData = new byte[byteData.Length + 4];
            byte[] lengthByte = BitConverter.GetBytes(byteData.Length);
            Buffer.BlockCopy(lengthByte, 0, sendByteData, 0, 4);
            Buffer.BlockCopy(byteData, 0, sendByteData, 4, byteData.Length);
            try
            {
                handler.BeginSend(sendByteData, 0, sendByteData.Length, 0, new AsyncCallback(SendCallback), handler);
            }
            catch (Exception ex)
            {
                Logger.d(ex.ToString());
                if (handler == CommandHandler.INSTANCE.recordSocket)
                {
                    CommandHandler.INSTANCE.RecordMode = false;
                    Logger.d("Maybe Recorder stops----");
                }

                if (handler == ClientCaller.socket)
                {
                    ClientCaller.socket = null;
                    Logger.d("ClientCaller socket");
                }

                CloseSocket(handler);
            }

        }

        private static void SendCallback(IAsyncResult result)
        {
            try
            {
                Socket handler = (Socket)result.AsyncState;
                SocketError error;
                int bytesSend = handler.EndSend(result, out error);
                Logger.d("Sent bytes to client = " + bytesSend);
                if (error != SocketError.Success)
                {
                    if (handler == CommandHandler.INSTANCE.recordSocket)
                    {
                        CommandHandler.INSTANCE.RecordMode = false;
                        Logger.d("Maybe Recorder stops");
                    }
                    CloseSocket(handler);
                }
                else
                {
                    Logger.d("Network "+error);
                }

                

            }
            catch (System.Exception ex)
            {
                Debug.Log(ex.ToString());
            }
        }



        private static void CheckExitGame(Cmd cmd)
        {
            if (cmd == Cmd.EXIT)
            {
                Logger.w("Recv exit command");
                CloseSocket(serverSocket);
                Environment.Exit(0);
            }
        }

        private static void Dispatch(Command command)
        {
            switch(command.cmd){
                case Cmd.PRC_SET_METHOD:
                    ClientCaller.SetRpcMethod(command);
                    break;
                case Cmd.RPC_METHOD:
                    Logger.d("RPC METHOD return "+command.recvObj);
                    ClientCaller.InvokeSeqCallBack(command);
                    break;
                default:
                    AddCommand(command);
                    break;
            }
            
                
        }

        private static void parse(StateObject stateObject)
        {
            //解析内容，然后放置在在Command中准备处理
            string content=stateObject.m_StringBuilder.ToString();

            Logger.v("parse Receive length = " + stateObject.recvedSize + ",receive content = " + content);

            try
            {
                //纯在极大优化控件，能够降低CPU
                long beg = DateTime.Now.Ticks / 10000;
                JsonData jsonObject = JsonMapper.ToObject(content);
                Cmd cmd = (Cmd)(int)jsonObject["cmd"];
                CheckExitGame(cmd);
                JsonData value = jsonObject["value"];
                string jsonValue = JsonMapper.ToJson(value);
                Command command = new Command(cmd,stateObject.m_CurSocket);
                command.recvObj = jsonValue;
                JsonParser.PreDeserialization(command);
                Logger.v("Enqueue commmand : " + command.cmd);
                Dispatch(command);
                Logger.v("Enqueue commmand :" + command.cmd + " end,use time " + (DateTime.Now.Ticks / 10000 - beg) / 1000);
            }
            catch (System.Exception ex)
            {
                CloseSocket(stateObject.m_CurSocket);//命令都无法解析，直接断开连接
                Logger.w(ex.Message + " " + ex.StackTrace);
            }
        }

        public static void CloseSocket(Socket socket)
        {
            try
            {
                if (socket != null)
                {
                    socket.Close();
                }
            }
            catch (System.Exception ex)
            {
                Logger.e(ex.Message + " " + ex.StackTrace);
            }
        }

        public static Command GetCommand()
        {
            lock (commandQueue)
            {
                if (commandQueue.Count == 0)
                {
                    return null;
                }
                else
                {
                    return commandQueue.Dequeue();
                }
            }
        }

        public static void AddCommand(Command command)
        {
            lock (commandQueue)
            {
                commandQueue.Enqueue(command);
            }
        }

        public static void SendCommand(Command cmd)
        {
            sendQueue.Enqueue(cmd);
        }

        public static void Start()
        {
            try
            {
                Debug.Log("Start server thread");
                RecvThread();

                if (sendThread == null)
                {
                    sendThread = new Thread(SendThread);
                    sendThread.IsBackground = true;
                    sendThread.Start();
                }
            }
            catch (System.Exception ex)
            {
                Logger.d(ex.Message);
            }
        } 
    }

    class StateObject
    {
        public Socket m_CurSocket = null;
        public const int m_BufferSize = 1024;
        public byte[] m_Buffer = new byte[m_BufferSize];
        public StringBuilder m_StringBuilder = new StringBuilder();
        public int recvedSize = 0;//已经接收的字符长度
        public int datalength = 0;//接收的总长度
    }

}
