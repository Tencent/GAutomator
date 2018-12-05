using System;
using UnityEngine;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Reflection;
using System.Text.RegularExpressions;
using WeTest.U3DAutomation;
using System.Threading;
using System.Runtime.InteropServices;

namespace WeTest.U3DAutomation
{
    public class CrashMonitor
    {

        public static bool selfCheck = false;//Application.RegisterLogCallback是单播的，会被后面的注册者覆盖
        public static readonly string SELF_CHECK = "WETEST_REGISTER_SELF_CHECK";
        private static int frameNum = 0;
        private static int ChechFreq = 100;//多少帧检测次数
        private static bool startCheck = false;

        private static int nativeSelfCheckFreq = 100;
        private static int nativeSelfCheck = 0;

        private static bool IsLogCallbackRegister = false;

        public static bool CLOSE_MONITOR = false;


        [DllImport("crashmonitor")]
        private static extern void InitWetestCrashMonitor();

        [DllImport("crashmonitor")]
        private static extern void ReInitWetestCrashMonitor();

        public delegate void OnUncaughtExceptionReport(string type, string message, string stackTrace, bool caught);

        //捕获异常之后的报告方式
        public static event OnUncaughtExceptionReport UncaughtExceptionReport;

        public static AndroidJavaObjectWrapper _wetestAgent = null;
        public static readonly string CLASS_UNITYAGENT = "com.tencent.wetest.WetestReport";

        private static Application.LogCallback wetest_call_back = _OnLogCallbackHandler;

        public static AndroidJavaObjectWrapper WetestAgent
        {

            get
            {
                if (_wetestAgent == null)
                {
                    try
                    {
                        _wetestAgent = new AndroidJavaObjectWrapper(CLASS_UNITYAGENT);
                        //object obj = _wetestAgent.CallStaticReturnAndroidJava("getInstance");
                        //_wetestAgent.setAndroidJavaObjectWrapper(obj);
                    }
                    catch (System.Exception ex)
                    {
                        Logger.w(ex.Message + ex.StackTrace);
                    }

                }
                return _wetestAgent;
            }

        }

        public static void LogErrorProxy(string type, string message, string stackTrace, string scene, bool uncaught)
        {
            try
            {
                WetestAgent.CallStatic("logError", type, message, stackTrace, scene, uncaught);
            }
            catch (System.Exception ex)
            {
                Logger.e(ex.Message);
            }
        }

        public void UnregisterExceptionHandler()
        {
            AppDomain.CurrentDomain.UnhandledException -= _OnUncaughtExceptionHandler;
            Application.RegisterLogCallback(null);
        }
        public static void RegisterExceptionHandler()
        {
            if (!IsLogCallbackRegister&&!CLOSE_MONITOR)
            {
                Logger.d("Register Exception Handler");
                IsLogCallbackRegister = true;
                try
                {
                    UncaughtExceptionReport += DefaultReportException;
                    //非捕获异常处理
                    AppDomain.CurrentDomain.UnhandledException += _OnUncaughtExceptionHandler;

                    Logger.d("Current Domain is default domain?" + (AppDomain.CurrentDomain.IsDefaultAppDomain() ? "True" : "False"));

                    //日志处理
                    //Application.RegisterLogCallback(_OnLogCallbackHandler);

                    Logger.d("Register jvm crash monitor");
                    //Java未捕获异常处理
                    WetestAgent.CallStatic("initCrashReport");

                    //native异常捕获
                    //native crash程序那边有二次注册检测，避免在异常处理出错时进入无限递归
                    //bugly如果在我们后面注册，会把我们的处理函数给干掉。我们二次检测并注册时，因为避免二次检测而无法再次注册，所以会出错。
                    Logger.d("Register native crash monitor");
                    InitWetestCrashMonitor();
                }
                catch (System.Exception ex)
                {
                    System.Console.WriteLine("Register error\n" + ex.Message + "\n" + ex.StackTrace);
                    CLOSE_MONITOR = true;
                }

            }
        }

        /// <summary>
        /// /处理未捕获的异常信息
        /// 
        /// 所有的异常Unity均能捕获，只有StackOverflow 、 OutOfMemory无法捕获，会造成崩溃
        /// 
        /// 其他线程的异常，同样无法通过这个函数捕获，所以这个函数暂时无可用之处。
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="args"></param>
        private static void _OnUncaughtExceptionHandler(object sender, System.UnhandledExceptionEventArgs args)
        {
            if (args == null || args.ExceptionObject == null)
            {
                return;
            }

            try
            {
                if (args.ExceptionObject.GetType() != typeof(System.Exception))
                {
                    return;
                }
            }
            catch
            {
                if (UnityEngine.Debug.isDebugBuild == true)
                {
                    UnityEngine.Debug.Log("<WeTestLog>:Failed to get uncaught exception");
                }

                return;
            }


            _HandleException((System.Exception)args.ExceptionObject, null, true);
        }

        private static void _HandleException(System.Exception e, string message, bool uncaught)
        {
            if (e == null)
            {
                return;
            }

            string exceptionName = e.GetType().Name;
            string reason = e.Message;

            if (!string.IsNullOrEmpty(message))
            {
                reason = string.Format("{0}{1}---{2}", reason, Environment.NewLine, message);
            }

            StringBuilder stackTraceBuilder = new StringBuilder("");

            StackTrace stackTrace = new StackTrace(e, true);
            int count = stackTrace.FrameCount;
            for (int i = 0; i < count; i++)
            {
                StackFrame frame = stackTrace.GetFrame(i);

                stackTraceBuilder.AppendFormat("{0}.{1}", frame.GetMethod().DeclaringType.Name, frame.GetMethod().Name);

                ParameterInfo[] parameters = frame.GetMethod().GetParameters();
                if (parameters == null || parameters.Length == 0)
                {
                    stackTraceBuilder.Append(" () ");
                }
                else
                {
                    stackTraceBuilder.Append(" (");

                    int pcount = parameters.Length;

                    ParameterInfo param = null;
                    for (int p = 0; p < pcount; p++)
                    {
                        param = parameters[p];
                        stackTraceBuilder.AppendFormat("{0} {1}", param.ParameterType.Name, param.Name);

                        if (p != pcount - 1)
                        {
                            stackTraceBuilder.Append(", ");
                        }
                    }
                    param = null;

                    stackTraceBuilder.Append(") ");
                }

                string fileName = frame.GetFileName();
                if (!string.IsNullOrEmpty(fileName) && !fileName.ToLower().Equals("unknown"))
                {
                    fileName = fileName.Replace("\\", "/");

                    int loc = fileName.ToLower().IndexOf("/assets/");
                    if (loc < 0)
                    {
                        loc = fileName.ToLower().IndexOf("assets/");
                    }

                    if (loc > 0)
                    {
                        fileName = fileName.Substring(loc);
                    }

                    stackTraceBuilder.AppendFormat("(at {0}:{1})", fileName, frame.GetFileLineNumber());
                }
                stackTraceBuilder.AppendLine();

            }

            UncaughtExceptionReport("UnhandleCaught  " + exceptionName, reason, stackTraceBuilder.ToString(), true);
        }


        /// <summary>
        /// 日志处理函数，捕获Exception级别的错误
        /// </summary>
        /// <param name="logString"></param>
        /// <param name="stackTrace"></param>
        /// <param name="type"></param>
        public static void _OnLogCallbackHandler(string condition, string stackTrace, LogType type)
        {

            if (LogType.Log == type)
            {
                return;
            }

            if (!string.IsNullOrEmpty(condition) && condition.Contains("<WeTestLog>"))
            {
                return;
            }

            if (condition.Contains(SELF_CHECK))
            {

                selfCheck = true;
                return;
            }


            _HandleException(type, condition, stackTrace);
        }


        public static Application.LogCallback getLogCallBackHandler()
        {
            return _OnLogCallbackHandler;
        }
        /// <summary>
        /// 日志分析函数，解析出相关的内容
        /// </summary>
        /// <param name="logLevel"></param>
        /// <param name="name"></param>
        /// <param name="message"></param>
        /// <param name="stackTrace"></param>
        /// <param name="uncaught"></param>
        private static void _HandleException(LogType logLevel, string message, string stackTrace)
        {

            string type = null;
            string reason = null;
            if (logLevel != LogType.Exception) return;

            if (!string.IsNullOrEmpty(message))
            {
                try
                {
                    if ((LogType.Exception == logLevel) && message.Contains("Exception"))
                    {
                        Match match = new Regex(@"^(?<errorType>\S+):\s*(?<errorMessage>.*)").Match(message);

                        if (match.Success)
                        {
                            type = match.Groups["errorType"].Value;
                            reason = match.Groups["errorMessage"].Value.Trim();
                        }
                    }
                }
                catch
                {

                }

                if (string.IsNullOrEmpty(reason))
                {
                    reason = message;
                }
            }


            if (string.IsNullOrEmpty(type))
            {
                type = string.Format("Unity{0}", logLevel.ToString());
            }

            bool uncaught = true;

            UncaughtExceptionReport(type, reason, stackTrace, uncaught);
        }

        /// <summary>
        /// 打印出Wetest_Report_Expection,用于检测是否有crash情况
        /// </summary>
        /// <param name="type"></param>
        /// <param name="message"></param>
        /// <param name="stackTrace"></param>
        public static void DefaultReportException(string type, string message, string stackTrace, bool uncaught)
        {
            try
            {
                string sceneName = Application.loadedLevelName;
                LogErrorProxy(type, message, stackTrace, sceneName, uncaught);
            }
            catch (System.Exception ex)
            {
                System.Console.WriteLine(ex.Message + "\n" + ex.StackTrace);
            }

        }

        /// <summary>
        /// 自我检测，Bugly等插件会把RegisterLogCallback覆盖
        /// </summary>
        public static void SelfCheck()
        {
            if (CLOSE_MONITOR)
                return;
            frameNum++;
            if (frameNum % ChechFreq == 0)
            {
                //启动自我检测
                startCheck = true;
                UnityEngine.Debug.LogWarning(SELF_CHECK);
                if (ChechFreq < int.MaxValue / 10)
                {
                    ChechFreq *= 2;
                }
                return;
            }

            if (startCheck)
            {
                if (!selfCheck)
                {
                    ReRegisterExceptionHandler();
                    frameNum = 0;
                    selfCheck = false;
                    startCheck = false;
                    ChechFreq *= 2;
                }
            }
        }

        public static void NativeCrashMonitorCheck()
        {
            if (CLOSE_MONITOR)
                return;
            nativeSelfCheck++;
            if (nativeSelfCheck % nativeSelfCheckFreq == 0)
            {
                nativeSelfCheck = 0;
                try
                {
                    ReInitWetestCrashMonitor();
                }
                catch (System.Exception ex)
                {
                    Logger.w(ex.Message + " " + ex.StackTrace);
                    CLOSE_MONITOR = true;
                }
                
            }

        }
        //public static void gets_LogCallback()
        //{
        //    Type type = typeof(Application);

        //    FieldInfo[] fields = type.GetFields(BindingFlags.NonPublic | BindingFlags.Static);

        //    foreach (FieldInfo field in fields)
        //    {
        //        if (field.Name.Equals("s_LogCallback"))
        //        {

        //            object obj = field.GetValue(type);
        //            Application.LogCallback o = (Application.LogCallback)obj;

        //            object target_o = o.Target;
        //            if (target_o != null)
        //            {
        //                Type target_type = target_o.GetType();

        //                Logger.d("target type: {0}", target_type.AssemblyQualifiedName);
        //            }


        //            string result = obj.ToString() + " hashcode: " + obj.GetHashCode() + " type_name" + obj.GetType().FullName;
        //            Logger.d(result);
        //            Logger.d("register by wetest {0}", obj == wetest_call_back);
        //            old = (Application.LogCallback)obj;
        //        }
        //    }

        //}

        public static void ReRegisterExceptionHandler()
        {
            Logger.d("Register Exception Handler,Agine");
            IsLogCallbackRegister = true;
            try
            {
                //日志处理
                //gets_LogCallback();
                Application.RegisterLogCallback(_OnLogCallbackHandler);
                InitWetestCrashMonitor();
                //gets_LogCallback();
            }
            catch (System.Exception ex)
            {
                System.Console.WriteLine("Register error");
                CLOSE_MONITOR = true;
            }

        }
    }
}
