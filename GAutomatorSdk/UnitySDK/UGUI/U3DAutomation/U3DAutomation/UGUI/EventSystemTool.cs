using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using UnityEngine.EventSystems;
using System.Reflection;
using UnityEngine.UI;
using System.Collections;


namespace WeTest.U3DAutomation
{
	public class EventSystemTool
	{
        private static readonly Comparison<RaycastResult> s_RaycastComparer = RaycastComparer;

        private static int RaycastComparer(RaycastResult lhs, RaycastResult rhs)
        {
            if (lhs.module != rhs.module)
            {
                if (lhs.module.eventCamera != null && rhs.module.eventCamera != null && lhs.module.eventCamera.depth != rhs.module.eventCamera.depth)
                {
                    // need to reverse the standard compareTo
                    if (lhs.module.eventCamera.depth < rhs.module.eventCamera.depth)
                        return 1;
                    if (lhs.module.eventCamera.depth == rhs.module.eventCamera.depth)
                        return 0;

                    return -1;
                }

                if (lhs.module.sortOrderPriority != rhs.module.sortOrderPriority)
                    return rhs.module.sortOrderPriority.CompareTo(lhs.module.sortOrderPriority);

                if (lhs.module.renderOrderPriority != rhs.module.renderOrderPriority)
                    return rhs.module.renderOrderPriority.CompareTo(lhs.module.renderOrderPriority);
            }

            //if (lhs.sortingLayer != rhs.sortingLayer)
            //{
            //    // Uses the layer value to properly compare the relative order of the layers.
            //    var rid = SortingLayer.GetLayerValueFromID(rhs.sortingLayer);
            //    var lid = SortingLayer.GetLayerValueFromID(lhs.sortingLayer);
            //    return rid.CompareTo(lid);
            //}


            if (lhs.sortingOrder != rhs.sortingOrder)
                return rhs.sortingOrder.CompareTo(lhs.sortingOrder);

            if (lhs.depth != rhs.depth)
                return rhs.depth.CompareTo(lhs.depth);

            if (lhs.distance != rhs.distance)
                return lhs.distance.CompareTo(rhs.distance);

            return lhs.index.CompareTo(rhs.index);
        }
        private static void AddInvaildGameObjets<T>(ICollection<GameObject> collections) where T : Component
        {

            Component[] components = GameObject.FindObjectsOfType<T>();
            if (components == null || collections == null) return;

            for (int i = 0; i < components.Length; ++i)
            {
                if (!components[i].gameObject.activeInHierarchy)
                {
                    continue;
                }

                var behaviour = components[i] as Behaviour;
                if (behaviour == null||behaviour.isActiveAndEnabled==false) continue;

                collections.Add(components[i].gameObject);
                    
            }
        }

        //UGUI事件传播的原理首先获取第一个Raycast的节点，然后一直往父节点遍历是否有注册的可执行内容
        private static bool CanInputEventOverObject(List<BaseRaycaster> raycasters, GameObject obj,ref Vector2 centerPoint)
        {
            //步骤1：获取到当前Gameobject的中心点
            //TODO:需要确认无法找到center点的情况。如果这个找不到原有的方法，其实也是找不到点的

            RectTransform rectTran = obj.GetComponent<RectTransform>();

            Vector3[] core = new Vector3[4];
            rectTran.GetWorldCorners(core);

            Vector2[] vectors = UGUITools.GetWorldCorner(obj);
            if (vectors == null) return false;
            Vector2 bottomLeft = vectors[0];
            Vector2 topLeft = vectors[1];
            Vector2 topRight = vectors[2];
            Vector2 bottomRight = vectors[3];

            bottomLeft.x += (bottomRight.x - bottomLeft.x) / 2;
            bottomLeft.y += (topRight.y - bottomRight.y) / 2;
            //步骤2，获取到所有Raycast到的点
            PointerEventData data = new PointerEventData(EventSystem.current);
            data.position = bottomLeft;
            centerPoint.x = bottomLeft.x;
            centerPoint.y = bottomLeft.y;


            List<RaycastResult> results = new List<RaycastResult>();

            Logger.d("Find objects on point===>(" + data.position.x + "," + data.position.y + ")");
            EventSystem.current.UpdateModules();

            EventSystem.current.RaycastAll(data, results);

            if (results.Count == 0) return false;
            foreach (RaycastResult res in results)
            {
                Logger.d("gameobject name=" + res.gameObject + " index=" + res.index + " module=" + res.module + " depth=" + res.depth + " isvaild=" + res.isValid.ToString());
            }
            GameObject firstGameObject = results[0].gameObject;
            Logger.d("Find obj " + firstGameObject + " orginal game obj " + obj);
            if (firstGameObject == obj || firstGameObject.transform.IsChildOf(obj.transform))
            {
                return true;
            }

            return false;
        }

        //UGUI事件传播的原理首先获取第一个Raycast的节点，然后一直往父节点遍历是否有注册的可执行内容
        private static bool CanInputEventOverObject(List<BaseRaycaster> raycasters, GameObject obj,ref Rectangle rect)
        {
            //步骤1：获取到当前Gameobject的中心点
            //TODO:需要确认无法找到center点的情况。如果这个找不到原有的方法，其实也是找不到点的

            RectTransform rectTran = obj.GetComponent<RectTransform>();

            Vector3[] core = new Vector3[4];
            rectTran.GetWorldCorners(core);

            Vector2[] vectors = UGUITools.GetWorldCorner(obj);
            if (vectors == null) return false;
            Vector2 bottomLeft = vectors[0];
            Vector2 topLeft = vectors[1];
            Vector2 topRight = vectors[2];
            Vector2 bottomRight = vectors[3];
            rect.x = topLeft.x;
            rect.y = topLeft.y;
            rect.width = topRight.x - topLeft.x;
            rect.height = topLeft.y - bottomLeft.y;

            bottomLeft.x += (bottomRight.x - bottomLeft.x) / 2;
            bottomLeft.y += (topRight.y - bottomRight.y) / 2;
            //步骤2，获取到所有Raycast到的点
            PointerEventData data = new PointerEventData(EventSystem.current);
            data.position = bottomLeft;


            List<RaycastResult> results = new List<RaycastResult>();

            Logger.d("Find objects on point===>(" + data.position.x + "," + data.position.y + ")");
            EventSystem.current.UpdateModules();

            EventSystem.current.RaycastAll(data, results);

            if (results.Count == 0) return false;
            //foreach (RaycastResult res in results)
            //{
            //    Logger.d("gameobject name=" + res.gameObject + " index=" + res.index + " module=" + res.module + " depth=" + res.depth + " isvaild=" + res.isValid.ToString());
            //}
            GameObject firstGameObject = results[0].gameObject;
            Logger.d("Find obj " + firstGameObject + " orginal game obj " + obj);
            if (firstGameObject == obj || firstGameObject.transform.IsChildOf(obj.transform))
            {
                return true;
            }

            return false;
        }



        private static List<BaseRaycaster> GetVaildRaycast()
        {
            BaseRaycaster[] raycasters=GameObject.FindObjectsOfType<BaseRaycaster>();

            List<BaseRaycaster> raycasterList = new List<BaseRaycaster>();
            if(raycasters==null||raycasters.Length==0){
                return null;
            }

            for (int i = 0; i < raycasters.Length; ++i)
            {
                if (raycasters[i] != null || raycasters[i].IsActive())
                    raycasterList.Add(raycasters[i]);
            }
            return raycasterList;
        }

        private static Component[] GetIEventSystemHandler(GameObject obj)
        {
            if(obj==null)
                return new Component[]{};
            Component[] components = obj.GetComponentsInChildren(typeof(IEventSystemHandler));
            return components;
        }

        /// <summary>
        /// 获取所有潜在的可交互的节点
        /// 
        /// 
        /// </summary>
        /// <returns></returns>
        public static List<UINode> GetInteractiveGameobject(List<String> buttonTypes)
        {
            Logger.d("GetInteractiveGameobject");
            HashSet<int> buffer = new HashSet<int>();
            List<UINode> vaildGameObjects = new List<UINode>();
            

            Canvas[] canvas = GameObject.FindObjectsOfType<Canvas>();
            List<BaseRaycaster> raycaster = GetVaildRaycast();

            for (int i = 0; i < canvas.Length; ++i)
            {

                GameObject gameobject = canvas[i].gameObject;
                
                //步骤1,找出当前界面下包含IEventSystemHandler的所有节点
                Component[] handlers = GetIEventSystemHandler(gameobject);
                for (int j = 0; j < handlers.Length; ++j)
                {
                    Component c = handlers[j] as Component;
                    if (c != null && !buffer.Contains(c.gameObject.GetInstanceID()))
                    {
                        buffer.Add(c.gameObject.GetInstanceID());
                        Logger.d("UGUI may Clickable gameobject => " + c.gameObject);

                        //步骤2，过滤掉所有被遮挡的节点。以点击中间点的方式
                        Rectangle rect = new Rectangle();
                        if (CanInputEventOverObject(raycaster, c.gameObject, ref rect))
                        {
                            if (RuntimePlatform.Android == Application.platform)
                            { //android 默认返回绝对坐标
                                rect = CoordinateTool.ConvertUnity2Mobile(rect);
                  
                            }

                            else if (RuntimePlatform.IPhonePlayer == Application.platform)
                            {//ios 默认返回归一化的坐标
                                rect.x /= Screen.width;
                                rect.y =1-rect.y/Screen.height;
                                rect.width /= Screen.width;
                                rect.height /= Screen.height;
                            }
                            UINode node = new UINode(c.gameObject,rect);
                            Logger.d("Gameobject can click " + c.gameObject);
                            vaildGameObjects.Add(node);
                        }
                    }

                }
            }

            List<Component> comps = new List<Component>();
            for (int i = 0; buttonTypes != null && i < buttonTypes.Count; ++i)
            {
                Type buttonType = Type.GetType(buttonTypes[i]);

                if (buttonType != null)
                {
                    Component[] handlers = GameObject.FindObjectsOfType(buttonType) as Component[];
                    for (int j = 0; j < handlers.Length; ++j)
                    {
                        Component c = handlers[j] as Component;
                        if (c != null && !buffer.Contains(c.gameObject.GetInstanceID()))
                        {
                            buffer.Add(c.gameObject.GetInstanceID());
                            Logger.d("UGUI may Clickable gameobject => " + c.gameObject);

                            //步骤2，过滤掉所有被遮挡的节点。以点击中间点的方式
                            Rectangle rect = new Rectangle();
                            if (CanInputEventOverObject(raycaster, c.gameObject, ref rect))
                            {

                                if (RuntimePlatform.Android==Application.platform){//android默认返回绝对坐标
                                    rect = CoordinateTool.ConvertUnity2Mobile(rect);
                                }

                                else if (RuntimePlatform.IPhonePlayer ==Application.platform)
                                {//ios 默认返回绝对坐标
                                    rect.x /= Screen.width;
                                    rect.y=1 - rect.y / Screen.height;
                                    rect.width /= Screen.width;
                                    rect.height /= Screen.height;
                                }
                                UINode node = new UINode(c.gameObject, rect);
                                Logger.d("Gameobject can click " + c.gameObject);
                                vaildGameObjects.Add(node);
                            }
                        }

                    }
                }
            }
            return vaildGameObjects;
        }
	}
}
