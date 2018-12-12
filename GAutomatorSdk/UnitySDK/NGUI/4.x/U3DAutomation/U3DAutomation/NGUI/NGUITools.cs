using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using System.Reflection;

namespace WeTest.U3DAutomation
{
    class DepthEntry
    {
        public int depth;
        public RaycastHit hit;
        public Vector3 point;
        public GameObject go;
    }

    enum FindElementType
    {
        World,
        UI
    }

    class NGUITools
    {

        public static readonly string UIRootTypeName = "UIRoot, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UICameraTypeName = "UICamera, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIPanelTypeName = "UIPanel, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIButtonName = "UIButton, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIToggleName = "UIToggle, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIEventListenerName = "UIEventListener, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIWidgetTypeName = "UIWidget, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIRectTypeName = "UIRect, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UILabelTypeName = "UILabel, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIInputTypeName = "UIInput, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UITextureTypeName = "UITexture, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UISpriteTypeName = "UISprite, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";

        public static readonly string UIRootTypeNameFirstPass = "UIRoot, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UICameraTypeNameFirstPass = "UICamera, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIPanelTypeNameFirstPass = "UIPanel, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIButtonNameFirstPass = "UIButton, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIToggleNameFirstPass = "UIToggle, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIEventListenerNameFirstPass = "UIEventListener, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIWidgetTypeNameFirstPass = "UIWidget, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIRectTypeNameFirstPass = "UIRect, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UILabelTypeNameFirstPass = "UILabel, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UIInputTypeNameFirstPass = "UIInput, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UITextureTypeNameFirstPass = "UITexture, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";
        public static readonly string UISpriteTypeNameFirstPass = "UISprite, Assembly-CSharp-firstpass, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null";



        private static Type UIRootType = null;
        private static Type UICameraType = null;
        private static Type UIPanelType = null;
        private static Type UIButtonType = null;
        private static Type UIToggleType = null;
        private static Type UIEventListenerType = null;
        private static Type UIWidgetType = null;
        private static Type UIRectType = null;

        private static Type UILabelType = null;
        private static Type UIInputType = null;
        private static Type UITextureType=null;
        private static Type UISpriteType=null;
       


        static BetterList<DepthEntry> mHits = new BetterList<DepthEntry>();

        static NGUITools()
        {
            try
            {
                UIRootType = Type.GetType(UIRootTypeName);
                if(UIRectType==null) UIRootType=Type.GetType(UIRootTypeNameFirstPass);

                UICameraType = Type.GetType(UICameraTypeName);
                if(UICameraType==null) UICameraType=Type.GetType(UICameraTypeNameFirstPass);

                UIPanelType = Type.GetType(UIPanelTypeName);
                if(UIPanelType==null) UIPanelType=Type.GetType(UIPanelTypeNameFirstPass);

                UIButtonType=Type.GetType(UIButtonName);
                if(UIButtonType==null) UIButtonType=Type.GetType(UIButtonNameFirstPass);

                UIToggleType = Type.GetType(UIToggleName);
                if(UIToggleType==null) UIToggleType=Type.GetType(UIToggleNameFirstPass);

                UIEventListenerType = Type.GetType(UIEventListenerName);
                if (UIEventListenerType == null) UIEventListenerType = Type.GetType(UIEventListenerNameFirstPass);

                UIWidgetType = Type.GetType(UIWidgetTypeName);
                if(UIWidgetType==null) UIWidgetType=Type.GetType(UIWidgetTypeNameFirstPass);

                UIRectType = Type.GetType(UIRectTypeName);
                if (UIRectType == null) UIRectType = Type.GetType(UIRectTypeNameFirstPass);

                UILabelType = Type.GetType(UILabelTypeName);
                if (UILabelType == null) UILabelType = Type.GetType(UILabelTypeNameFirstPass);

                UIInputType = Type.GetType(UIInputTypeName);
                if (UIInputType == null) UIInputType = Type.GetType(UIInputTypeNameFirstPass);

                UITextureType=Type.GetType(UITextureTypeName);
                if (UITextureType == null) UITextureType = Type.GetType(UITextureTypeNameFirstPass);

                UISpriteType=Type.GetType(UISpriteTypeName);
                if (UISpriteType == null) UISpriteType = Type.GetType(UISpriteTypeNameFirstPass);
            }
            catch (System.Exception ex)
            {
                Logger.w("NGUITool init error =>" + ex.Message + "\n" + ex.StackTrace);
            }

        }

        public static string GetText(GameObject gameobject)
        {
            object txt = ReflectionTools.GetComponentAttribute(gameobject,UILabelType, "text");

            if (txt != null)
            {
                return (String)txt;
            }

            txt = ReflectionTools.GetComponentAttribute(gameobject, UIInputType, "value");

            if (txt != null)
            {
                return (String)txt;
            }

            return null;
        }

        public static List<string> GetInChildrenTexts(GameObject gameobject)
        {
            List<string> textNames = new List<string>();
            List<object> txts = ReflectionTools.GetComponentInChildrenAttribute(gameobject,UILabelType, "text");
            if (txts != null)
            {
                for (int i = 0; i < txts.Count; ++i)
                {
                    if (txts[i] != null)
                    {
                        textNames.Add((string)txts[i]);
                    }
                }
            }

            txts = ReflectionTools.GetComponentInChildrenAttribute(gameobject,UIInputType, "text");

            if (txts != null)
            {
                for (int i = 0; i < txts.Count; ++i)
                {
                    if (txts[i] != null)
                    {
                        textNames.Add((string)txts[i]);
                    }
                }
            }

            return textNames;
        }

        public static string GetImage(GameObject obj)
        {
            if (obj == null)
                return null;


            object mainTexture = ReflectionTools.GetComponentAttribute(obj, UITextureType, "mainTexture");

            if (mainTexture != null)
            {
                Texture t = (Texture)mainTexture;
                return t.name;
            }

            object spriteName = ReflectionTools.GetComponentAttribute(obj, UISpriteType, "spriteName");

            if (spriteName != null)
            {
                String name = (String)spriteName;
                return name;
            }
            return null;
        }

        public static List<string> GetInChildrenImages(GameObject obj)
        {
            List<string> imageNames = new List<string>();
            List<object> mainTextures = ReflectionTools.GetComponentInChildrenAttribute(obj,UITextureType, "mainTexture");

            if (mainTextures != null)
            {
                for (int i = 0; i < mainTextures.Count; ++i)
                {
                    Texture t = (Texture)mainTextures[i];
                    imageNames.Add(t.name);
                }

            }

            List<object> spriteNames = ReflectionTools.GetComponentInChildrenAttribute(obj,UISpriteType, "spriteName");

            if (spriteNames!= null)
            {
                for (int i = 0; i < spriteNames.Count; ++i)
                {
                    if (spriteNames[i] != null)
                    {
                        imageNames.Add((string)spriteNames[i]);
                    }
                }
            }
            return imageNames;
        }

        private static float GetDistance(Vector3 point1, Vector3 point2)
        {
            float value = (float)Math.Sqrt(Math.Abs(point1.x - point2.x) * Math.Abs(point1.x - point2.x) + Math.Abs(point1.y - point2.y) * Math.Abs(point1.y - point2.y));

            return value;
        }

        /// <summary>
        /// 获取NGUI的长宽高
        /// </summary>
        /// <param name="c"></param>
        /// <param name="obj"></param>
        /// <returns></returns>
        public static Rectangle GetNGUIBound(Camera c, GameObject obj)
        {
            Vector3[] worldCorners = (Vector3[])ReflectionTools.GetComponentAttribute(obj,UIWidgetType, "worldCorners");

            if (worldCorners != null)
            {
                if (c == null)
                {
                    Logger.e("NO Camera!");
                    return null;
                }

                //修改获取矩形的宽高为负数的情形，例如，当箭头的外包矩形非与坐标轴平行时。光用左上角坐标点、和宽高来表示一个矩形存在一定错误，但影响不大，可容忍.

                //index==1，是左上角。index==3是右下角。坐标原点在左下角。
                Vector3 point0 = c.WorldToScreenPoint(worldCorners[0]);
                Vector3 point1 = c.WorldToScreenPoint(worldCorners[1]);
                Vector3 point2 = c.WorldToScreenPoint(worldCorners[2]);
                Vector3 point3 = c.WorldToScreenPoint(worldCorners[3]);
                float h = GetDistance(point0, point1);
                float w = GetDistance(point1, point2);

                Logger.v("Screen Height = " + Screen.height + " Width = " + Screen.width);
                //换算成坐标原点在左上角。        
                Point ptTopLeft = new Point(point1.x, Screen.height - point1.y);
                Point ptBottomRight = new Point(point3.x, Screen.height - point3.y);

                return new Rectangle(ptTopLeft.X, ptTopLeft.Y, w, h);
            }
            return null;
        }

        public static bool SetNGUIInputText(GameObject obj,string text)
        {
            if (ReflectionTools.SetComponentAttribute(obj, UIInputType, "value", text))
            {
                return true;
            }
            else if (ReflectionTools.SetComponentAttribute(obj, UIInputType, "text", text))
            {
                //NGUI 3.0
                return true;
            }

            return false;
        }

        //获取所有的UIRoot节点
        public static Component[] GetUIRootGameObjects()
        {
            UnityEngine.Object[] gameObjects = GetObjectByTypes(UIRootTypeName);

            Component[] components;
            if (gameObjects == null)
            {
                gameObjects = GetObjectByTypes(UIRootTypeNameFirstPass);
            }

            if (gameObjects == null)
            {
                Logger.d("GetUIRootGameObjects => can not find, UIRoot: " + UIRootTypeName + ", and " + UIRootTypeNameFirstPass);
                return null;
            }
            else
            {
                components = gameObjects as Component[];
                return components;
            }
        }

        public static UnityEngine.Object[] GetObjectByTypes(string typeName)
        {

            Type type = Type.GetType(typeName);
            if (type == null)
            {
                Logger.e("Can't get =>" + typeName + " type");
                return null;
            }
            UnityEngine.Object[] objects = GameObject.FindObjectsOfType(type);
            if (objects != null)
            {

                Logger.v("Find Object by type:" + typeName + " num:" + objects.Length);
            }
            else
            {
                Logger.v("Find Object by type:" + typeName + " num:0");
            }
            return objects;
        }

        public static Type GetUICameraType()
        {
            Type type = null;
            try
            {
                type = Type.GetType(UICameraTypeName);
            }
            catch (System.Exception ex)
            {
                Logger.d("Unknow type " + UICameraTypeName);
            }
            if (type != null)
            {
                return type;
            }

            try
            {
                type = Type.GetType(UICameraTypeNameFirstPass);
            }
            catch (System.Exception ex)
            {
                Logger.d("Unknow type " + UICameraTypeNameFirstPass);
            }

            return type;
        }

        public static GameObject GetUIElementbyRaycast(Point point)
        {
            Point pt = new Point(0, 0);
            if (point.X < 1 && point.X > 0 && point.Y < 1 && point.Y > 0 )
            {
                pt = new Point(Screen.width * point.X, Screen.height * (1 - point.Y));

            }
            else if (RuntimePlatform.Android == Application.platform)
            {
                pt = CoordinateTool.ConvertMobile2Unity(point);
            }
            else {
                pt = new Point(point.X, Screen.height - point.Y);
            }
            Vector2 vector = CoordinateTool.ConvertPoint2Vector(pt);
            bool invalid = false;
            GameObject gameObject = Raycast(vector, ref invalid);
            return gameObject;
        }

        public static GameObject FindElementByUnityPos(Point pt)
        {
            Vector2 vector = CoordinateTool.ConvertPoint2Vector(pt);
            bool invalid = false;
            GameObject gameObject = Raycast(vector, ref invalid);
            return gameObject;
        }

        public static bool OverUIElement(GameObject obj, ref Vector2 vector)
        {
            if (obj == null) return false;

            Rectangle rc = null;
            UIBase uibase = new UIBase();
            Camera cm = UIBase.FindBestCamera(obj);

            if (cm == null) return false;

            rc = uibase.GetBoundByCollider(cm,obj);
            if (rc == null) return false;

            Vector2 position = new Vector2();
            position.x = rc.x + rc.width / 2;
            position.y = Screen.height - (rc.y + rc.height / 2);
            //position.y = rc.y + rc.height / 2;
            vector.x = position.x;
            vector.y = position.y;

            Logger.d("Test raycast point (" + position.x + " , " + position.y + ")");
            bool invaild = false;
            GameObject raycastGameobject = Raycast(position, ref invaild);
            if (raycastGameobject != null)
            {
                Logger.v("Raycast GameObject " + raycastGameobject.name);
            }
            if (invaild)
            {
                Logger.v("Invaild Raycast");
                return true;
            }

            return raycastGameobject == obj;

        }

        public static bool OverUIElement(GameObject obj, ref Rectangle rect)
        {
            if (obj == null) return false;

            Rectangle rc = null;
            UIBase uibase = new UIBase();
            Camera cm = UIBase.FindBestCamera(obj);
            if (cm == null) return false;
            rc = uibase.GetBoundByCollider(cm, obj);
            if (rc == null) return false;
            Vector2 position = new Vector2();
            position.x = rc.x + rc.width / 2;
            position.y = Screen.height - (rc.y + rc.height / 2);
            //position.y = rc.y + rc.height / 2;
            rect.x = rc.x;
            rect.y = Screen.height - rc.y;
            rect.height = rc.height;
            rect.width = rc.width;

            Logger.d("Test raycast point (" + position.x + " , " + position.y + ")");
            bool invaild = false;
            GameObject raycastGameobject = Raycast(position, ref invaild);
            if (raycastGameobject != null)
            {
                Logger.v("Raycast GameObject " + raycastGameobject.name);
            }
            if (invaild)
            {
                Logger.v("Invaild Raycast");
                return true;
            }

            return raycastGameobject == obj;

        }

        public static void GetMethod(Type type)
        {

            MethodInfo[] methodInfos = type.GetMethods(BindingFlags.Static | BindingFlags.Public);
            Logger.d("Find Methods number " + methodInfos.Length);
            foreach (MethodInfo m in methodInfos)
            {
                Logger.d("Name = " + m.Name);
                MethodAttributes attributes = m.Attributes;
                ParameterInfo[] types = m.GetParameters();
                foreach (ParameterInfo t in types)
                {
                    Logger.d("Arg type " + t.ParameterType.FullName);
                }
            }
        }

        public static GameObject Raycast(Vector3 inpos, ref bool invaild)
        {
            try
            {
                invaild = false;
                Type uiCameraType = GetUICameraType();
                if (uiCameraType == null)
                {
                    Logger.e("Find UICamera type failed!");
                    return null;
                }

                MethodInfo raycastMethod = uiCameraType.GetMethod("Raycast", new[] { typeof(Vector3) });
                bool result = false;
                if (raycastMethod != null)
                {
                    result = (bool)raycastMethod.Invoke(null, new object[] { inpos });
                }
                else
                {
                    raycastMethod = uiCameraType.GetMethod("Raycast", BindingFlags.Public | BindingFlags.Static, null, new[] { typeof(Vector3), typeof(RaycastHit).MakeByRefType() }, null);
                    if (raycastMethod == null)
                    {
                        Logger.w("No Raycast Method");
                        return null;
                    }
                    RaycastHit hit = new RaycastHit();
                    result = (bool)raycastMethod.Invoke(null, new object[] { inpos, hit });
                }



                Logger.v("Raycast result " + (result ? "True" : "False"));

                FieldInfo fieldInfo = uiCameraType.GetField("hoveredObject");
                if (fieldInfo != null)
                {
                    Logger.v("Find hoveredObject");
                    object obj = fieldInfo.GetValue(null);
                    if (obj != null)
                    {
                        return obj as GameObject;
                    }
                }

                fieldInfo = uiCameraType.GetField("mRayHitObject", BindingFlags.Static | BindingFlags.NonPublic);
                if (fieldInfo != null)
                {
                    Logger.v("Find mRayHitObject");
                    object obj = fieldInfo.GetValue(null);
                    if (obj != null)
                    {
                        return obj as GameObject;
                    }
                }

                return null;
            }
            catch (System.Exception ex)
            {
                Logger.e(ex.Message + "\n" + ex.StackTrace);
            }
            return null;
        }

        public static List<UINode> GetInteractiveGameobject(List<string> buttonTypes)
        {
            //string[] typeNames = new string[] { UIButtonName, UIToggleName, UIEventListenerName };
            //string[] typeNamesFirst = new string[] { UIButtonNameFirstPass, UIToggleNameFirstPass, UIEventListenerNameFirstPass };

            List<string> typeNames = new List<string>();
            List<string> typeNamesFirst = new List<string>();
            typeNames.Add(UIButtonName);
            typeNamesFirst.Add(UIButtonNameFirstPass);

            typeNames.Add(UIToggleName);
            typeNamesFirst.Add(UIToggleNameFirstPass);

            typeNames.Add(UIEventListenerName);
            typeNamesFirst.Add(UIEventListenerNameFirstPass);

            if (buttonTypes != null)
            {
                for (int i = 0; i < buttonTypes.Count; ++i)
                {
                    typeNames.Add(buttonTypes[i]);
                    typeNamesFirst.Add(buttonTypes[i]);
                }
            }

            HashSet<int> buffers = new HashSet<int>();
            List<UINode> gameObjects = new List<UINode>();
            Rectangle rect = new Rectangle();
            for (int i = 0; i < typeNames.Count; ++i)
            {
                Type buttonType = Type.GetType(typeNames[i]);
                if (buttonType == null) buttonType = Type.GetType(typeNamesFirst[i]);

                if (buttonType != null)
                {
                    Component[] objs = GameObject.FindObjectsOfType(buttonType) as Component[];
                    foreach (Component c in objs)
                    {
                        GameObject obj = c.gameObject;

                        Logger.v("Find GameObject " + obj.name);

                        if (!buffers.Contains(obj.GetInstanceID()) && OverUIElement(obj, ref rect))
                        {
                            Rectangle rc = new Rectangle();
                            if (RuntimePlatform.Android==Application.platform){//安卓默认返回绝对坐标
                                rc = CoordinateTool.ConvertUnity2Mobile(rect);
                            }
                            else if(RuntimePlatform.IPhonePlayer==Application.platform){//ios 默认返回归一化的坐标
                                rc.x = rect.x/Screen.width;
                                rc.y = 1 - rect.y / Screen.height;
                                rc.width = rect.width / Screen.width;
                                rc.height = rect.height / Screen.height;

                            }

                           
                            UINode node = new UINode(obj, rc);
                            buffers.Add(obj.GetInstanceID());
                            gameObjects.Add(node);
                        }

                    }
                }
            }

            return gameObjects;
        }

        public static bool IsInteraction(GameObject obj)
        {
            if (obj == null)
                return false;
            Type[] types = new Type[] { UIButtonType, UIToggleType, UIEventListenerType };
            foreach (Type t in types)
            {
                Component c = obj.GetComponentInParent(t);
                if (c != null)
                {
                    return true;
                }
            }
            return false;
        }

        
        //控件是否可见
        public static bool IsVisible(GameObject obj)
        {
            if (obj == null || obj.activeInHierarchy == false)
            {
                return false;
            }

            object vs = ReflectionTools.GetComponentAttribute(obj, UIWidgetType, "isVisible");
            if (vs!=null)
            {
                return (Boolean)vs;
            }
            return obj.activeSelf && obj.hideFlags == HideFlags.None;
            
        }
    }
}
