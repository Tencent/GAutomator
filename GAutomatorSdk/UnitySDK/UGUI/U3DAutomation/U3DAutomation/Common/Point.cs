using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WeTest.U3DAutomation
{

    public enum CoordinateType
    {
        MobileScreen,
        UnityScreen
    };
    public class Point
    {
        float x;
        float y;
        CoordinateType type;

        public float X
        {
            get { return x; }
            set { x = value; }
        }

        public float Y
        {
            get { return y; }
            set { y = value; }
        }

        public CoordinateType Type
        {
            get { return type;}
        }

        public Point(CoordinateType type)
        {
            this.type=type;
        }

        public Point(float x, float y)
        {
            this.x = x;
            this.y = y;
        }
        public Point(float x, float y,CoordinateType type)
        {
            this.x = x;
            this.y = y;
            this.type=type;
        }

        public Point()
        {
            x = 0;
            y = 0;
        }

        public override string ToString()
        {
            StringBuilder sb = new StringBuilder();

            sb.Append("x=");
            sb.Append(x.ToString());
            sb.Append("; y=");
            sb.Append(y.ToString());

            return sb.ToString();
        }        
    }
}
