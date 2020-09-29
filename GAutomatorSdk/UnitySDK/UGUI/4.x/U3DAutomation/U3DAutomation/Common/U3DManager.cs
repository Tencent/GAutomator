using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

namespace WeTest.U3DAutomation
{
	class U3DManager
	{
        public static void Init()
        {
            if (Application.platform == RuntimePlatform.Android)
            {
                WeTest.U3DAutomation.TouchEventHandler.INSTANCE.Start();
            }
          
            WeTest.U3DAutomation.CommandDispatcher.Start();
           
        }

        public static string GetSceneName()
        {
            return Application.loadedLevelName;
        }
	}
}
