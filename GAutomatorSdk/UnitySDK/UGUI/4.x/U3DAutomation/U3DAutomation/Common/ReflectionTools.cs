using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using System.Reflection;
using System.IO;
using UnityEngine;


namespace WeTest.U3DAutomation
{
    public class ReflectionTools
    {
        private static Assembly testAssembly = null;
        /// <summary>
        /// 获取Object所有的属性值
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public static Hashtable getTypeInfo(System.Object obj)
        {
            if (obj == null)
                return null;
            Type type = obj.GetType();
            Hashtable table = new Hashtable();

            Hashtable properties = new Hashtable();
            PropertyInfo[] propertyInfos=type.GetProperties();

            try
            {
                foreach (PropertyInfo pi in propertyInfos)
                {
                    object value1 = pi.GetValue(obj, null);
                    string name = pi.Name;
                    Logger.d("Property Info => " + name + " value=" + value1);
                    if (properties.Contains(name)) continue;
                    properties.Add(name, value1.ToString());
                }
                table.Add("properties", properties);
            }
            catch (System.Exception ex)
            {
                Logger.e(ex.Message + "\n" + ex.StackTrace);
            }
            
            try
            {
                Type[] types = type.GetInterfaces();
                Hashtable interfaces = new Hashtable();
                table.Add("Intefaces", interfaces);
                foreach (Type inter in types)
                {
                    Logger.d("Interface Info => " + inter.AssemblyQualifiedName + " value=" + inter.ToString());
                    if (interfaces.Contains(inter.AssemblyQualifiedName)) continue;
                    interfaces.Add(inter.AssemblyQualifiedName, inter.Name);
                }
            }
            catch (System.Exception ex)
            {
                Logger.e(ex.Message + "\n" + ex.StackTrace);
            }

            
            try
            {
                MethodInfo[] methods = type.GetMethods();
                Hashtable methodsTable = new Hashtable();
                table.Add("Methods", methodsTable);

                foreach (MethodInfo methodInfo in methods)
                {
                    Logger.d("Method info => " + methodInfo.Name);
                    if (methodsTable.Contains(methodInfo.Name)) continue;
                    methodsTable.Add(methodInfo.Name, methodInfo.Name);
                }
            }
            catch (System.Exception ex)
            {
                Logger.e(ex.Message + "\n" + ex.StackTrace);
            }

            
            return table;
        }


        public static void printPropertyInfo(System.Object obj)
        {
            Hashtable table = getTypeInfo(obj);
            if (table == null) return;

            foreach (DictionaryEntry pair in table)
            {
                Hashtable tab = pair.Value as Hashtable;
                foreach (DictionaryEntry entry in tab)
                {
                    Logger.w(entry.Key + " = " + entry.Value);
                }
                
            }
        }

        public static object GetComponentAttribute(GameObject gameobject, Type t, String attributeName)
        {
            if (gameobject == null || t == null)
            {
                return null;
            }

            Component comp = gameobject.GetComponent(t);

            if (comp == null)
            {
                return null;
            }

            PropertyInfo pi = GetPropertyNest(t, attributeName);

            if (pi == null || !pi.CanRead)
            {
                return null;
            }

            return pi.GetValue(comp, null);
        }

        public static object GetComponentAttribute(GameObject gameobject, String componentName, String attributeName)
        {
            if (gameobject == null || componentName == null || attributeName == null)
                return null;

            Component[] components=gameobject.GetComponents<Component>();
            Component c=null;
            foreach (Component comp in components)
            {
                string name = comp.GetType().Name;
                if (name.Equals(componentName))
                {
                    c = comp;
                    break;
                }
            }
            if (c == null)
            {
                throw new Exception("Can't find " + componentName);
            }

            PropertyInfo pi = GetPropertyNest(c.GetType(), attributeName);

            if (pi != null && pi.CanRead)
            {
                return pi.GetValue(c, null);
            }

            FieldInfo info = GetFieldInfoNest(c.GetType(), attributeName);

            if (info != null)
            {
  
                return info.GetValue(c);
            }
            throw new Exception("unAccess field " + attributeName);
        }

        private static PropertyInfo GetPropertyNest(Type t, String name)
        {

            PropertyInfo pi = t.GetProperty(name);

            if (pi != null)
            {
                return pi;
            }

            if (t.BaseType != null)
            {
                return GetPropertyNest(t.BaseType, name);
            }

            return null;
        }

        private static FieldInfo GetFieldInfoNest(Type t, String name)
        {
            FieldInfo info = t.GetField(name);

            if (info != null)
            {
                return info;
            }

            if (t.BaseType != null)
            {
                return GetFieldInfoNest(t.BaseType, name);
            }
            return null;
        }

        public static List<object> GetComponentInChildrenAttribute(GameObject gameobject, Type t, String attributeName)
        {
            if (t == null)
            {
                return null;
            }
            List<object> lists = new List<object>();
            Component[] comps = gameobject.GetComponentsInChildren(t);

            if (comps == null)
            {
                return null;
            }

            PropertyInfo pi = GetPropertyNest(t, attributeName);

            if (pi == null || !pi.CanRead)
            {
                return null;
            }

            for (int i = 0; i < comps.Length; ++i)
            {
                object obj = pi.GetValue(comps[i], null);
                if (obj != null)
                {
                    lists.Add(obj);
                }
            }
            return lists;

        }

        public static bool SetComponentAttribute(GameObject obj, Type t, String attributeName, object value)
        {
            if (t == null)
            {
                return false;
            }

            Component comp = obj.GetComponent(t);

            if (comp == null)
            {
                return false;
            }

            PropertyInfo pi = GetPropertyNest(t, attributeName);

            if (!pi.CanWrite)
            {
                return false;
            }
            
            pi.SetValue(comp, value, null);

            return true;
        }

        public static Type TypeOf(string name)
        {
            string typeName = name;

            Type objType = Type.GetType(name);
            if (objType != null)
            {
                return objType;
            }

            if (!name.Contains("Assembly-CSharp"))
            {
                typeName = name + ", Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
            }

            objType = Type.GetType(typeName);

            if (objType == null)
            {
                typeName = name + ", Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
                objType = Type.GetType(typeName);
            }
            return objType;
        }

        /**
         * 利用反射获取某个component的所有方法。
         * 
        */
        public static MethodDetail[] GetComponentMethods(GameObject gameobject, String componentName)
        {
            if (gameobject == null || componentName == null)
                return null;

            Component[] components = gameobject.GetComponents<Component>();
            Component c = null;
            foreach (Component comp in components)
            {
                string name = comp.GetType().Name;
                if (name.Equals(componentName))
                {
                    c = comp;
                    break;
                }
            }
            if (c == null)
            {
                throw new Exception("Can't find " + componentName);
            }
            MethodInfo[] methods = c.GetType().GetMethods();
            if (methods == null || methods.Length == 0)
            {
                return null;
            }
            Debug.Log("Reflection Methods Length: " + methods.Length);
            MethodDetail[] methodDetails = new MethodDetail[methods.Length];
            for (int i = 0; i < methods.Length; i++)
            {
                Debug.Log("Reflection Method Name: " + methods[i].Name);
                methodDetails[i] = new MethodDetail();
                methodDetails[i].methodName = methods[i].Name;               
                methodDetails[i].returnType = methods[i].ReturnType.Name;
                ParameterInfo[] pi = methods[i].GetParameters();
                if (pi != null && pi.Length > 0)
                {
                    methodDetails[i].parameterTypes = new string[pi.Length];
                    for (int j = 0; j < pi.Length; j++)
                    {
                        methodDetails[i].parameterTypes[j] = pi[j].ParameterType.Name;
                    }
                }
            }
            return methodDetails;
        }

        public static object CallComponentMethod(GameObject gameobject, String componentName, String methodName, object[] parameters)
        {
            if (gameobject == null || componentName == null)
                return null;

            Component[] components = gameobject.GetComponents<Component>();
            Component c = null;
            foreach (Component comp in components)
            {
                string name = comp.GetType().Name;
                if (name.Equals(componentName))
                {
                    c = comp;
                    break;
                }
            }
            if (c == null)
            {
                throw new Exception("Can't find " + componentName);
            }
            MethodInfo method = c.GetType().GetMethod(methodName);
            Debug.Log("Found Method: "+ method.Name);
            ParameterInfo[] pi = method.GetParameters();
            object[] paras = null;
            if (pi != null && pi.Length > 0)
            {
                if (parameters == null || pi.Length > parameters.Length)
                {
                    throw new System.ArgumentException("Parameters dismatch!");
                }

                paras = new object[pi.Length];
                for (int i = 0; i < pi.Length; i++)
                {
                    //paras[i] = Convert.ChangeType(parameters[i], pi[i].ParameterType);       
                    paras[i] = parameters[i];
                }

                if (method.IsStatic)
                {
                    c = null;
                }
            }
            object obj = method.Invoke(c, paras);
            return obj;
        }

        private static void loadAssembly(String path)
        {
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
                    testAssembly = System.Reflection.Assembly.Load(bin);
                }
            }
            catch (System.Exception ex)
            {
                testAssembly = null;

                Debug.Log("Find no dynamic test lib file.");
                Debug.Log(ex);
                throw new Exception("load /data/local/tmp/gametestlib library failed.");
            }
        }

        public static void testLibInit()
        {
            loadAssembly("/data/local/tmp/gametestlib.dll");
            Type local_tp = testAssembly.GetType("GameTest.Test");

            // 获取函数并调用
            MethodInfo method = local_tp.GetMethod("init");
            if (method != null)
            {
                try
                {
                    Debug.Log("invoke gametestlib init");
                    method.Invoke(null, null);
                }
                catch (System.Exception ex)
                {
                    Debug.Log(ex);
                }
            }
            
        }

	}

    
}
