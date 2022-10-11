using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

namespace WeTest.U3DAutomation
{
	public class GUINode
	{
        public GameObject gameObject;
            public GUINode parent;
            public List<GUINode> children;
            public int level = 0;//从0开始
            public int depth = 0;
            public string fullPath = "";

            public GUINode()
            {
                gameObject = null;
                parent = null;
                children = new List<GUINode>();
            }

            public GUINode(GameObject gameObject, GUINode parent, int level)
            {
                this.gameObject = gameObject;
                this.parent = parent;
                this.level = level;
                children = new List<GUINode>();
            }
	}

    public class UINode
    {
        private GameObject obj;
        private Point pt;
        private Rectangle rect;

        public UINode(GameObject gameobject, Point pt)
        {
            obj = gameobject;
            this.pt = pt;
        }

        public UINode(GameObject gameobject, Rectangle bound)
        {
            obj = gameobject;
            this.rect = bound;
        }

        public GameObject gameobject
        {
            get { return obj;}
        }

        public Point point
        {
            get { return pt; }
        }

        public Rectangle bound
        {
            get { return rect; }
        }
    }
}
