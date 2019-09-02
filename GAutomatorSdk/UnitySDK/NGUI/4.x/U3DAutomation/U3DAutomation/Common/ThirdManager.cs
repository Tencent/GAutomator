using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;
using System.IO;
using System.Collections;
using System.Threading;
using UnityEngine;
using WeTest.U3DAutomation;

namespace Dynamic
{
    public class ThirdManager
    {
        public static ThirdManager instance_ = new ThirdManager();
        public Assembly third_assembly_ = null;

        public static ThirdManager INSTANCE
        {
            get { return instance_; }
        }

        public void Initialize()
        {
            if (RuntimePlatform.Android == Application.platform)
            {
                Dynamic.ThirdManager.INSTANCE.LoadCSharpScript("/data/local/tmp/wetest.u3dautomation.dll");
            }
            //else if (RuntimePlatform.IPhonePlayer == Application.platform){// sll dynamic load in iOS  is forbidden
            //    Dynamic.ThirdManager.INSTANCE.LoadCSharpScript(Application.persistentDataPath+"/wetest.u3dautomation.dll");
            //}

            Dynamic.ThirdManager.INSTANCE.InvokeStaticFunction("Dynamic.ThirdManager", "Entry");

            return;
        }

        public bool IsFileLoaded()
        {
            if (null == third_assembly_)
            {
                return false;
            }
            return true;
        }

        public void LoadCSharpScript(String path)
        {
            Debug.Log("try to load csharp script: " + path);
            try
            {
                if (File.Exists(path))
                {
                    // 加载dll
                    FileStream fs = new FileStream(path, FileMode.Open);
                    byte[] bin = new byte[fs.Length];
                    fs.Read(bin, 0, bin.Length);
                    fs.Close();

                    // 生成assembly
                    third_assembly_ = System.Reflection.Assembly.Load(bin);
                }
            }
            catch (System.Exception ex)
            {
                third_assembly_ = null;
                Debug.Log("Find no dynamic lib file.");
                Debug.Log(ex);
            }

            return;
        }

        public object InvokeStaticFunction(String cls, String func)
        {
            if (false == IsFileLoaded())
            {
                return null;
            }

            // 以下的类，成员函数，成员变量需要为public
            // 获取类信息
            Type local_tp = third_assembly_.GetType(cls);

            // 获取函数并调用
            MethodInfo method = local_tp.GetMethod(func);
            return method.Invoke(null, null);
        }

        public object InvokeFunction(System.Object obj, String cls, String func)
        {
            if (false == IsFileLoaded())
            {
                return null;
            }

            // 以下的类，成员函数，成员变量需要为public
            // 获取类信息
            Type local_tp = third_assembly_.GetType(cls);

            // 获取函数并调用
            MethodInfo method = local_tp.GetMethod(func);
            return method.Invoke(obj, null);
        }

        public static System.Object GetInstance()
        {
            return (System.Object)(Dynamic.ThirdManager.INSTANCE);
        }

        // [7/19/2015 levyzhang]
        // 第三方dll的调用接口函数
        public static bool Entry()
        {
            Debug.Log("third entry.");
            return false;
        }

        //public static void OnGUI()
        //{
        //    if (false == Dynamic.ThirdManager.INSTANCE.IsFileLoaded())
        //    {
        //        WeTest.U3DAutomation.CommandHandler.INSTANCE.OnGUI();
        //    }
        //    else
        //    {
        //        Dynamic.ThirdManager.INSTANCE.InvokeStaticFunction("Dynamic.ThirdManager", "OnGUI");
        //    }

        //    return;
        //}

        public static void HandleEvent()
        {
            if (Application.platform == RuntimePlatform.Android)
            {
                if (false == Dynamic.ThirdManager.INSTANCE.IsFileLoaded())
                {
                    WeTest.U3DAutomation.CommandHandler.INSTANCE.HandleEvent();
                }
                else
                {
                    Dynamic.ThirdManager.INSTANCE.InvokeStaticFunction("Dynamic.ThirdManager", "HandleEvent");
                }
            }


            return;
        }

        public static IEnumerator HandleCommand()
        {
            IEnumerator result = null;

            if (false == Dynamic.ThirdManager.INSTANCE.IsFileLoaded())
            {
                result = WeTest.U3DAutomation.CommandHandler.INSTANCE.HandleCommand();
            }
            else
            {
                result = (IEnumerator)Dynamic.ThirdManager.INSTANCE.InvokeStaticFunction("Dynamic.ThirdManager", "HandleCommand");
            }

            return result;
        }

        public static void Start()
        {
            if (false == Dynamic.ThirdManager.INSTANCE.IsFileLoaded())
            {
                WeTest.U3DAutomation.U3DManager.Init();
            }
            else
            {
                Dynamic.ThirdManager.INSTANCE.InvokeStaticFunction("Dynamic.ThirdManager", "Start");
            }

            return;
        }

        public static void getAndroidMScreen()
        {
            if (false == Dynamic.ThirdManager.INSTANCE.IsFileLoaded())
            {
                WeTest.U3DAutomation.AndroidRobot.getAndroidMScreen();
            }
            else
            {
                Dynamic.ThirdManager.INSTANCE.InvokeStaticFunction("Dynamic.ThirdManager", "getAndroidMScreen");
            }

            return;
        }

        public static void FrameUpdate()
        {
            ComputeFPS();
        
        }

        public static void ComputeFPS()
        {
            if (false == Dynamic.ThirdManager.INSTANCE.IsFileLoaded())
            {
               WeTest.U3DAutomation.CommandHandler.INSTANCE.ComputeFPS();
            }
            else
            {
                Dynamic.ThirdManager.INSTANCE.InvokeStaticFunction("Dynamic.ThirdManager", "ComputeFPS");
            }

            return;
        }
    }
}
