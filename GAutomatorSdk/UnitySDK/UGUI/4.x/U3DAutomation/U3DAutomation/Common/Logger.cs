//#define WETEST_U3D_VERBOSE_MODE
#define WETEST_U3D_DEBUG_MODE
#define WETEST_U3D_ERROR_MODE
#define WETEST_U3D_WARN_MODE

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;



namespace WeTest.U3DAutomation
{
    class Logger
    {
        //
   
        public static void v(string message)
        {
            #if WETEST_U3D_VERBOSE_MODE
            Debug.Log(message);
            #endif
        }

        public static void v(string format,params object[] args)
        {
            #if WETEST_U3D_VERBOSE_MODE
            v(String.Format(format, args));
            #endif
        }


        public static void d(string message)
        {
#if WETEST_U3D_DEBUG_MODE
            Debug.Log(message);
#endif

        }

        public static void d(string format,params object[] args)
        {
#if WETEST_U3D_DEBUG_MODE
            Debug.Log(String.Format(format, args));
#endif
        }

        public static void e(string message)
        {
#if WETEST_U3D_ERROR_MODE
            Debug.LogError("<WeTestLog> [\n"+message+" \n]");
#endif
        }

        public static void e(string format,params object[] args)
        {
#if WETEST_U3D_ERROR_MODE
            e(String.Format(format, args));
#endif
        }

        public static void w(string message)
        {
#if WETEST_U3D_WARN_MODE
            Debug.LogWarning(message);
#endif
        }

        public static void w(string format,params object[] args)
        {
#if WETEST_U3D_WARN_MODE
            w(String.Format(format, args));
#endif
        }


    }
}
