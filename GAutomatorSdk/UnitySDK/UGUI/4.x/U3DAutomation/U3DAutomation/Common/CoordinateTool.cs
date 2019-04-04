using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

namespace WeTest.U3DAutomation
{
	public class CoordinateTool
	{
        private static MobileScreen physicalscreen = null;

        public static bool GetCurrenScreenParam(ref float offsetx, ref float offsety, ref float scalex, ref float scaley)
        {
            //Logger.d("getCurrenScreenScale");
            if (RuntimePlatform.IPhonePlayer == Application.platform){
                scalex = 1;
                scaley = 1;
                offsetx = 0;
                offsety = 0;
                return true;
            }
            if (physicalscreen == null)
            {
                physicalscreen = AndroidRobot.getAndroidMScreen();

                //为了查问题用
                Logger.d("Screen.width=" + Screen.width + ", Screen.height=" + Screen.height);
                if (physicalscreen != null)
                {
                    Logger.d("physicalscreen.width=" + physicalscreen.width + " , physicalscreen.height=" + physicalscreen.height + "physicalscreen.x=" + physicalscreen.x + " , physicalscreen.y=" + physicalscreen.y);
                }
            }
            if (physicalscreen == null)
            {
                Logger.d("get physical screen failed.");
                return false;
            }


            int realphysicalwidth = physicalscreen.width;
            int realphysicalheight = physicalscreen.height;
            //做下面校验，是为了防止有些游戏登录时是竖屏、游戏里面是横屏
            //横屏的情况下
            if (Screen.width > Screen.height)
            {
                if (realphysicalwidth < realphysicalheight)
                {
                    realphysicalwidth = physicalscreen.height;
                    realphysicalheight = physicalscreen.width;
                }
            }
            //竖屏的情况下
            else if (Screen.width < Screen.height)
            {
                if (realphysicalwidth > realphysicalheight)
                {
                    realphysicalwidth = physicalscreen.height;
                    realphysicalheight = physicalscreen.width;
                }
            }

            float sx = (float)(realphysicalwidth / (Screen.width * 1.0));
            float sy = (float)(realphysicalheight / (Screen.height * 1.0));
            Logger.v("realphysicalwidth=" + realphysicalwidth + ", realphysicalheight=" + realphysicalheight);
            Logger.v("Screen.width=" + Screen.width + ", Screen.height=" + Screen.height);
            Logger.v("sx=" + sx + ", sy=" + sy);
            scalex = sx;
            scaley = sy;
            offsetx = physicalscreen.x;
            offsety = physicalscreen.y;
            return true;
        }


        public static Point ConvertMobile2Unity(Point pt)
        {
            if (pt == null) return null;
            float scalex = 0, scaley = 0, offsetx = 0, offsety = 0;
            Point ptNew = new Point(CoordinateType.UnityScreen);
            if (GetCurrenScreenParam(ref offsetx, ref offsety,ref scalex, ref scaley))
            {
                ptNew.X = (pt.X - offsetx) / scalex;
                ptNew.Y = Screen.height - (pt.Y - offsety) / scaley;

                Logger.d("point(" + pt.X + "," + pt.Y + ") => (" + ptNew.X + "," + ptNew.Y + ")");

            }
            return ptNew;
        }

        public static Point ConvertUnity2Mobile(Vector2 pt)
        {
            Point point = new Point();
            float scalex = 0, scaley = 0, offsetx = 0, offsety = 0;
            if (GetCurrenScreenParam( ref offsetx, ref offsety, ref scalex, ref scaley))
            {
                point.X = pt.x * scalex + offsetx;
                point.Y = (Screen.height - pt.y) * scaley + offsety;

                Logger.v("ConvertUnity2Mobile from point =(" + pt.x + ", " + pt.y + ") ==> ( " + point.X + ", " + point.Y + ")");
            }
            else
            {
                point.X = pt.x;
                point.Y = pt.y;
            }
            return point;
        }

        public static Rectangle ConvertUnity2Mobile(Rectangle rect)
        {
            Rectangle r = new Rectangle();
            float scalex = 0, scaley = 0, offsetx = 0, offsety = 0;
            if (GetCurrenScreenParam( ref offsetx, ref offsety, ref scalex, ref scaley))
            {
                r.x = rect.x * scalex + offsetx;
                r.y = (Screen.height - rect.y) * scaley + offsety;
                r.width = rect.width * scalex;
                r.height = rect.height * scaley;
            }
            else
            {
                r = rect;
            }
            return r;
        }


        public static Vector2 ConvertPoint2Vector(Point pt)
        {
            Vector2 vector = new Vector2(pt.X, pt.Y);
            return vector;
        }

        /// <summary>
        /// 将世界坐标点按指定的摄像机转化为屏幕坐标点
        /// </summary>
        /// <param name="c"></param>
        /// <param name="v"></param>
        /// <returns></returns>
        private static Point WorldPointToScreenPoint(Camera c, Vector3 v)
        {
            Vector3 v1 = c.WorldToScreenPoint(v);
            return new Point(v1.x, Screen.height - v1.y);
        }

        private static Vector3 WorldPointToScreenPoints(Camera c, Vector3 v)
        {
            Vector3 v1 = c.WorldToScreenPoint(v);
            return new Vector3(v1.x, Screen.height - v1.y,v1.z);
        }

        /// <summary>
        /// 根据一组屏幕坐标点计算出一个能包含这些点的最佳矩形位置
        /// </summary>
        /// <param name="pts"></param>
        /// <returns></returns>
        private static Rectangle CalculateBounds(Point[] pts)
        {
            float xmin = pts[0].X;
            float xmax = pts[0].X;
            float ymin = pts[0].Y;
            float ymax = pts[0].Y;

            foreach (Point pt in pts)
            {
                if (pt.X > xmax) xmax = pt.X;
                if (pt.X < xmin) xmin = pt.X;
                if (pt.Y > ymax) ymax = pt.Y;
                if (pt.Y < ymin) ymin = pt.Y;
            }

            return new Rectangle(xmin, ymin, xmax - xmin, ymax - ymin);
        }

        //public static Rectangle WorldBoundsToScreenRect(Camera cm, Bounds bounds)
        //{
        //    Vector3[] worldCorners = new Vector3[8];

        //    worldCorners[0] = new Vector3(bounds.center.x + bounds.extents.x, bounds.center.y + bounds.extents.y, bounds.center.z + bounds.extents.z);
        //    worldCorners[1] = new Vector3(bounds.center.x + bounds.extents.x, bounds.center.y + bounds.extents.y, bounds.center.z - bounds.extents.z);
        //    worldCorners[2] = new Vector3(bounds.center.x + bounds.extents.x, bounds.center.y - bounds.extents.y, bounds.center.z + bounds.extents.z);
        //    worldCorners[3] = new Vector3(bounds.center.x - bounds.extents.x, bounds.center.y + bounds.extents.y, bounds.center.z + bounds.extents.z);
        //    worldCorners[4] = new Vector3(bounds.center.x + bounds.extents.x, bounds.center.y - bounds.extents.y, bounds.center.z - bounds.extents.z);
        //    worldCorners[5] = new Vector3(bounds.center.x - bounds.extents.x, bounds.center.y + bounds.extents.y, bounds.center.z - bounds.extents.z);
        //    worldCorners[6] = new Vector3(bounds.center.x - bounds.extents.x, bounds.center.y - bounds.extents.y, bounds.center.z + bounds.extents.z);
        //    worldCorners[7] = new Vector3(bounds.center.x - bounds.extents.x, bounds.center.y - bounds.extents.y, bounds.center.z - bounds.extents.z);

        //    Point[] ptScreens = new Point[8];

        //    ptScreens[0] = WorldPointToScreenPoint(cm, worldCorners[0]);
        //    ptScreens[1] = WorldPointToScreenPoint(cm, worldCorners[1]);
        //    ptScreens[2] = WorldPointToScreenPoint(cm, worldCorners[2]);
        //    ptScreens[3] = WorldPointToScreenPoint(cm, worldCorners[3]);
        //    ptScreens[4] = WorldPointToScreenPoint(cm, worldCorners[4]);
        //    ptScreens[5] = WorldPointToScreenPoint(cm, worldCorners[5]);
        //    ptScreens[6] = WorldPointToScreenPoint(cm, worldCorners[6]);
        //    ptScreens[7] = WorldPointToScreenPoint(cm, worldCorners[7]);

        //    return CalculateBounds(ptScreens);
        //}

        public static Rectangle WorldBoundsToScreenRect(Camera mainCamera, Bounds bounds)
        {
            return WorldBoundsToScreenRect(mainCamera, bounds, false);
        }

        public static Rectangle WorldBoundsToScreenRect(Camera mainCamera, Bounds bounds, Boolean ignoreZ)
        {

            //计算出世界坐标系中的8个点
            Vector3 cen = bounds.center;
            Vector3 ext = bounds.extents;
            Vector3[] screenBoundsExtents = new Vector3[8];
            screenBoundsExtents[0] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x - ext.x, cen.y - ext.y, cen.z - ext.z));
            screenBoundsExtents[1] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x + ext.x, cen.y - ext.y, cen.z - ext.z));
            screenBoundsExtents[2] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x - ext.x, cen.y - ext.y, cen.z + ext.z));
            screenBoundsExtents[3] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x + ext.x, cen.y - ext.y, cen.z + ext.z));
            screenBoundsExtents[4] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x - ext.x, cen.y + ext.y, cen.z - ext.z));
            screenBoundsExtents[5] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x + ext.x, cen.y + ext.y, cen.z - ext.z));
            screenBoundsExtents[6] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x - ext.x, cen.y + ext.y, cen.z + ext.z));
            screenBoundsExtents[7] = WorldPointToScreenPoints(mainCamera, new Vector3(cen.x + ext.x, cen.y + ext.y, cen.z + ext.z));

            int margin = 20;
            int minimum = -margin;

            float xMin = minimum;
            float xMax = minimum;
            float yMin = minimum;
            float yMax = minimum;

            if (ignoreZ)
            {
                xMin = screenBoundsExtents[0].x;
                xMax = screenBoundsExtents[0].x;
                yMin = screenBoundsExtents[0].y;
                yMax = screenBoundsExtents[0].y;
            }

            for (int i = 0; i < screenBoundsExtents.Length; i++)
            {
                if (screenBoundsExtents[i].z >= 0.0)
                {
                    xMin = screenBoundsExtents[i].x;
                    xMax = screenBoundsExtents[i].x;
                    yMin = screenBoundsExtents[i].y;
                    yMax = screenBoundsExtents[i].y;
                    break;
                }
            }



            float widthMiddle = Screen.width * 0.5f;
            float heightMiddle = Screen.height * 0.5f;

            Boolean unvisible = false;

            for (int i = 0; i < screenBoundsExtents.Length; i++)
            {

                if (screenBoundsExtents[i].z < -0.1 && !ignoreZ)
                {
                    unvisible = true;
                }

                if (screenBoundsExtents[i].x < xMin)
                    xMin = screenBoundsExtents[i].x;

                else if (screenBoundsExtents[i].x > xMax)
                    xMax = screenBoundsExtents[i].x;

                if (screenBoundsExtents[i].y < yMin)
                    yMin = screenBoundsExtents[i].y;

                else if (screenBoundsExtents[i].y > yMax)
                    yMax = screenBoundsExtents[i].y;
            }

            if (unvisible)
            {
                Rectangle rect = new Rectangle(xMin, yMin, xMax - xMin, yMax - yMin);
                rect.visible = false;
                return rect;
            }
            return new Rectangle(xMin, yMin, xMax - xMin, yMax - yMin);
        }
	}
}
