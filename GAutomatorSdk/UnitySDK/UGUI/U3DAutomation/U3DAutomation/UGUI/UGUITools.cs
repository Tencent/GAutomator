using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using UnityEngine.EventSystems;
using System.Reflection;
using UnityEngine.UI;

namespace WeTest.U3DAutomation
{
    class UGUITools
    {

        private static string rendModeScreenSpaceOverlay = "ScreenSpaceOverlay";
        private static string rendModeScreenSpaceCamera = "ScreenSpaceCamera";
        private static string rendModeWorldSpace = "WorldSpace";


        public static string ScreenSpaceOverlay
        {
            get
            {
                return rendModeScreenSpaceOverlay;
            }
        }

        public static string ScreenSpaceCamera
        {
            get
            {
                return rendModeScreenSpaceCamera;
            }
        }

        public static string WorldSpace
        {
            get
            {
                return rendModeWorldSpace;
            }
        }

        //获取所有的UIRoot节点
        public static Canvas[] GetCanvasGameObjects()
        {
            Canvas[] canvas = GameObject.FindObjectsOfType<Canvas>();

            return canvas;
        }

        //判断是否是UGUI的控件
        public static bool isUGUIElement(GameObject obj)
        {
            if (obj == null)
                return false;
            RectTransform rect = obj.GetComponent<RectTransform>();
            if (rect == null)
            {
                return false;
            }

            return true;
        }

        //判断是否是可见的UGUI控件
        public static bool isVisiableUGUIElement(GameObject obj)
        {
            if (obj == null || !isUGUIElement(obj) || !obj.activeInHierarchy)
            {
                return false;
            }
            return true;
        }

        public static bool isVisiableUIElementWithChildren(GameObject gameObj)
        {
            if (gameObj == null || !isUGUIElement(gameObj) || !gameObj.activeInHierarchy)
            {
                return false;
            }


            Queue<GameObject> queue = new Queue<GameObject>();
            queue.Enqueue(gameObj);
            while (queue.Count != 0)
            {
                GameObject obj = queue.Dequeue();
                if (isVisiableUGUIElement(obj))
                {
                    return true;
                }
                int childCount = obj.transform.childCount;
                for (int i = 0; i < childCount; ++i)
                {
                    queue.Enqueue(obj.transform.GetChild(i).gameObject);
                }
            }

            return false;
        }
        /// <summary>
        /// 分别返回Unity屏幕概念下UGUI的4个点，左下角，左上角，右上角，右下角
        /// </summary>
        /// <param name="gameObject"></param>
        /// <returns></returns>
        public static Vector2[] GetWorldCorner(GameObject gameObject)
        {
            //Logger.d("GetWorldCorner");
            if (!isUGUIElement(gameObject))
                return null;

            Canvas canvas = gameObject.GetComponentInParent<Canvas>();

            if (canvas == null || canvas.renderMode == null)
            {
                return null;
            }

            GameObject o = canvas.gameObject;
            Logger.d("Canvas name " + o.name);
            RenderMode mode = canvas.renderMode;

            Camera c = null;
            //Screen Space Overlay模式非常特别，没有对应的摄像机
            if (mode.Equals(RenderMode.ScreenSpaceOverlay))
            {
                Logger.d("ScreenSpaceOverlay");
                c = null;
            }
            else if (mode.Equals(RenderMode.ScreenSpaceCamera))
            {
                Logger.d("ScreenSpaceCamera");
                c = canvas.worldCamera;
            }
            else if (mode.Equals(RenderMode.WorldSpace))
            {
                Logger.d("WorldSpace");
                c = UIBase.FindBestCamera(gameObject);
            }
            else
            {
                return null;
            }

            RectTransform rectTran = gameObject.GetComponent<RectTransform>();

            Vector3[] core = new Vector3[4];
            rectTran.GetWorldCorners(core);
            Vector2[] vectors = new Vector2[4];
            vectors[0] = RectTransformUtility.WorldToScreenPoint(c, core[0]);
            vectors[1] = RectTransformUtility.WorldToScreenPoint(c, core[1]);
            vectors[2] = RectTransformUtility.WorldToScreenPoint(c, core[2]);
            vectors[3] = RectTransformUtility.WorldToScreenPoint(c, core[3]);

            return vectors;

        }

        public static Rectangle GetUGUIBound(GameObject gameObject)
        {
            Logger.d("get ugui bound");
            Vector2[] vectors = GetWorldCorner(gameObject);
            if (vectors == null)
            {
                return null;
            }
            Rectangle rc = new Rectangle();

            /* 
            float[] xx = { vectors[0].x, vectors[1].x, vectors[2].x };
            float[] yy = { vectors[0].y, vectors[1].y, vectors[2].y };

            rc.x = Mathf.Min(xx);
            rc.y = Screen.height - Mathf.Max(xx);
            rc.width = Mathf.Max(xx) - Mathf.Min(xx);
            rc.height = Mathf.Max(yy) - Mathf.Min(yy);
            */

            rc.x = vectors[1].x;
            rc.y = Screen.height - vectors[1].y;
            rc.width = vectors[3].x - vectors[0].x;
            rc.height = vectors[1].y - vectors[0].y;

            Logger.v("Get UGUI Bound orginal rc.x=" + rc.x + ", rc.y=" + rc.y + ", wight = " + rc.width + ", height=" + rc.height);

            return rc;
        }

        public static GameObject GetUIElementbyRaycast(Point point)
        {
            if (EventSystem.current == null)
            {
                Logger.d("No Event System");
                return null;
            }
            Point pt = new Point(0, 0);
            if (point.X > 0 && point.X < 1 && point.Y > 0 && point.Y < 1) { //归一化的坐标
                pt = new Point(Screen.width * point.X, Screen.height * (1 - point.Y));
            }
            else if (RuntimePlatform.Android==Application.platform)
            {//android绝对坐标
                pt =CoordinateTool.ConvertMobile2Unity(point);
            }
            else
            {//一般绝对坐标
                pt = new Point( point.X, (1 - point.Y));
            }
               
            return GetUIElementbyRaycastByUnity(pt);
        }

        public static GameObject GetUIElementbyRaycastByUnity(Point point)
        {
            if (EventSystem.current == null)
            {
                Logger.d("No Event System");
                return null;
            }

            PointerEventData data = new PointerEventData(EventSystem.current);
            Vector2 vector = new Vector2(point.X, point.Y);
            data.position = vector;

            Logger.d("Raycast Find objects on point===>(" + data.position.x + "," + data.position.y + ")");

            List<RaycastResult> results = new List<RaycastResult>();
            EventSystem.current.UpdateModules();

            EventSystem.current.RaycastAll(data, results);
            foreach (RaycastResult res in results)
            {
                Logger.v("gameobject name=" + res.gameObject + " index=" + res.index + " module=" + res.module + " depth=" + res.depth + " isvaild=" + res.isValid.ToString());
            }

            if (results.Count != 0)
            {
                GameObject raycastObject = results[0].gameObject;
                do
                {
                    if (raycastObject.gameObject.GetComponent(typeof(IEventSystemHandler)) != null)
                    {
                        return raycastObject;
                    }
                    raycastObject = raycastObject.transform.parent.gameObject;
                } while (raycastObject.transform.parent != raycastObject.transform);
                return null;
            }
            else
            {
                return null;
            }
        }

        public static String SetInputTxt(GameObject obj, String txt)
        {
            Logger.d("SetInputTxt" + obj == null ? "" : obj.name + " set txt content " + txt == null ? "" : txt);

            if (obj == null || txt == null)
                return null;
            InputField input = obj.GetComponent<InputField>();

            if (input == null)
            {
                Logger.e("Gameobject " + obj.name + " is not input element");
                return null;
            }

            string orginalText = input.text;

            input.text = txt;

            return orginalText;
        }

        public static bool IsInteraction(GameObject obj)
        {
            if (obj == null)
                return false;

            Component e = obj.GetComponentInParent(typeof(IEventSystemHandler));
            if (e == null)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    }
}
