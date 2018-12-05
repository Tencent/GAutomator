using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WeTest.U3DAutomation
{
    
	public class CustomHandler
	{
        public delegate string HandleCustom(string message);
        public delegate void PcCallBack(int status,string message); //调用PC端程序后，返回结果后的回调函数。切勿阻塞操作

        private static Dictionary<string, HandleCustom> dict = new Dictionary<string, HandleCustom>();
        public static List<string> keys = new List<string>();

        public static void RegisterCallBack(string key, HandleCustom handle)
        {

            if (dict.ContainsKey(key))
            {
                dict[key] = handle;
            }
            else
            {
                dict.Add(key, handle);
                keys.Add(key);
            }
            Logger.v("Register " + key);
        }

        public static bool UnRegisterCallBack(string key)
        {
            if (dict.ContainsKey(key))
            {
                dict.Remove(key);
                keys.Remove(key);
                return true;
            }
            else
            {
                return false;
            }
        }

        public static bool Call(string key, string arg,out string result)
        {
            result = "";
            if (dict.ContainsKey(key))
            {

                HandleCustom handler = dict[key];
                try
                {
                    result = handler(arg);
                }
                catch (System.Exception ex)
                {
                    Logger.w(ex.Message + "\n" + ex.StackTrace);
                }
                return true;
            }
            else
            {
                Logger.w("UnRegitster Function ==>"+key);
                return false;
            }
        }

        public static List<string> GetRegistered()
        {
            return keys;
        }

        public static void InvokeClientMethod(string name, string value,PcCallBack callback)
        {
            ClientCaller.Invoke(name, value,callback);
        }

        public static void InvokeClientMethod(string name, string value)
        {
            ClientCaller.Invoke(name, value, null);
        }

        public static string InvokeClientMethodReturnValue(string name, string value,int timeout)
        {
           return ClientCaller.InvokeReturnValue(name, value, timeout);
        }
	}
}
