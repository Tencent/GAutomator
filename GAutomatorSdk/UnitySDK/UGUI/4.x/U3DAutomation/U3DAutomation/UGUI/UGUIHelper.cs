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
    class UGUIHelper : UIBase
    {
        /// <summary>
        /// 返回Text、GUIText的文字内容
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public string GetText(GameObject obj)
        {
            try
            {
                if (obj == null)
                    return null;
                Text txt = obj.GetComponent<Text>();

                if (txt != null)
                {
                    string str = txt.text;
                    return str;
                }
                GUIText guiText = obj.GetComponent<GUIText>();
                if (guiText != null)
                {
                    return guiText.text;
                }
            }
            catch (System.Exception ex)
            {
            	
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
            List<string> txtNames = new List<string>();
            try
            {
                if (obj == null)
                    return txtNames;
                Text[] txts = obj.GetComponentsInChildren<Text>();

                if (txts != null)
                {
                    for (int i = 0; i < txts.Length; ++i)
                    {
                        if (txts[i] != null)
                        {
                            txtNames.Add(txts[i].text);
                        }
                    }
                }
                GUIText[] guiTexts = obj.GetComponentsInChildren<GUIText>(); ;
                if (guiTexts != null)
                {
                    for (int i = 0; i < guiTexts.Length; ++i)
                    {
                        if (guiTexts[i] != null)
                        {
                            txtNames.Add(guiTexts[i].text);
                        }
                    }
                }
                return txtNames;
            }
            catch (System.Exception ex)
            {
            	
            }
            return txtNames;
            
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

            try
            {
                Image image = gameobject.GetComponent<Image>();
                if (image != null && image.sprite != null)
                {
                    return image.sprite.name;
                }

                RawImage rawImage = gameobject.GetComponent<RawImage>();

                if (rawImage != null && rawImage.texture != null)
                {
                    return rawImage.texture.name;
                }
                SpriteRenderer renderer = gameobject.GetComponent<SpriteRenderer>();
                if (renderer != null && renderer.sprite != null)
                {
                    return renderer.sprite.name;
                }
            }
            catch (System.Exception ex)
            {
            	
            }
            

            return null;
        }

        public List<string> GetInChildrenImages(GameObject gameobject)
        {
            if (gameobject == null)
                return null;

            List<string> imageNames = new List<string>();
            try
            {
                Image[] images = gameobject.GetComponentsInChildren<Image>();
                if (images != null)
                {
                    for (int i = 0; i < images.Length; ++i)
                    {
                        if (images[i].sprite != null)
                        {
                            imageNames.Add(images[i].sprite.name);
                        }
                    }
                }

                RawImage[] rawImages = gameobject.GetComponentsInChildren<RawImage>();

                if (rawImages != null)
                {
                    for (int i = 0; i < rawImages.Length; ++i)
                    {
                        if (rawImages[i] != null && rawImages[i].texture != null)
                        {
                            imageNames.Add(rawImages[i].texture.name);
                        }
                    }
                }
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
            }
            catch (System.Exception ex)
            {
            	
            }
            

            return imageNames;
        }

        public Rectangle GetBound(GameObject obj)
        {
            Rectangle rc = null;
            if (obj == null)
                return null;
            if (UGUITools.isUGUIElement(obj))
            {
                rc = UGUITools.GetUGUIBound(obj);
            }
            if (rc == null)
            {
                Camera cm = FindBestCamera(obj);
                if (cm == null)
                    return null;
                rc = GetGUIBound(cm,obj);
            }

            if (rc == null)
                return null;

            Logger.v("GetBound gameobject =" + obj.name + "  rc.x=" + rc.x + ", rc.y=" + rc.y + ", wight = " + rc.width + ", height=" + rc.height);

            //坐标缩放
            float offsetx = 0, offsety = 0, scalex = 0, scaley = 0;
            if(RuntimePlatform.IPhonePlayer == Application.platform){//iOS 返回归一化的值
                rc.x = rc.x / Screen.width;
                rc.y = rc.y / Screen.height;
                rc.width = rc.width / Screen.width;
                rc.height = rc.height / Screen.height;
            }
            else if (CoordinateTool.GetCurrenScreenParam(ref offsetx, ref offsety,ref scalex, ref scaley))
            {
                rc.x = rc.x * scalex + offsetx;
                rc.y = rc.y * scaley + offsety;

                rc.width = rc.width * scalex;
                rc.height = rc.height * scaley;

                
            }
            Logger.v("GetBound() after scale : rc.x=" + rc.x + ", rc.y=" + rc.y + ", wight = " + rc.width + ", height=" + rc.height);
            return rc;
        }

        public string SetInputText(GameObject obj, string content)
        {
            Logger.d("SetInputTxt" + obj == null ? "" : obj.name + " set txt content " + content == null ? "" : content);

            if (obj == null || content == null)
                return null;
            InputField input = obj.GetComponentInChildren<InputField>();

            if (input == null)
            {
                Logger.e("Gameobject " + obj.name + " is not input element");
                return null;
            }

            string orginalText = input.text;

            input.text = content;

            return orginalText;
        }

        public List<GameObject> FindGameObjectsByPoint(Point pt)
        {
            List<GameObject> result = new List<GameObject>();

            try
            {
                GameObject obj = UGUITools.GetUIElementbyRaycast(pt);
                if (obj != null)
                {
                    result.Add(obj);
                    
                }
            }
            catch (System.Exception ex)
            {
                Logger.d(ex.Message + "\n" + ex.StackTrace);
            }

            return result;
        }

        public List<InteractElement> GetInteractElements()
        {

            List<InteractElement> elements = GetInteractElements(null);
            return elements;
        }

        public List<InteractElement> GetInteractElements(List<String> buttonTypes)
        {
            List<UINode> nodes = EventSystemTool.GetInteractiveGameobject(buttonTypes);

            List<InteractElement> elements = new List<InteractElement>();

            foreach (UINode node in nodes)
            {
                GameObject gameobject = node.gameobject;
                Rectangle rect = node.bound;

                InteractElement element = new InteractElement();
                if (gameobject.GetComponent<Button>() != null)
                {
                    element.nodetype = AutoTravelNodeType.BUTTON;
                    //能够很容易的获取控件上的文字，下同
                }
                else if (gameobject.GetComponent<InputField>() != null)
                {
                    if (gameobject.GetComponent<InputField>().contentType == InputField.ContentType.Password)
                    {
                        element.nodetype = AutoTravelNodeType.INPUTPAS;
                    }
                    else
                    {
                        element.nodetype = AutoTravelNodeType.INPUTXT;
                    }
                }
                else
                {
                    element.nodetype = AutoTravelNodeType.OTHER;
                }
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
