using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using System.Collections;

namespace WeTest.U3DAutomation
{
	public class GameObjectManager
	{
        private static GameObjectManager instance = new GameObjectManager();

        private GameObjectTable objectTable = new GameObjectTable();

        private UGUIHelper uiHelper = new UGUIHelper();

        public static GameObjectManager INSTANCE
        {
            get { return instance; }
        }

        public GameObject FindGameObject(String findexpr)
        {
            GameObject obj = GameObject.Find(findexpr);

            if (!obj.activeInHierarchy)
            {
                return null;
            }

            return obj;
        }

        public int AddGameObject(GameObject obj)
        {
            if (obj == null)
            {
                return -1;
            }
            int id = objectTable.Add(obj);

            return id;
        }

        public GameObject FindGameObject(int id)
        {
            return objectTable.Find(id);
        }
 
        public GameObject FindGameObjectGlobal(int id)
        {
            GameObject o = objectTable.Find(id);
            if (o != null)
            {
                return o;
            }

            GameObject[] objs = UnityEngine.Object.FindObjectsOfType<GameObject>();

            foreach (GameObject obj in objs)
            {
                if (obj == null)
                {
                    continue;
                }

                if (obj.GetInstanceID() == id)
                {
                    return obj;
                }
            }

            return null;
        }

        /// <summary>
        /// 获取所有的根节点，不包含未激活的节点
        /// </summary>
        /// <returns></returns>
        public Transform[] GetRootTransforms()
        {
            Transform[] transforms = UnityEngine.Object.FindObjectsOfType<Transform>();

            //Logger.d("transforms = " + transforms.Length);

            List<Transform> list = new List<Transform>();
            foreach (Transform transform in transforms)
            {
                if (transform == null)
                {
                    continue;
                }

                if (GameObjectTool.IsRoot(transform.gameObject))
                {                    
                    list.Add(transform);
                    continue;
                }
            }

            return list.ToArray();
        }

        public int GetParent(GameObject obj)
        {
            if (obj.transform == obj.transform.parent)
            {
                return AddGameObject(obj);
            }

            return AddGameObject(obj.transform.parent.gameObject);
        }

        public List<int> GetChildren(GameObject obj)
        {
            Transform transform = obj.transform;
            List<int> result = new List<int>();

            int childCount = transform.childCount;

            for (int i = 0; i < childCount; ++i )
            {
                GameObject childobj = transform.GetChild(i).gameObject;
                if (childobj != null)
                {
                    result.Add(AddGameObject(childobj));
                }
            }

            return result;
        }

        private bool FilterNode(GameObject obj, PathNode node)
        {
            if (obj == null || !obj.activeInHierarchy)
            {
                return false;
            }

            if (!String.IsNullOrEmpty(node.regex))
            {
                if (!System.Text.RegularExpressions.Regex.IsMatch(obj.name, node.regex))
                {
                    return false;
                }
            }
            else if (node.name != null&&!node.name.Equals("*"))
            {
                if (!obj.name.Equals(node.name))
                {
                    return false;
                }
            }
            if (!String.IsNullOrEmpty(node.img))
            {
                List<string> img = uiHelper.GetInChildrenImages(obj);
                if (!img.Contains(node.img))
                {
                    return false;
                }
            }

            if (!String.IsNullOrEmpty(node.txt))
            {
                List<string> txts = uiHelper.GetInChildrenTexts(obj);
                if (!txts.Contains(node.txt))
                {
                    return false;
                }
            }
            return true;
        }
        
        /// <summary>
        ///从用户给出的路径中找到一条可以确定唯一的路径，通过GameObject.Find直接查找
        /// </summary>
        /// <param name="req"></param>
        /// <param name="rootPath"></param>
        /// <returns>从[0,returnValue)部分属于唯一可以定位的路径
        /// </returns>
        public int ParseRootPath(List<PathNode> nodes, StringBuilder rootPath)
        {
            int num = nodes.Count;
            if (num == 0 || !nodes[0].name.Equals("/"))
            {
                return 0;
            }
            
            //rootPath.Append("/");
            int firstGameobject = 1;
            if (nodes[firstGameobject].index <= 0 && String.IsNullOrEmpty(nodes[firstGameobject].img) && String.IsNullOrEmpty(nodes[firstGameobject].txt))
            {
                rootPath.Append("/");
                rootPath.Append(nodes[firstGameobject].name);
            }
            else
            {
                return 1;
            }
            return firstGameobject + 1;
        }


        private void FindGameObjectByParent(GameObject parent,List<GameObject> list, List<PathNode> nodes, int start)
        {

            if (parent == null) 
                return;
            if (nodes.Count == start)
            {
                list.Add(parent);
                return;
            }

            PathNode node = nodes[start];

            int childCount = parent.transform.childCount;
            List<GameObject> objs = new List<GameObject>();

            Logger.v("PathNode index = {0},name={1},txt={2},img={3}",node.index,node.name,node.txt,node.img);
            if (node.index >= 0 && node.index < childCount)
            {
                GameObject obj = parent.transform.GetChild(node.index).gameObject;

                if (FilterNode(obj, node))
                {
                    FindGameObjectByParent(obj, list, nodes, start + 1);
                }
            }
            else if(node.index<childCount)
            {
                for (int i = 0; i < childCount; i++)
                {
                    GameObject obj = parent.transform.GetChild(i).gameObject;

                    if (FilterNode(obj, node))
                    {
                        FindGameObjectByParent(obj, list, nodes, start + 1);
                    }
                }
            }
        }

        private void FindGameObjectByRootNode(string rootNode,List<GameObject> list,List<PathNode> nodes,int start)
        {
            Logger.d("Find GameObject by "+rootNode);
            GameObject root = GameObject.Find(rootNode);

            if (root == null)
            {
                return;
            }

            FindGameObjectByParent(root, list, nodes, start);
        }

        private void FindGameObjectByRootName(List<GameObject> list, List<PathNode> nodes)
        {
            if(nodes.Count==0)
            {
                return;
            }
            GameObject[] objs = GameObject.FindObjectsOfType<GameObject>();
            PathNode node=nodes[0];
            for (int i = 0; i < objs.Length; ++i)
            {
                GameObject obj=objs[i];
                if (node.index<0&&FilterNode(obj, node))
                {
                    FindGameObjectByParent(obj, list, nodes, 1);
                }
                else if (node.index >= 0)
                {
                    if (obj.transform.parent != null &&obj.transform.parent!=obj&&obj.transform.parent.childCount > node.index && obj.transform.parent.GetChild(node.index).gameObject == obj&&FilterNode(obj,node))
                    {
                        FindGameObjectByParent(obj, list, nodes, 1);
                    }
                }
            }
        }

        
        /// <summary>
        /// 通过表达式搜索当前场景中的符合的GameObject
        /// 
        /// 第一个节点"/"代表从根节点，如果不是代表可以从任意位置开始
        /// 
        /// 
        /// index：代表节点的位置。
        ///     parent
        ///    /      \
        /// index[0]  index[1]
        /// 
        /// szName:代表节点名称，"*"代表任意名称
        /// szText:代表节点的文字内容（当前GameObject的挂载的Compenent）
        /// szImg:图片名称,sprite或者texture名称
        /// 
        /// 
        /// /Canvas/Panel/Button 
        /// Canvas[0]{txt="hello"}/Button
        /// /Canvas/Panel/*[1]/Button
        /// 
        /// </summary>
        /// <param name="nodes"></param>
        /// <returns></returns>
        public List<GameObject> FindByPath(List<PathNode> nodes)
        {
            List<GameObject> list=new List<GameObject>();
            if (nodes == null||nodes.Count==0)
            {
                return list;
            }
            StringBuilder rootPath = new StringBuilder();
            int end = ParseRootPath(nodes, rootPath);

            if (end == 0)
            {
                //case: Canvas/Panel/Button
                Logger.w("Search not from Root, a cost method");
                FindGameObjectByRootName(list, nodes);
            }
            else if (end == 1)
            {
                //准确来说不存在这样的节点，根节点，且包含img或txt这是不可能的
                //case: /img="" txt=""/Button
                Logger.w("Root Node with condition");
                return list;
            }
            else
            {
                //可以先通过GameObject查找到部分
                Logger.v("Find Root Node by GameObject");
                FindGameObjectByRootNode(rootPath.ToString(), list, nodes, 2);
            }

            return list;                     
        }

        public List<GameObject> FindByPath(GameObject parent, List<PathNode> nodes)
        {
            List<GameObject> list = new List<GameObject>();
            if (parent==null||nodes == null || nodes.Count == 0)
            {
                return list;
            }
            Logger.d("Parent Gameobject " + parent.name);
            FindGameObjectByParent(parent, list, nodes, 0);
            
            return list;
        }

        public List<GameObject> FindByComponent(string name)
        {
            List<GameObject> objs = new List<GameObject>();
            Type type = ReflectionTools.TypeOf(name);

            if (type != null)
            {
                Component[] objArray = GameObject.FindObjectsOfType(type) as Component[];
                if (objArray != null)
                {
                    foreach (Component c in objArray)
                    {
                        objs.Add(c.gameObject);
                    }
                }
                
            }
            return objs;

        }

	}

}
