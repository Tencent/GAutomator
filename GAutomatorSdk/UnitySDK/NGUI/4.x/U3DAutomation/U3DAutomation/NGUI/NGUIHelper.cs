using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using System.Reflection;

namespace WeTest.U3DAutomation
{
    class NGUIHelper : UIBase
    {
        /// <summary>
        /// 返回Text、GUIText的文字内容
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public string GetText(GameObject gameobject)
        {
            if (gameobject == null)
                return null;

            try
            {
                string text = NGUITools.GetText(gameobject);
                if (text != null)
                {
                    return text;
                }
            }
            catch (System.Exception ex)
            {
            	
            }

            GUIText guiText = gameobject.GetComponent<GUIText>(); ;
            if (guiText != null)
            {
                return guiText.text;
            }

            return null;
        }

        /// <summary>
        /// 
        /// 返回当前节点，及其子节点中的所有文字内容
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public List<string> GetInChildrenTexts(GameObject obj)
        {
            

            if (obj == null)
                return null;

            List<string> textNames = NGUITools.GetInChildrenTexts(obj);

            GUIText[] guiTexts = obj.GetComponentsInChildren<GUIText>(); ;
            for (int i = 0; i < guiTexts.Length; ++i)
            {
                if (guiTexts[i] != null)
                {
                    textNames.Add((string)guiTexts[i].text);
                }
            }

            return textNames;
        }

        /// <summary>
        /// 
        /// 如果当前GameObject包含，Image\RawImage\SpriteRender组件，则返回图片名称
        /// </summary>
        /// <param name="gameobject"></param>
        /// <returns></returns>
        public string GetImage(GameObject gameobject)
        {
            if (gameobject == null)
                return null;

            string name = NGUITools.GetImage(gameobject);
            if (name != null)
            {
                return name;
            }
            
            SpriteRenderer renderer = gameobject.GetComponent<SpriteRenderer>();
            if (renderer != null && renderer.sprite != null)
            {
                return renderer.sprite.name;
            }

            return null;
        }

        public List<string> GetInChildrenImages(GameObject gameobject)
        {
            if (gameobject == null)
                return null;

            List<string> imageNames = NGUITools.GetInChildrenImages(gameobject);

            SpriteRenderer[] renderers = gameobject.GetComponentsInChildren<SpriteRenderer>();
            if (renderers != null)
            {
                for (int i = 0; i < renderers.Length; ++i)
                {
                    if (renderers[i] != null && renderers[i].sprite != null)
                    {
                        imageNames.Add(renderers[i].sprite.name);
                    }
                }
            }

            return imageNames;
        }

        public Rectangle GetBound(GameObject obj)
        {
            
            if (obj == null)
                return null;
            Rectangle rc = null;
            Camera cm = FindBestCamera(obj);
            if (cm == null)
                return null;

            rc = GetBoundByCollider(cm, obj);//主要是boxcolider2d物体的时候

            if (rc == null)
            {
                rc = NGUITools.GetNGUIBound(cm,obj);
            }

            if (rc == null)
                rc = GetGUIBound(cm, obj);

            if(rc==null)
                return null;

            Logger.d("GetBound gameobject =" + obj.name + "  rc.x=" + rc.x + ", rc.y=" + rc.y + ", wight = " + rc.width + ", height=" + rc.height);

            //坐标缩放
            float offsetx = 0, offsety = 0, scalex = 0, scaley = 0;
            if (RuntimePlatform.IPhonePlayer == Application.platform)//ios默认返回归一化的值
            {
                rc.x = rc.x / Screen.width;
                rc.y = rc.y / Screen.height;
                rc.width = rc.width / Screen.width;
                rc.height = rc.height / Screen.height;
            }
            else if (CoordinateTool.GetCurrenScreenParam(ref offsetx, ref offsety, ref scalex, ref scaley))
            {
                rc.x = rc.x * scalex + offsetx;
                rc.y = rc.y * scaley + offsety;

                rc.width = rc.width * scalex;
                rc.height = rc.height * scaley;


            }
            Logger.d("GetBound() after scale : rc.x=" + rc.x + ", rc.y=" + rc.y + ", wight = " + rc.width + ", height=" + rc.height);

            return rc;
        }

        public string SetInputText(GameObject obj, string content)
        {
            Logger.d("SetInputTxt" + obj == null ? "" : obj.name + " set txt content " + content == null ? "" : content);

            if (obj == null || content == null)
                return null;

            string orginalText = GetText(obj);

            NGUITools.SetNGUIInputText(obj, content);

            return orginalText;
        }

        public List<GameObject> FindGameObjectsByPoint(Point pt)
        {
            List<GameObject> result = new List<GameObject>();

            try
            {
                GameObject obj = NGUITools.GetUIElementbyRaycast(pt);
                if (obj != null)
                {
                    result.Add(obj);
                    return result;
                    
                }
            }
            catch (System.Exception ex)
            {
                Logger.d(ex.Message + "\n" + ex.StackTrace);
            }


            Transform[] ts = GameObjectManager.GetRootTransforms();

            foreach (Transform t in ts)
            {
                if (t == null)
                {
                    continue;
                }

                FindGameObjectsByPointTravel(t.gameObject, pt, result);
            }

            return result;
        }


        public void FindGameObjectsByPointTravel(GameObject obj, Point pt, List<GameObject> objs)
        {
            if (!NGUITools.IsVisible(obj))
            {
                return;
            }

            Rectangle rect = GetBound(obj);
            if (rect != null && rect.ContainPt(pt))
            {
                if (objs.ToArray().Length <= 0)
                {
                    objs.Add(obj);
                    Logger.d("Add obj " + obj.name);
                }
                else
                {
                    Rectangle rect0 = GetBound(objs[0]);
                    if (rect._height * rect._width <= rect0._width * rect0._height)      //compare rect size
                    {
                        if (objs.ToArray().Length > 0 && rect._height * rect._width < rect0._width * rect0._height)
                        {
                            objs.Clear();
                        }
                        objs.Add(obj);
                    }

                }
            }

            Transform transfrom = obj.transform;

            for (int i = 0; i < transfrom.childCount; ++i)
            {
                GameObject o = transfrom.GetChild(i).gameObject;

                FindGameObjectsByPointTravel(o, pt, objs);
            }


        }

        public List<InteractElement> GetInteractElements()
        {

            List<InteractElement> elements = GetInteractElements(null);

            return elements;
        }

        public List<InteractElement> GetInteractElements(List<String> buttonTypes)
        {
            List<UINode> nodes = NGUITools.GetInteractiveGameobject(buttonTypes);

            List<InteractElement> elements = new List<InteractElement>();

            foreach (UINode node in nodes)
            {
                GameObject gameobject = node.gameobject;
                Rectangle rect = node.bound;

                InteractElement element = new InteractElement();
                element.nodetype = AutoTravelNodeType.BUTTON;
                //能够很容易的获取控件上的文字，下同
                String path_name = GameObjectTool.GenerateNamePath(gameobject);
                element.name = path_name;
                element.instanceid = gameobject.GetInstanceID();
                element.bound.x = rect.x;
                element.bound.y = rect.y;
                element.bound.fWidth = rect.width;
                element.bound.fHeight = rect.height;
                elements.Add(element);
                GameObjectManager.INSTANCE.AddGameObject(gameobject);
            }

            return elements;
        }
    }
}
