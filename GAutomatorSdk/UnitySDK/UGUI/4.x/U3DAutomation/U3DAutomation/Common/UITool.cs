using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;


namespace WeTest.U3DAutomation
{
    public class Rectangle
    {
        public float _x;
        public float _y;
        public float _width;
        public float _height;
        public bool _visible;

        public bool visible
        {
            get { return _visible; }
            set { _visible = value; }
        }

        public float x
        {
            get { return _x; }
            set { _x = value; }
        }

        public float y
        {
            get { return _y; }
            set { _y = value; }
        }

        public float width
        {
            get { return _width; }
            set { _width = value; }
        }

        public float height
        {
            get { return _height; }
            set { _height = value; }
        }

        public Rectangle()
        {
            x = 0;
            y = 0;
            width = 0;
            height = 0;
            visible = true;
        }

        public Rectangle(float x, float y, float width, float height)
        {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
            this.visible = true;
        }

        public Rect ToRect()
        {
            return new Rect(x, y, width, height);
        }

        public bool ContainPt(Point pt)
        {
            return pt.X > _x && pt.X < _x + _width && pt.Y > _y && pt.Y < _y + _height;
        }

        public override string ToString()
        {
            StringBuilder sb = new StringBuilder();

            sb.Append("x=");
            sb.Append(_x.ToString());
            sb.Append("; y=");
            sb.Append(_y.ToString());
            sb.Append("; width=");
            sb.Append(_width.ToString());
            sb.Append("; height=");
            sb.Append(_height.ToString());

            return sb.ToString();
        }
    }

    //interface UIHelper
    //{

    //    string GetText(GameObject obj);

    //    string GetImage(GameObject obj);

    //    List<string> GetInChildrenImages(GameObject obj);

    //    List<string> GetInChildrenTexts(GameObject obj);

    //    Rectangle GetBound(GameObject obj);

    //    string SetInputText(GameObject obj, string content); //设置文字内容

    //    WorldBound GetWorldBound(GameObject obj);//获取GameObject的世界坐标

    //    /// <summary>
    //    ///  输入屏幕坐标，找到这个屏幕坐标对应的UI控件
    //    /// </summary>
    //    /// <param name="pt"></param>
    //    /// <returns></returns>
    //    List<GameObject> FindGameObjectsByPoint(Point pt);

    //    /// <summary>
    //    /// 获取游戏当前界面可点击的节点
    //    /// </summary>
    //    /// <returns></returns>
    //    List<InteractElement> GetInteractElements();

    //    bool IsVisible(GameObject obj);

    //}

    class UIBase
    {
        public static String cameraName = null;

        public static String setCamera(String name)
        {
            Logger.d("Set render Camera " + name);
            String old = cameraName;
            if (name != null)
            {
                cameraName = name;
            }
            return cameraName;
        }


        /// <summary>
        /// 找到最适合的渲染的Camera
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public static Camera FindBestCamera(GameObject obj)
        {
            if (cameraName != null && !cameraName.Equals(""))
            {
                GameObject gameobject = GameObject.Find(cameraName);
                if (obj != null)
                {
                    Camera c = gameobject.GetComponent<Camera>();
                    if (c != null)
                    {
                        Logger.v("Find setting camera");
                        return c;
                    }
                }
            }

            Camera[] camerasArray = Camera.allCameras;
            List<Camera> cameras = new List<Camera>();

            //找到渲染改GameObject的Camera
            for (int i = 0; i < camerasArray.Length; ++i)
            {
                if ((camerasArray[i].cullingMask & (1 << obj.layer)) == (1 << obj.layer))
                {
                    cameras.Add(camerasArray[i]);
                }
            }

            cameras.Sort(
                delegate(Camera p1, Camera p2)
                {
                    return (int)(p2.depth - p1.depth);
                });

            for (int i = 0; i < cameras.Count; ++i)
            {
                if (cameras[i] == null || !cameras[i].gameObject.activeInHierarchy)
                {
                    continue;
                }
                //TODO,如果有多个的情况情况下，选渲染GameObject最大的那个
                return cameras[i];
            }
            return null;

        }

        public Camera FindBestCamera()
        {
            return Camera.main;
        }

        public Rectangle GetBoundByRender(Camera cm, GameObject obj)
        {
            Renderer render = obj.GetComponent<Renderer>();
            if (render != null&&render.isVisible)
            {
                return CoordinateTool.WorldBoundsToScreenRect(cm, render.bounds);
            }

            return null;
        }

        public Rectangle GetBoundByCollider(Camera cm, GameObject obj)
        {

            return GetBoundByCollider(cm, obj, false);
        }

        public Rectangle GetBoundByCollider(Camera cm, GameObject obj, Boolean ignoreZ)
        {

            Collider collider = obj.GetComponent<Collider>();
            if (obj.activeInHierarchy && collider != null && collider.enabled)
            {
                return CoordinateTool.WorldBoundsToScreenRect(cm, collider.bounds, ignoreZ);
            }

            return null;
        }


        public Rectangle GetBoundByMesh(Camera cm, GameObject obj)
        {
            MeshFilter meshFilter = obj.GetComponent<MeshFilter>();
            if (meshFilter != null && meshFilter.sharedMesh != null)
            {
                //Logger.d("By MeshFilter");
                Mesh mesh = meshFilter.sharedMesh;
                return CoordinateTool.WorldBoundsToScreenRect(cm, mesh.bounds);
            }

            return null;
        }

        public Rectangle GetGUIBound(Camera cm, GameObject obj)
        {

            Rectangle rect = null;

            if ((rect = GetBoundByRender(cm,obj)) != null)
            {
                return rect;
            }
            else if ((rect = GetBoundByCollider(cm,obj)) != null)
            {
                return rect;
            }
            else if ((rect = GetBoundByMesh(cm,obj)) != null)
            {
                return rect;
            }

            return null;
        }

        public bool IsVisible(GameObject obj)
        {
            return obj.activeSelf && obj.hideFlags == HideFlags.None;
        }

        private WorldBound Vector2WorldBound(Vector3 center, Vector3 extents)
        {
            WorldBound worldBound = new WorldBound();
            worldBound.centerX = center.x;
            worldBound.centerY = center.y;
            worldBound.centerZ = center.z;
            worldBound.extentsX = extents.x;
            worldBound.extentsY = extents.y;
            worldBound.extentsZ = extents.z;
            worldBound.existed = true;
            return worldBound;


        }

        public WorldBound GetWorldBound(GameObject gameobject)
        {
            Vector3 center = new Vector3();
            Vector3 extents = new Vector3();
            WorldBound worldBound;
            Renderer render = gameobject.GetComponent<Renderer>();
            if (render != null)
            {
                center = render.bounds.center;
                extents = render.bounds.extents;
                worldBound = Vector2WorldBound(center, extents);
                return worldBound;
            }

            MeshFilter meshFilter = gameobject.GetComponent<MeshFilter>();
            if (meshFilter != null && meshFilter.sharedMesh != null)
            {
                //Logger.d("By MeshFilter");
                Mesh mesh = meshFilter.sharedMesh;
                center = mesh.bounds.center;
                extents = mesh.bounds.extents;
                worldBound = Vector2WorldBound(center, extents);
                return worldBound;
            }

            Collider collider = gameobject.GetComponent<Collider>();
            if (gameobject.activeInHierarchy && collider != null && collider.enabled)
            {
                center = collider.bounds.center;
                extents = collider.bounds.extents;
                worldBound = Vector2WorldBound(center, extents);
                return worldBound;
            }
            worldBound = new WorldBound();
            worldBound.existed = false;
            return worldBound;
        }
    }

}
