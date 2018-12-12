import subprocess
from ga2.common.logger_config import *
from ga2.common.cmdExecuter import CmdExecuter

class IMobileDevice():

    def __init__(self,udid):
        self.udid=udid

    def install(self,ipapath):
        cmd="ideviceinstaller -i "+ipapath
        if self.udid!=None:
            cmd=" -u " + self.udid
        CmdExecuter.executeAndWait(cmd)

    def uninstall(self,bundleid):
        cmd = "ideviceinstaller -U " + bundleid
        if self.udid != None:
            cmd = " -u " + self.udid
        CmdExecuter.executeAndWait(cmd)








