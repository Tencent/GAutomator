using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Reflection;
using WeTest.U3DAutomation;

namespace WeTest.U3DAutomation
{
    public class U3DAutomationBehaviour : MonoBehaviour
    {
        private static bool inited = false;
        private bool IsThisObjectWork = false;
        private static int survive = 0;
        private static int MAX_SURVIVE = 500;

        void SubStart()
        {
            Dynamic.ThirdManager.INSTANCE.Initialize();

            Dynamic.ThirdManager.Start();

            //Dynamic.ThirdManager.getAndroidMScreen();

            StartCoroutine(Dynamic.ThirdManager.HandleCommand());
        }

        void Start()
        {
            if (Application.platform == RuntimePlatform.Android){
                Debug.Log("WTSDK Running ,android platform...");
            }
            else if(Application.platform == RuntimePlatform.IPhonePlayer){
                Debug.Log("WTSDK Running ios player...");
            }
            else{
                Debug.Log("WTSDK can not running, if not Android nor iphoneplayer.");
                return;
            }


            if (!inited)
            {
                GameObject.DontDestroyOnLoad(this.gameObject);
                IsThisObjectWork = true;
                inited = true;
                Debug.Log("Start Init ");
                SubStart();

                Debug.Log("U3DAutomation Init OK. Version = " + VersionInfo.SDK_VERSION+" UIType = "+VersionInfo.SDK_UI);
            }
            else
            {
                Debug.Log("U3DAutomation already init.");
            }
        }

        void SubUpdate()
        {
            Dynamic.ThirdManager.HandleEvent();

            //每帧检测
            Dynamic.ThirdManager.FrameUpdate();
        }

        void Update()
        {
            if (Application.platform != RuntimePlatform.Android && Application.platform != RuntimePlatform.IPhonePlayer) 
            {
                return;
            }

            if (IsThisObjectWork)
            {
                SubUpdate();
            }
        }

 
        void OnApplicationPause(bool pauseStatus)
        {
            Logger.d("OnApplicationPause:{0}", pauseStatus);
        }

        void OnApplicationFocus(bool focusStatus)
        {
            Logger.d("OnApplicationFocus:{0}", focusStatus);
        }


        void OnDestroy()
        {
            Logger.d("Destroy Wetest sdk");
            CommandDispatcher.CloseServerSocket();
        }

        void OnGUI()
        {
            if (survive < MAX_SURVIVE)
            {
                GUI.Label(new Rect(20, 20, 300, 200), "<color=red><size=30>WeTest GAutomator</size></color>");
                survive++;
            }

        }

    }
}
