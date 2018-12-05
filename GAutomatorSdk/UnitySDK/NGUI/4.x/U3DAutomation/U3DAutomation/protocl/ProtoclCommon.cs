using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WeTest.U3DAutomation
{
    [Serializable]
    enum Cmd
    {
        EXIT = 0,//退出游戏
        ////////////////////////
        GET_VERSION = 100,//获取版本号
        FIND_ELEMENTS = 101,//查找节点
        FIND_ELEMENT_PATH = 102,//模糊查找
        GET_ELEMENTS_BOUND = 103,//获取节点的位置信息
        GET_ELEMENT_WORLD_BOUND = 104,//获取节点的世界坐标
        GET_UI_INTERACT_STATUS = 105,//获取游戏的可点击信息，包括scene、可点击节点，及位置信息
        GET_CURRENT_SCENE = 106,//获取Unity的Scene名称
        GET_ELEMENT_TEXT = 107,//获取节点的文字内容
        GET_ELEMENT_IMAGE = 108,//获取节点的图片名称
        GET_REGISTERED_HANDLERS = 109,//获取注册的函数的名称
        CALL_REGISTER_HANDLER = 110,//调用注册的函数
        SET_INPUT_TEXT = 111,//input控件更换文字信息
        GET_OBJECT_FIELD = 112,//反射获取对象属性值
        FIND_ELEMENTS_COMPONENT = 113,//获取所有包含改组件的gameobject
        SET_CAMERA_NAME = 114,//设置渲染的最佳的Camera
        GET_COMPONENT_METHODS = 115,//反射获取组件上的方法
        CALL_COMPONENT_MOTHOD = 116,//通过反射调用组件的函数
        LOAD_TEST_LIB = 117,//拉起test相关的库


        PRC_SET_METHOD = 118,//注册python端的方法
        RPC_METHOD = 119,//游戏内的接口可调用，python端的方法

        ///////////////////////////////////////////////
        HANDLE_TOUCH_EVENTS = 200,//发送down,move,up

        //////////////////////////////////////////////
        DUMP_TREE = 300,//获取节点树xml
        FIND_ELEMENT_BY_POS = 301,//根据位置信息获取节点内容

        //////////////////////////////////////////////
        GET_FPS = 400,//获取FPS
        GET_TRAFFIC_DATA = 401,//获取流量

        //////////////////////////////////////////////
        ENTER_RECORD = 500,//开始录制
        LEAVE_RECORD = 501,//结束录制
        TOUCH_NOTIFY = 502,//返回点击的节点


    }

    [Serializable]
    class VersionData
    {
        public string sdkVersion;//SDK版本号如1.0.1,主版本.子版本.修正版本
        public string engine;
        public string engineVersion;
        public string sdkUIType;//UGUI,NGUI

        public VersionData()
        {
            sdkVersion = VersionInfo.SDK_VERSION;
            engine = VersionInfo.ENGINE;
            sdkUIType = VersionInfo.SDK_UI;
        }
    }

    [Serializable]
    public class ElementInfo
    {
        //节点信息
        public int instance;
        public string name;

        public ElementInfo()
        {

        }
        public ElementInfo(string name, int instance)
        {
            this.name = name;
            this.instance = instance;
        }
    }

    [Serializable]
    public class PathNode
    {
        public string name; // 代表节点名称，/代表根节点,*代表任意一个或多节点
        public int index; // 子节点中的位置，从0开始。不是代表name相同的，而是直接子节点的位置。具有唯一性
        public string txt; // Label的内容
        public string img; // 图片sprite或者texture的名称
        public string regex; // name的正则表达式

        public PathNode(string name, int index, string txt, string img, string regex)
        {
            this.name = name;
            this.index = index;
            this.txt = txt;
            this.img = img;
            this.regex = regex;
        }

        public PathNode()
        {
            name = null;
            img = null;
            txt = null;
            regex = null;
            index = -1;
        }

    }

    [Serializable]
    public class BoundInfo
    {
        public int instance;
        public Boolean visible;
        public Boolean existed;
        public float width;
        public float height;
        public float x;
        public float y;
        public string path;

        public BoundInfo()
        {
            existed = true;
            visible = true;
            path = "";
        }
    }

    [Serializable]
    public class AppNetTrafficRes
    {
        public int input;
        public int output;
        public AppNetTrafficRes()
        {
        }
    }

    [Serializable]
    public class AppNetReq
    {
        public int uid;
    }

    [Serializable]
    public class CustomCaller
    {
        public string name;//名称
        public string args;//参数

        public CustomCaller(string name, string args)
        {
            this.name = name;
            this.args = args;
        }

        public CustomCaller()
        {

        }
    }

    [Serializable]
    public class InteractStatus
    {
        public string scenename;
        public List<InteractElement> elements;

    }

    [Serializable]
    public class InteractElement
    {
        public string name;
        public int instanceid;
        public AutoTravelNodeType nodetype;
        public AutoBound bound;

        public InteractElement()
        {
            bound = new AutoBound();
        }
    }

    [Serializable]
    public class AutoBound
    {
        public float x;
        public float y;
        public float fWidth;
        public float fHeight;
    }

    [Serializable]
    public enum AutoTravelNodeType
    {
        BUTTON = 1, // 按钮类型的
        IMG = 2, // 图片类型的
        TXT = 3, // 文字类型的
        INPUTXT = 4,//输入框
        INPUTPAS = 5,//密码框
        OTHER = 6, // 其他类型的
    }

    [Serializable]
    public enum TouchType
    {
        TOUCH_DOWN = 1, // 按下
        TOUCH_UP = 2, // 抬起
        TOUCH_MOVE = 3, // 移动
    }

    //点击事件
    [Serializable]
    public class TouchEvent
    {
        public float x;
        public float y;
        public int sleeptime;
        public MotionEventAction type;
    }

    //设置文字内容的请求信息
    [Serializable]
    public class TextSetter
    {
        public int instance;
        public string content;
    }

    //世界坐标系
    [Serializable]
    public class WorldBound
    {
        public int id;
        public Boolean existed;
        public float centerX;//中心点
        public float centerY;
        public float centerZ;
        public float extentsX;//中心点到其他位置
        public float extentsY;
        public float extentsZ;
    }

    [Serializable]
    public class TouchData
    {
        public float deltatime; // 距离上一次输入的时间，单位为秒
        public byte phase; // 类型，ref:ATElementType
        public float x; // x坐标,手机屏幕坐标
        public float y; // y坐标，手机屏幕坐标
        public float relativeX; // x相对坐标,手机屏幕坐标
        public float relativeY; // y相对坐标，手机屏幕坐标
        public short fingerId; // 用以唯一标示手指

        /* construct methods */
        public TouchData()
        {
        }
    }

    [Serializable]
    public class TouchNotify
    {
        public string scene;
        public string name;
        public List<TouchData> touches;

        public TouchNotify()
        {
            scene = "";
            name = "";
            touches = new List<TouchData>();
        }
    }

    //反射获取属性
    [Serializable]
    public class ComponentField
    {
        public int instance;
        public string comopentName;
        public string attributeName;
    }

    //反射获取属性
    [Serializable]
    public class ComponentMethod
    {
        public int instance;
        public string comopentName;
    }

    //反射获取属性
    [Serializable]
    public class MethodDetail
    {
        public string methodName;
        public string returnType;
        public string[] parameterTypes;
    }

    //反射获取属性
    [Serializable]
    public class ComponentMethodCall
    {
        public int instance;
        public string comopentName;
        public string methodName;
        public object[] parameters;
    }

    [Serializable]
    public class DumpTree
    {
        public string scene;
        public string xml;

        public DumpTree()
        {
            scene = "";
            xml = "";
        }
    }

    [Serializable]
    public class RPCRequestBody
    {
        public string name;
        public string value;
        public int seq;
    }

    [Serializable]
    public class RPCResponseBody
    {
        public string name;
        public string returnValue;
        public int status;//无异常为0,调用删除抛出异常为0
        public int seq;
    }
}
