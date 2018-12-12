using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace WeTest.U3DAutomation
{
    class TouchActions
    {
        public Command cmd;
        public TouchEvent[] events;

    }
    class TouchEventHandler
    {
        private static TouchEventHandler instance = new TouchEventHandler();

        private BlockQueue<TouchActions> actionsQueue = new BlockQueue<TouchActions>();
        private Queue<TouchEvent> eventQueue = new Queue<TouchEvent>();
        private Thread thrd;
        

        private bool run=false;

        private TouchEventHandler()
        {

        }

        public static TouchEventHandler INSTANCE
        {
            get{return instance;}
            
        }

        public void Start()
        {
            try
            {
                if (null != thrd)
                {
                    return;
                }
                run = true;
                thrd = new Thread(PushTouchAction);
                thrd.IsBackground = true;
                thrd.Start();
            }
            catch (System.Exception ex)
            {
                Logger.d(ex.Message);
            }
        }

        public void Stop()
        {
            run = false;
        }

        private void PushTouchAction()
        {
            while (run)
            {
                try
                {
                    TouchActions actions = actionsQueue.Dequeue();

                    if (actions.events != null)
                    {
                        for (int i = 0; i < actions.events.Length; ++i)
                        {
                            TouchEvent touchEvent = actions.events[i];
                            AddEvent(touchEvent);
                            if (touchEvent.sleeptime > 0)
                            {
                                Thread.Sleep(touchEvent.sleeptime);
                            }
                        }
                    }

                    if (actions.cmd != null)
                    {
                        CommandDispatcher.SendCommand(actions.cmd);
                    }
                }
                catch (System.Exception ex)
                {
                    Logger.w(ex.Message + "\n" + ex.StackTrace);
                }
                
            }
        }

        /// <summary>
        /// 主线程获取touch 时间然后注入到View中
        /// </summary>
        /// <returns></returns>
        public List<TouchEvent> GetTouchEvents()
        {
            lock (eventQueue)
            {
                if (eventQueue.Count == 0)
                {
                    return null;
                }
                else
                {

                    List<TouchEvent> events = new List<TouchEvent>();
                    while (eventQueue.Count > 0)
                    {
                        events.Add(eventQueue.Dequeue());
                    }
                    return events;
                }
            }
        }

        /// <summary>
        /// 获取命令后，交由时间处理线程来处理
        /// </summary>
        /// <param name="touchActions"></param>
        public void AddTouchActions(TouchActions touchActions)
        {
            actionsQueue.Enqueue(touchActions);
        }

        private void AddEvent(TouchEvent touchEvent)
        {
            lock (eventQueue)
            {
                eventQueue.Enqueue(touchEvent);
            }
        }

    }
}
