using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using UnityEngine;

namespace WeTest.U3DAutomation
{
    //弱引用的表
    class GameObjectTable
    {
        Dictionary<int, WeakReference> dict = new Dictionary<int, WeakReference>();
        public int Add(GameObject obj)
        {
            int instance = obj.GetInstanceID();
            if(dict.ContainsKey(instance))
            {
                return instance;
            }
            dict.Add(instance, new WeakReference(obj));
            return instance;
        }

        public GameObject Find(int intanceID)
        {
            WeakReference gameObjectReference = null;

            if (dict.TryGetValue(intanceID, out gameObjectReference))
            {
                if (gameObjectReference != null)
                {
                    GameObject obj = gameObjectReference.Target as GameObject;
                    if (obj == null)
                    {
                        dict.Remove(intanceID);
                    }
                    return obj;
                }
                
            }
            return null;
        }
    }
}
