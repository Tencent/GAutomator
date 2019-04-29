using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;
using System.IO;
using UnityEngine.EventSystems;
using System.Threading;

namespace WeTest.U3DAutomation
{
    class CommandHandler
    {
        private delegate void CmdHandler(Command cmd);

        private long startTime = 0;

        private static CommandHandler instance = new CommandHandler();
        private Dictionary<Cmd, CmdHandler> handlers = new Dictionary<Cmd, CmdHandler>();

        private double sdkUseTime = 0.0f;//SDK使用的时间，计算FPS时应该扣除
        public float updateInterval = 0.5F;
        private double lastInterval;
        private int frames = 0;
        private float fps = 0.0f;

        private int recvByte = 0;//SDK接收到的流量
        private int sendByte = 0;//SDK发送的流量
        private object netlocker = new object();
        private bool netReadInvaild = true;//流量读取方式是否有效

        public Boolean RecordMode = false;
        public Socket recordSocket;

        private UGUIHelper uiHelper;

        private void InitCmdHandlerMap()
        {
            handlers.Add(Cmd.GET_VERSION, new CmdHandler(handleGetVersion));
            handlers.Add(Cmd.FIND_ELEMENTS, new CmdHandler(handleGetElements));
            handlers.Add(Cmd.FIND_ELEMENT_PATH, new CmdHandler(handleGetElementsByPath));
            handlers.Add(Cmd.GET_ELEMENTS_BOUND, new CmdHandler(handleGetElementsBound));
            handlers.Add(Cmd.GET_ELEMENT_TEXT, new CmdHandler(handleGetNodeText));
            handlers.Add(Cmd.GET_ELEMENT_IMAGE, new CmdHandler(handleGetNodeImage));
            handlers.Add(Cmd.DUMP_TREE, new CmdHandler(handleDumpTree));
            handlers.Add(Cmd.GET_REGISTERED_HANDLERS, new CmdHandler(handleGetRegisterHandlers));
            handlers.Add(Cmd.CALL_REGISTER_HANDLER, new CmdHandler(handleCallRegisteredHandler));
            handlers.Add(Cmd.GET_CURRENT_SCENE, new CmdHandler(handleGetCurrentScene));
            handlers.Add(Cmd.GET_UI_INTERACT_STATUS, new CmdHandler(handleInteractStatus));
            handlers.Add(Cmd.HANDLE_TOUCH_EVENTS, new CmdHandler(handleTouchActions));
            handlers.Add(Cmd.SET_INPUT_TEXT,new CmdHandler(handleSetInputText));
            handlers.Add(Cmd.GET_ELEMENT_WORLD_BOUND, new CmdHandler(handleGetWorldBound));
            handlers.Add(Cmd.FIND_ELEMENT_BY_POS, new CmdHandler(handleGetElementByPos));
            handlers.Add(Cmd.GET_FPS, new CmdHandler(handleGetFPS));
            handlers.Add(Cmd.GET_TRAFFIC_DATA, new CmdHandler(handleGetStreamData));
            handlers.Add(Cmd.ENTER_RECORD, new CmdHandler(handleEnterRecord));
            handlers.Add(Cmd.LEAVE_RECORD, new CmdHandler(handleLeaveRecord));
            handlers.Add(Cmd.GET_OBJECT_FIELD, new CmdHandler(handleGetObjectField));
            handlers.Add(Cmd.FIND_ELEMENTS_COMPONENT, new CmdHandler(handleGetElementsByComponent));
            handlers.Add(Cmd.SET_CAMERA_NAME, new CmdHandler(handleSetCamera));
            handlers.Add(Cmd.GET_COMPONENT_METHODS, new CmdHandler(handleGetObjectMethods));
            handlers.Add(Cmd.CALL_COMPONENT_MOTHOD, new CmdHandler(handleCallObjectMethod));
            handlers.Add(Cmd.LOAD_TEST_LIB, new CmdHandler(handleLoadTestLib));
        }
        private CommandHandler()
        {
            InitCmdHandlerMap();
            uiHelper = new UGUIHelper();
            startTime = DateTime.Now.Ticks / 10000;
        }

        public static CommandHandler INSTANCE
        {
            get { return instance; }
        }

        public IEnumerator HandleCommand()
        {
            while (true)
            {
                Command command = CommandDispatcher.GetCommand();
                if (command == null)
                {
                    yield return null;
                }
                else
                {
                    Logger.v("Find command : " + command.cmd + " value :" + command.recvObj);
                    try
                    {
                        CmdHandler handler = null;
                        if (handlers.TryGetValue(command.cmd,out handler))
                        {
                            long beg = DateTime.Now.Ticks / 10000;
                            handler(command);
                            StringBuilder sb = new StringBuilder();
                            sb.Append("[");
                            sb.Append(command.socket);
                            sb.Append("] Cmd: ");
                            sb.Append(command.cmd);
                            sb.Append(" costs: ");
                            sb.Append(DateTime.Now.Ticks / 10000 - beg);
                            sb.Append("ms");
                            Debug.Log(sb.ToString());
                            sdkUseTime += (DateTime.Now.Ticks / 10000 - beg) / 1000;

                        }
                        else
                        {
                            //没法找到
                            command.status = ResponseStatus.NO_SUCH_CMD;
                            CommandDispatcher.SendCommand(command);
                        }
                    }
                    catch (System.Exception ex)
                    {
                        Logger.d("Handle Command expection =>" + ex.Message + " \n" + ex.StackTrace);
                        command.status = ResponseStatus.UN_KNOW_ERROR;
                    CommandDispatcher.SendCommand(command);
                }
                    
                }
                yield return null;
            }
            
        }

        protected void InjectTouchEvent()
        {
            try
            {
       //         Logger.d("InjectTouchEvent");
                List<TouchEvent> events = TouchEventHandler.INSTANCE.GetTouchEvents();

                if (events != null)
                {
                    float offsetx = 0, offsety = 0, scalex = 0, scaley = 0;
                    if (CoordinateTool.GetCurrenScreenParam(ref offsetx, ref offsety, ref scalex, ref scaley))
                    {
                        for (int i = 0; i < events.Count; ++i) {
                            events[i].x -= offsetx;
                            events[i].y -= offsety;
                        }
                    }

                    for (int i = 0; i < events.Count; ++i)
                    {
                        TouchEvent touchEvent=events[i];
                        AndroidRobot.INSTANCE.InjectMotionEvent(touchEvent.x, touchEvent.y, touchEvent.type);
                    }
                }
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + "\n" + ex.StackTrace);
            }
        }

        protected void NotifyTouchElement()
        {
            try
            {
                Cmd cmd = Cmd.TOUCH_NOTIFY;
                Command command = new Command(cmd, recordSocket);
                Touch[] touchs = Input.touches;
                int fingerNum = touchs.Length;
                if (fingerNum == 0)
                {
                    return;
                }
                bool finded = false;
                TouchNotify touchNotify = new TouchNotify();
                string scene = Application.loadedLevelName;
                touchNotify.scene = scene;
                for (int i = 0; i < fingerNum && i < 5; ++i)
                {
                    Touch t = touchs[i];
                    Logger.d("Touch delta time = {0},x = {1},y={2} ,fingerId = {3},phase = {4}", t.deltaTime * Time.timeScale, t.position.x, t.position.y, t.fingerId, t.phase);
                    //只考虑，一个点的情况，Begin的时候
                    if (t.phase == TouchPhase.Began && !finded)
                    {
                        GameObject selectedObj = null;
                        try
                        {
                            selectedObj = UGUITools.GetUIElementbyRaycastByUnity(new Point(t.position.x, t.position.y));
                        }
                        catch (System.Exception ex)
                        {
                            Logger.v(ex.StackTrace);
                        }
                        if (selectedObj != null && UGUITools.IsInteraction(selectedObj))
                        {
                            finded = true;
                            string name = GameObjectTool.GenerateNamePath(selectedObj);
                            Logger.d("Touch UI = " + name);
                            touchNotify.name = name;
                        }
                    }
                    if (t.phase == TouchPhase.Canceled || t.phase == TouchPhase.Stationary || t.phase == TouchPhase.Moved)
                    {
                        continue;
                    }
                    TouchData td = new TouchData();
                    td.deltatime = DateTime.Now.Ticks / 10000 - startTime;
                    td.fingerId = (short)t.fingerId;
                    Point point = CoordinateTool.ConvertUnity2Mobile(t.position);
                    td.x = point.X;
                    td.y = point.Y;
                    td.relativeX = t.position.x / Screen.width;
                    td.relativeY = (Screen.height - t.position.y) / Screen.height;
                    switch (t.phase)
                    {
                        case TouchPhase.Began:
                            td.phase = (byte)TouchType.TOUCH_DOWN;
                            break;
                        //case TouchPhase.Moved:
                        //    td.bPhase = (byte)ATTouchType.AT_TOUCH_MOVE;
                        //    break;
                        case TouchPhase.Ended:
                            td.phase = (byte)TouchType.TOUCH_UP;
                            break;
                    }
                    touchNotify.touches.Add(td);
                }
                if (touchNotify.touches.Count>0)
                {
                    command.sendObj = touchNotify;
                    CommandDispatcher.SendCommand(command);
                }
                
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + "\n" + ex.StackTrace);
                Cmd cmd = Cmd.TOUCH_NOTIFY;
                Command command = new Command(cmd, recordSocket);
                command.sendObj = ex.Message + "\n" + ex.StackTrace;
                command.status = ResponseStatus.UN_KNOW_ERROR;
                CommandDispatcher.SendCommand(command);
            }
        }

        /// <summary>
        /// 该函数，每次update都会运行
        /// </summary>
        public void HandleEvent()
        {
            InjectTouchEvent();

            if (RecordMode)
            {
                NotifyTouchElement();
            }
        }

        protected void handleGetVersion(Command command)
        {
            //Thread.Sleep(5000);//测试超时
            VersionData version = new VersionData();
            version.engineVersion = Application.unityVersion;
            command.sendObj = version;
            Logger.d("Engine=" + version.engine + "; Version=" + version.sdkVersion + "; UnityVersion=" +version.engineVersion+"; UI="+version.sdkUIType);
            CommandDispatcher.SendCommand(command);
        }

        protected void handleLoadTestLib(Command command)
        {
            try
            {
                Logger.d("handleLoadTestLib");
                ReflectionTools.testLibInit();
                command.sendObj = "OK";
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message;
            }
            CommandDispatcher.SendCommand(command);
        }

        /// <summary>
        /// 根据名称查找控件。控件不存在则返回instance=-1
        /// </summary>
        /// <param name="command"></param>
        protected void handleGetElements(Command command)
        {
            Logger.d("handleGetElements " + command.recvObj);
            List<string> elementNames = JsonParser.Deserialization<List<string>>(command);
            List<ElementInfo> elements = new List<ElementInfo>();
            foreach (string s in elementNames)
            {
                Logger.d("element name = " + s);
                ElementInfo e = new ElementInfo();
                elements.Add(e);
                try
                {
                    GameObject obj = GameObjectManager.INSTANCE.FindGameObject(s);
                    if (obj != null)
                    {
                        e.instance = GameObjectManager.INSTANCE.AddGameObject(obj);
                        e.name = s;
                    }
                    else
                    {
                        e.instance = -1;
                        e.name = s;
                    }

                }
                catch (System.Exception ex)
                {
                    Logger.w(ex.Message + " " + ex.StackTrace);
                    e.instance = -1;
                }
            }
            command.sendObj = elements;
            CommandDispatcher.SendCommand(command);
        }

        protected void handleGetElementsByPath(Command command)
        {
            Logger.d("handleGetElementsByPath " + command.recvObj);
            List<PathNode> pathNodes = JsonParser.Deserialization<List<PathNode>>(command);
            List<GameObject> objs;
            List<ElementInfo> elements = new List<ElementInfo>();
            command.sendObj = elements;
            try
            {
                objs = GameObjectManager.INSTANCE.FindByPath(pathNodes);
                foreach (GameObject obj in objs)
                {
                    if (obj != null && obj.activeInHierarchy)
                    {
                        string name = GameObjectTool.GenerateNamePath(obj);
                        int instance = GameObjectManager.INSTANCE.AddGameObject(obj);
                        ElementInfo e = new ElementInfo(name, instance);
                        elements.Add(e);
                        Logger.d("Element name = " + e.name + " ,instance =" + e.instance);
                    }

                }
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
            }
            CommandDispatcher.SendCommand(command);

        }

        /// <summary>
        /// 根据组件查找节点
        /// </summary>
        /// <param name="command"></param>
        protected void handleGetElementsByComponent(Command command)
        {
            Logger.d("handleGetElementsByComponent " + command.recvObj);
            List<string> componentNames = JsonParser.Deserialization<List<string>>(command);

            string componentName = componentNames[0];

            List<GameObject> objs;
            List<ElementInfo> elements = new List<ElementInfo>();
            command.sendObj = elements;
            try
            {
                objs = GameObjectManager.INSTANCE.FindByComponent(componentName);
                foreach (GameObject obj in objs)
                {
                    string name = GameObjectTool.GenerateNamePath(obj);
                    int instance = GameObjectManager.INSTANCE.AddGameObject(obj);
                    ElementInfo e = new ElementInfo(name, instance);
                    elements.Add(e);
                    Logger.d("Element name = " + e.name + " ,instance =" + e.instance);

                }
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
            }
            CommandDispatcher.SendCommand(command);
        }

        /// <summary>
        /// 获取GameObject在屏幕上的位置信息
        /// </summary>
        /// <param name="command"></param>
        protected void handleGetElementsBound(Command command)
        {
            Logger.d("handleGetElementsBound: "+command.recvObj);
            List<int> instances = JsonParser.Deserialization<List<int>>(command);
            List<BoundInfo> boundInfos = new List<BoundInfo>();

           
            foreach (int instance in instances)
            {
                GameObject obj = GameObjectManager.INSTANCE.FindGameObjectGlobal(instance);
                BoundInfo bound = new BoundInfo();
                bound.instance = instance;
                boundInfos.Add(bound);
                try
                {
                    if (obj != null)
                    {
                        Rectangle rc = uiHelper.GetBound(obj);
                        if (rc == null)
                        {
                            bound.visible = false;
                        }
                        else
                        {
                            bound.x = rc.x;
                            bound.y = rc.y;
                            bound.width = rc.width;
                            bound.height = rc.height;
                            bound.visible = obj.activeInHierarchy;
                            
                        }
                        bound.path = GameObjectTool.GenerateNamePath(obj); 
                    }
                    else
                    {
                        bound.existed = false;
                    }
                }
                catch (System.Exception ex)
                {
                    Logger.w(ex.Message+" "+ex.StackTrace);
                    bound.visible = false;
                }
                
            }

            foreach (BoundInfo b in boundInfos)
            {
                Logger.d("Bound width = " + b.width + " height = " + b.height + " x = " + b.x + " y=" + b.y + " existed = " + b.existed + " visible = " + b.visible);
            }
            command.sendObj = boundInfos;
            CommandDispatcher.SendCommand(command);
        }

        protected void handleGetNodeText(Command command)
        {
            Logger.d("handleGetNodeText +" + command.recvObj);
            try
            {
                int instance = int.Parse(command.recvObj);
                GameObject gameObject = GameObjectManager.INSTANCE.FindGameObjectGlobal(instance);
                if (null == gameObject)
                {
                    //返回无该gameobject
                    command.status = ResponseStatus.GAMEOBJ_NOT_EXIST;
                    command.sendObj = "GameObject " + instance + " is not exists";
                    return;
                }
                string text = uiHelper.GetText(gameObject);
                if (text == null)
                {
                    //command.status = ResponseStatus.COMPONENT_NOT_EXIST;
                    //command.sendObj = "Component Text/GUIText " + instance + " is not exists";
                    command.sendObj = "No Component with text";
                    command.status = ResponseStatus.NO_SUCH_RESOURCE;
                }
                else
                {
                    command.sendObj = text;
                }
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
            CommandDispatcher.SendCommand(command);
            
        }

        protected void handleGetNodeImage(Command command)
        {
            Logger.d("handleGetNodeImage +" + command.recvObj);
            int instance = int.Parse(command.recvObj);
            try
            {
                GameObject gameObject = GameObjectManager.INSTANCE.FindGameObjectGlobal(instance);
                if (null == gameObject)
                {
                    //返回无该gameobject
                    command.status = ResponseStatus.GAMEOBJ_NOT_EXIST;
                    command.sendObj = "GameObject " + instance + " is not exists";
                    return;
                }
                string image = uiHelper.GetImage(gameObject);
                if (image == null)
                {
                    //command.status = ResponseStatus.COMPONENT_NOT_EXIST;
                    //command.sendObj = "Component Image/RawImage/SpriteRender " + instance + " is not exists";
                    command.sendObj = "No Component with image";
                    command.status = ResponseStatus.NO_SUCH_RESOURCE;
                }
                else
                {
                    command.sendObj = image;
                }
                
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
           
            CommandDispatcher.SendCommand(command);
           
        }

        protected void handleDumpTree(Command command)
        {
            Logger.d("handleDumpTree ");
            try
            {
                string xml = GameObjectTool.DumpTree();
                string scene = Application.loadedLevelName;
                DumpTree dumpTree = new DumpTree();
                dumpTree.scene = scene;
                dumpTree.xml = xml;
                command.sendObj = dumpTree;
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
            CommandDispatcher.SendCommand(command);
        }

        protected void handleGetRegisterHandlers(Command command)
        {
            Logger.d("handleGetRegisterHandlers");

            try
            {
                List<string> lists = CustomHandler.GetRegistered();
                command.sendObj = lists;
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
            CommandDispatcher.SendCommand(command);
        }

        protected void handleCallRegisteredHandler(Command command)
        {

            Logger.d("handleCallRegisteredHandler");

            try
            {
                CustomCaller caller = JsonParser.Deserialization<CustomCaller>(command);
                string result;
                bool r = CustomHandler.Call(caller.name, caller.args, out result);
                if (r)
                {
                    command.sendObj = result;
                }
                else
                {
                    command.status = ResponseStatus.NO_SUCH_HANDLER;
                    command.sendObj = "No such handler: " + caller.name;
                }
            }
            catch(System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
            CommandDispatcher.SendCommand(command);
        }

        protected void handleGetCurrentScene(Command command)
        {
            Logger.d("handleGetCurrentScene");
            try
            {
                command.sendObj = Application.loadedLevelName;
            }
            catch(System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
            Logger.d("scene :" + command.sendObj);
            CommandDispatcher.SendCommand(command);
        }

        protected void handleInteractStatus(Command command)
        {
            Logger.d("handleGetCurrentScene");
            List<String> buttonTypes = null;
            try
            {
                buttonTypes = JsonParser.Deserialization<List<String>>(command);
            }
            catch (System.Exception ex)
            {
                buttonTypes = new List<string>();
            }
            try
            {
                
                InteractStatus status=new InteractStatus();

                List<InteractElement> elements = uiHelper.GetInteractElements(buttonTypes);

                status.elements = elements;

                status.scenename = U3DManager.GetSceneName();

                command.sendObj = status;
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
            CommandDispatcher.SendCommand(command);
        }

        protected void handleTouchActions(Command command)
        {
            Logger.d("HandleTouchActions");

            TouchEvent[] events=null;
            if (command.recvObject != null)
            {
                events=(TouchEvent[])command.recvObject;
            }else{
                events = JsonParser.Deserialization<TouchEvent[]>(command);
            }

            float scalex = 0, scaley = 0, offsetx = 0, offsety = 0;
            Point ptNew = new Point(CoordinateType.UnityScreen);
         
            TouchActions actions = new TouchActions();
            actions.cmd = command;
            actions.events = events;

            TouchEventHandler.INSTANCE.AddTouchActions(actions);
        }


        protected void handleSetInputText(Command command)
        {
            Logger.d("handleSetInputText +" + command.recvObj);
            TextSetter textSetter=JsonParser.Deserialization<TextSetter>(command);
            try
            {
                GameObject gameObject = GameObjectManager.INSTANCE.FindGameObjectGlobal(textSetter.instance);
                if (null == gameObject)
                {
                    //返回无该gameobject
                    command.status = ResponseStatus.GAMEOBJ_NOT_EXIST;
                    command.sendObj = "GameObject " + instance + " is not exists";
                    CommandDispatcher.SendCommand(command);
                    return;
                }
                else
                {
                    string oldContent=uiHelper.SetInputText(gameObject, textSetter.content);
                    command.sendObj = oldContent;
                }

            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }

            CommandDispatcher.SendCommand(command);
        }

        protected void handleGetWorldBound(Command command)
        {
            Logger.d("handleGetWorldBound");

            List<int> instances = JsonParser.Deserialization<List<int>>(command);
            List<WorldBound> worldBounds = new List<WorldBound>();

            for (int i = 0; i < instances.Count; ++i)
            {
                int instance = instances[i];
                GameObject obj = GameObjectManager.INSTANCE.FindGameObjectGlobal(instance);
                WorldBound worldBound = null;
                try
                {
                    if (obj != null)
                    {
                        worldBound = uiHelper.GetWorldBound(obj);
                    }
                    else
                    {
                        worldBound = new WorldBound();
                        worldBound.existed = false;
                    }
                }
                catch (System.Exception ex)
                {
                    Logger.w(ex.Message + " " + ex.StackTrace);
                    worldBound = new WorldBound();
                    worldBound.existed = false;
                }
                worldBound.id = instance;
                worldBounds.Add(worldBound);
            }

            command.sendObj = worldBounds;
            CommandDispatcher.SendCommand(command);
        }
        protected void handleGetElementByPos(Command command)
        {
            try
            {
                List<double> pos = JsonParser.Deserialization<List<double>>(command);
                float x = (float)pos[0];
                float y = (float)pos[1];
                Logger.d("handleGetElementByPos: " + x + " " + y);
                List<GameObject> selectedObjs = uiHelper.FindGameObjectsByPoint(new Point(x, y));
                if (selectedObjs == null || selectedObjs.Count == 0)
                {
                    command.status = ResponseStatus.GAMEOBJ_NOT_EXIST;
                    command.sendObj = "";
                    CommandDispatcher.SendCommand(command);
                    return;
                }
                ElementInfo element = new ElementInfo();
                GameObject obj = selectedObjs[0];
                string name = GameObjectTool.GenerateNamePath(obj);
                int instance = GameObjectManager.INSTANCE.AddGameObject(obj);
                element = new ElementInfo(name, instance);
                Logger.d("Element name = " + element.name + " ,instance =" + element.instance);              
                command.sendObj = element;
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                Logger.e("***************************" + ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;

            }
            CommandDispatcher.SendCommand(command);
        }

        protected void handleSetCamera(Command command)
        {
            Logger.d("handleSetCamera");
            
            try
            {
                List<String> camerName = JsonParser.Deserialization<List<String>>(command);
                if (camerName.Count > 0)
                {
                    String oldCamera = UGUIHelper.setCamera(camerName[0]);
                }
                else
                {
                    command.status = ResponseStatus.UN_KNOW_ERROR;
                    command.sendObj = "need camera name ";
                }
                
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                Logger.e("***************************" + ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;

            }
            CommandDispatcher.SendCommand(command);

        }

        protected void handleGetFPS(Command command)
        {
            Logger.d("handleGetFPS");
            try
            {
                command.sendObj=(uint)fps;
            }
            catch (System.Exception ex)
            {
                Logger.w(ex.Message + " " + ex.StackTrace);
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = ex.Message + " " + ex.StackTrace;
            }
            CommandDispatcher.SendCommand(command);

        }

        protected void handleGetStreamData(Command command)
        {
            Logger.d("handleGetStreamData");
            AppNetTrafficRes appNetTrafficRes = new AppNetTrafficRes();
            if (!netReadInvaild)
            {
                command.status = ResponseStatus.UN_KNOW_ERROR;
                command.sendObj = "";
            }
            else
            {
                try
                {
                    AppNetReq req = JsonParser.Deserialization<AppNetReq>(command);
                    int uid = req.uid;
                    Debug.Log("----------------" + uid + "----------------");
                    string recvPath = "/proc/uid_stat/" + uid + "/tcp_rcv";
                    string sendPath = "/proc/uid_stat/" + uid + "/tcp_snd";

                    int appRecv = 0;
                    int appSend = 0;
                    lock (netlocker)
                    {
                        int systemRecv = getNetData(recvPath);
                        int systemSend = getNetData(sendPath);
                        if (systemRecv == -1 || systemSend == -1)
                        {
                            //读取流量失败的，后面也一定会继续失败
                            netReadInvaild = false;
                        }
                        appRecv = systemRecv - recvByte;
                        appSend = systemSend - sendByte;
                    }

                    Logger.v("App(uid:" + uid + "） recv size:" + appRecv + " send size:" + appSend);

                    appNetTrafficRes.input = appRecv;
                    appNetTrafficRes.output = appSend;
                    command.sendObj = appNetTrafficRes;

                }
                catch (System.Exception ex)
                {
                    Logger.w(ex.Message + " " + ex.StackTrace);
                    command.status = ResponseStatus.UN_KNOW_ERROR;
                    command.sendObj = ex.Message + " " + ex.StackTrace;
                }
            }
            
            CommandDispatcher.SendCommand(command);
            
        }

        /// <summary>
        /// 计算fps的瞬时值。如果计算平均值，可能部分时段在执行WSDK中的内容，对FPS会有影响。
        /// </summary>
        public void ComputeFPS()
        {
            ++frames;
            float timeNow = Time.realtimeSinceStartup;
            if (timeNow > lastInterval + updateInterval)
            {
                double useTime = (timeNow - lastInterval - sdkUseTime);

                if (useTime == 0.0)
                {
                    fps = 0;
                }
                else
                {
                    fps = (float)(frames / useTime);
                }
                //Logger.v("fps:" + fps);
                sdkUseTime = 0;
                frames = 0;
                lastInterval = timeNow;
            }
        }

        private int getNetData(string path)
        {
            StreamReader theReader = null;
            int result = -1;
            try
            {
                string line = "";

                theReader = new StreamReader(path, Encoding.Default);
                using (theReader)
                {
                    line = theReader.ReadLine();
                    result = int.Parse(line);
                }
            }
            catch (Exception e)
            {
                Logger.d("read from" + path + " failed\n" + e.Message);
            }
            finally
            {
                if (theReader != null)
                {
                    theReader.Close();
                }

            }
            return result;
        }

        protected void handleEnterRecord(Command command)
        {
            Logger.d("handleEnterRecord");
            recordSocket = command.socket;
            CommandDispatcher.SendCommand(command);
            RecordMode = true;
        }

        protected void handleLeaveRecord(Command command)
        {
            Logger.d("handleLeaveRecord");
            RecordMode = false;
            CommandDispatcher.SendCommand(command);
            
        }

        


        protected void handleGetObjectField(Command command)
        {
            Logger.d("handleGetElementsBound" + command.recvObj);

            ComponentField componentField = JsonParser.Deserialization<ComponentField>(command);

            GameObject obj = GameObjectManager.INSTANCE.FindGameObjectGlobal(componentField.instance);

            if (obj == null)
            {
                command.status = ResponseStatus.GAMEOBJ_NOT_EXIST;
            }
            else
            {
                try
                {
                    object value = ReflectionTools.GetComponentAttribute(obj, componentField.comopentName, componentField.attributeName);
                    if (value != null)
                    {
                        command.sendObj = value.ToString();
                    }
                    

                }
                catch (System.Exception ex)
                {
                    command.status = ResponseStatus.REFLECTION_ERROR;
                    command.sendObj = ex.Message;
                }
            }

            CommandDispatcher.SendCommand(command);
        }

        protected void handleGetObjectMethods(Command command)
        {
            Logger.d("handleGetObjectMethods" + command.recvObj);
            try
            {
                ComponentMethod componentField = JsonParser.Deserialization<ComponentMethod>(command);

                GameObject obj = GameObjectManager.INSTANCE.FindGameObjectGlobal(componentField.instance);

                if (obj == null)
                {
                    command.status = ResponseStatus.GAMEOBJ_NOT_EXIST;
                }
                else
                {
                    MethodDetail[] methods = ReflectionTools.GetComponentMethods(obj, componentField.comopentName);
                    Logger.d("Methods Count: " + methods.Length);
                    command.sendObj = methods;
                }
            }
            catch (System.Exception ex)
            {
                command.status = ResponseStatus.REFLECTION_ERROR;
                command.sendObj = ex.Message;
            }

            CommandDispatcher.SendCommand(command);
        }

        protected void handleCallObjectMethod(Command command)
        {
            //Logger.d("handleCallObjectMethod" + command.recvObj);
            Logger.d("handleCallObjectMethod" + command.recvObj);
            try
            {
                ComponentMethodCall componentCall = JsonParser.Deserialization<ComponentMethodCall>(command);
                GameObject obj = GameObjectManager.INSTANCE.FindGameObjectGlobal(componentCall.instance);

                if (obj == null)
                {
                    command.status = ResponseStatus.GAMEOBJ_NOT_EXIST;
                }
                else
                {
                    object result = ReflectionTools.CallComponentMethod(obj, componentCall.comopentName, componentCall.methodName, componentCall.parameters);
                    Logger.d("Result is " + result.ToString());
                    command.sendObj = result.ToString();
                }
            }
            catch (System.Exception ex)
            {
                command.status = ResponseStatus.REFLECTION_ERROR;
                command.sendObj = ex.Message;
            }
            CommandDispatcher.SendCommand(command);
        }

    }
}
