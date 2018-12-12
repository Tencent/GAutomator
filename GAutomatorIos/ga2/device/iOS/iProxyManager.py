import os
import subprocess
import logging
from ga2.common.cmdExecuter import CmdExecuter

logger=logging.getLogger(__name__)

class IProxyManager(object):

    def __init__(self,udid):
        self.udid=udid
        self.forward_list={}

    def forward(self,localport,remoteport):
        localport=str(localport)
        remoteport=str(remoteport)
        cmd="iproxy "+localport+" "+remoteport
        if self.udid:
            cmd+=" "+self.udid
        CmdExecuter.executeWithoutWait(cmd)
        self.forward_list[localport]=remoteport

    def removeForward(self,localport):
        localport=str(localport)
        cmd = "iproxy " + localport+" "
        CmdExecuter.executeAndWait("pkill -f \""+cmd+"\"")
        if localport in self.forward_list.keys():
            self.forward_list.pop(localport)

    def removeAllForwards(self):
        for key,value in self.forward_list.items():
            localport = str(key)
            cmd = "iproxy " + localport + " "
            CmdExecuter.executeAndWait("pkill -f \"" + cmd + "\"")
        self.forward_list.clear()



    # @staticmethod
    # def _init_wdaServer():
    #     udid = os.environ.get("IOS_SERIAL")
    #     if udid is None:
    #         process=subprocess.Popen("idevice"
    #     mXcodeCmd =
    #         "xcodebuild -project %s/WebDriverAgent.xcodeproj test -scheme WebDriverAgentRunner -destination 'platform=iOS,id=%s'",
    #         wdaDriverPath, udid);

