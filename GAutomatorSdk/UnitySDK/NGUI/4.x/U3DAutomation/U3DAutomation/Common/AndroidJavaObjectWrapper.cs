using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using System.Collections;
using System.Reflection;

namespace WeTest.U3DAutomation
{
    /*
     * AndroidJavaClass是Android平台独有的，不能在IOS和WIN平台上编译通过
     * 
     * 
     * 
     */
	public class AndroidJavaObjectWrapper
	{
        private static Assembly ass;
        private static Type androidJavaClassType;

        public readonly static string AndoridJavaObjectName = "UnityEngine.AndroidJavaObject, UnityEngine, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";

        private static MethodInfo callMethod;
        private static MethodInfo callStaticMethod;
        private static MethodInfo callReturnMethod;
        private static MethodInfo callReturnStaticMethod;


        private object[] constructArgs;
        private object androidJavaObj;

        private static void InitMethod()
        {
            if (ass == null)
            {
                ass = typeof(GameObject).Assembly;
                androidJavaClassType = ass.GetType("UnityEngine.AndroidJavaObject");

                MethodInfo[] ms = androidJavaClassType.GetMethods();
                foreach (MethodInfo m in ms)
                {
                    if (m != null && m.Name.Equals("CallStatic") && m.ReturnType == typeof(void))
                    {
                        callStaticMethod = m;
                    }
                    else if (m != null && m.Name.Equals("CallStatic") && m.ReturnType.ToString().Equals("ReturnType"))
                    {
                        callReturnStaticMethod = m;
                    }
                    else if (m != null && m.Name.Equals("Call") && m.ReturnType == typeof(void))
                    {
                        callMethod = m;
                    }
                    else if (m != null && m.Name.Equals("Call") && m.ReturnType.ToString().Equals("ReturnType"))
                    {
                        callReturnMethod = m;
                    }
                }
            }
        }

        public AndroidJavaObjectWrapper(string className,params object[] args)
        {

            InitMethod();

            androidJavaObj = ass.CreateInstance("UnityEngine.AndroidJavaObject", true, BindingFlags.Default, null, new object[] { className, args }, null, null);

        }

        public void setAndroidJavaObjectWrapper(object obj)
        {

            androidJavaObj = obj;
        }


        public void CallStatic(string methodName, params object[] args)
        {
            callStaticMethod.Invoke(androidJavaObj, new object[] { methodName, args });
        }


        public void Call(string methodName, params object[] args)
        {
            callMethod.Invoke(androidJavaObj, new object[] { methodName,args});
        }
	}
}
