using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using UnityEngine;

namespace WeTest.U3DAutomation
{
    class GameObjectTool
    {
        public static bool IsRoot(GameObject gameobject)
        {
            if (!gameobject.activeInHierarchy)
            {
                return false;
            }

            if (gameobject.transform.root != gameobject.transform)
            {
                return false;
            }

            return true;
        }

        public static string GenerateNamePath(GameObject gameobj)
        {

            String result = null;

            while (gameobj.transform.root != gameobj.transform)
            {
                if (result == null)
                {
                    result = gameobj.name;
                }
                else
                {
                    result = gameobj.name + "/" + result;
                }

                gameobj = gameobj.transform.parent.gameObject;
            }

            if (result == null)
            {
                return "/" + gameobj.name;
            }
            else
            {
                return "/" + gameobj.name + "/" + result;
            }
        }

        public static string GetObjectType(GameObject gameobject)
        {
            if (gameobject == null)
            {
                return "";
            }

            Component[] components = gameobject.GetComponents<Component>();

            if (components == null)
            {
                return "";
            }

            StringBuilder sb = new StringBuilder();

            foreach (Component cp in components)
            {
                if (cp == null)
                {
                    continue;
                }

                if (cp is Transform)
                {
                    continue;
                }

                if (sb.Length != 0)
                {
                    sb.Append("|");
                }

                sb.Append(cp.GetType().Name);               
            }

            return sb.ToString();
        }

        public static string DumpTree()
        {
            XmlDocument doc = new XmlDocument();

            XmlElement root = doc.CreateElement("AbstractRoot");
            string xmltext = "";
            doc.AppendChild(root);

            root.SetAttribute("id", "0");

            try
            {
                Transform[] roots = GameObjectManager.INSTANCE.GetRootTransforms();

                foreach (Transform transform in roots)
                {
                    if (transform.gameObject.activeInHierarchy)
                    {
                        root.AppendChild(Transform2XmlElement(transform, null, doc));
                    }
                }

                xmltext = doc.InnerXml;
                return xmltext;
            }
            catch (System.Exception ex)
            {
                Logger.e("DumpTree error message:" + ex.Message + "\n" + ex.StackTrace);
                throw ex;
            }
           
        }

        private static XmlElement Transform2XmlElement(Transform t, GameObject[] selectedObjs, XmlDocument doc)
        {
            UGUIHelper helper = new UGUIHelper();
            XmlElement elem = doc.CreateElement("GameObject");

            elem.SetAttribute("name", t.gameObject.name);
            elem.SetAttribute("components", GetObjectType(t.gameObject));
            elem.SetAttribute("id", t.gameObject.GetInstanceID().ToString());

            Logger.d("t.gameObject.name=" + t.gameObject.name.ToString() + ", t.gameObject.GetType()=" + t.gameObject.GetType().FullName.ToString());

            string str = helper.GetText(t.gameObject);

            if (str != null)
            {
                elem.SetAttribute("txt", str);
            }

            str = helper.GetImage(t.gameObject);

            if (str != null)
            {
                elem.SetAttribute("img", str);
            }

            bool result = helper.IsVisible(t.gameObject);
            if (!result)
            {
                elem.SetAttribute("visible", "false");
            }

            if (selectedObjs != null && IsSelected(t.gameObject, selectedObjs))
            {
                elem.SetAttribute("sel", "true");
            }

            for (int i = 0; i < t.childCount; ++i)
            {
                Transform transform = t.GetChild(i);

                if (transform.gameObject.activeInHierarchy)
                {
                    elem.AppendChild(Transform2XmlElement(transform, selectedObjs, doc));
                }
            }

            return elem;
        }

        private static Boolean IsSelected(GameObject obj, GameObject[] selectedObjs)
        {
            foreach (GameObject selectedObj in selectedObjs)
            {
                if (selectedObj.GetInstanceID() == obj.GetInstanceID())
                {
                    return true;
                }
            }

            return false;
        }

    }
}
