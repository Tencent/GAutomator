# -*- coding: UTF-8 -*-

import struct
import traceback

import atexit
from wpyscripts.common.adb_process import *
from wpyscripts.common.coordinate_transfer import *
from wpyscripts.common.utils import retry_if_fail
import logging
import threading
import six
if six.PY2:
    from Queue import Queue
elif six.PY3:
    from queue import Queue
import socket
logger = logging.getLogger("wetest")

SNAP_SHOT_MODE = '\001'
MAX_TRIES = 3
FORWARD_PORT = 40000
PHONE_PORT = 25666
PUSH_MINITOUCH = "push {0} /data/local/tmp/minitouch"
CHMOD_MINITOUCH = "shell chmod 777 /data/local/tmp/minitouch"
LAUNCH_MINITOUCH = "shell /data/local/tmp/minitouch"
DEL_SCREENCAPTURE = "rm /data/local/tmp/minitouch"
FORWARD = "forward tcp:{0} localabstract:minitouch".format(FORWARD_PORT)
REMOVE_FORWARD = "forward --remove tcp:{0}".format(FORWARD_PORT)



class Minitouch(object):

    @retry_if_fail()
    def reinit(self): #reforward and relaunch minitouch connector
        self.sub_process = excute_adb_process_daemon(LAUNCH_MINITOUCH, shell=True, needStdout=False)
        excute_adb_process(FORWARD)
        atexit.register(self.cleanup)
        try:
            #   self.socketClient = SocketClient(self.screen_address, FORWARD_PORT)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.connect((self.screen_address, FORWARD_PORT))
            t = self.socket.recv(30)
            logger.info(t)
            m = re.search('\\^ (\\d+) (\\d+) (\\d+) (\\d+)', str(t), re.S)
            (maxContacts, maxX, maxY, maxPressure) = map(int, m.groups())
            self._MinitouchStream__screenWidth = maxX
            self._MinitouchStream__screenHeight = maxY
        except :
            self.socket.close()
            #  self.socketClient.close()
            self.sub_process.kill()
            excute_adb_process(REMOVE_FORWARD)
            return None

        #            self.image_uploader = ImageUpload(self.testid, self.deviceid)
        threadSend = threading.Thread(target=self.MinitouchSend)
        threadSend.setDaemon(True)
        threadSend.start()
        return True

    def MinitouchSend(self):
        cmd = None
        try:
            while True:
                cmd = self.touch_cmd_queue.get()
                if not cmd:
                    continue
                elif cmd[-1] != '\n':
                    cmd += '\n'
                if six.PY2:
                    self.socket.send(cmd)
                else:
                    self.socket.send(bytes(cmd, 'UTF-8'))
        except :
            if cmd:#restore cmd queue
                new_queue = Queue()
                new_queue.put(cmd)
                while(not self.touch_cmd_queue.empty()) :
                    new_queue.put(self.touch_cmd_queue.get_nowait())
                self.touch_cmd_queue = new_queue
            self.reinit()

    def __init__(self):
        #port = os.environ.get("IMAGE_ENCODER_PORT")
        self.touch_cmd_queue = Queue()
      #  self.screen_address = os.environ.get("PLATFORM_IP", "127.0.0.1")
        self.screen_address="127.0.0.1"
        abi=self._get_abi()
        file_path = os.path.split(os.path.realpath(__file__))[0]
        minitouch_path = os.path.abspath(os.path.join(file_path,"minitouch_lib","libs",abi,"minitouch"))
        excute_adb_process(PUSH_MINITOUCH.format(minitouch_path))
        excute_adb_process(CHMOD_MINITOUCH)
        self.reinit()

    def cleanup(self):
        logger.info("kill minitouch...")
        kill_process_by_name("minitouch")
        self.socket.close()
        excute_adb_process(REMOVE_FORWARD)

    @retry_if_fail()
    def _get_abi(self):
        file = excute_adb("shell getprop ro.product.cpu.abi")
        abi = file.read().strip()
        file.close()
        logger.info("_get_abi: {0}".format(abi))
        return abi

    @retry_if_fail()
    def _get_version(self):
        file = excute_adb("shell getprop ro.build.version.sdk")
        version = file.read()
        file.close()
        version = version.replace("\r\n", "")
        version = version.replace("\n", "")
        logger.info("get_version: {0}".format(version))
        if version not in ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "N"]:
            logger.warning("not supported version")
            return ""
        return version

    def reset(self):
        cmds = 'r\nc\n'
        self.touch_cmd_queue.put(cmds)

    def click(self, x, y, contact=0):
        cmds = 'd {0} {1} {2} 50\nc\nu {0}\nc\n'.format(contact, int(x), int(y))
        self.touch_cmd_queue.put(cmds)

    def touchDown(self, x, y, contact=0):
        cmds = 'd {0} {1} {2} 50\nc\n'.format(contact, int(x), int(y))
        self.touch_cmd_queue.put(cmds)
     #   print(cmds)
        self.mx = x
        self.my = y

    def touchUp(self, contact=0):
        cmds = 'u {0}\nc\n'.format(contact)
      #  print(cmds)
        self.touch_cmd_queue.put(cmds)

    def touchMove(self, x, y, contact=0):
        if self.mx != -1 and self.my != -1:
            dx = x - self.mx
            dy = y - self.my
            tmpx = self.mx + dx / 2
            tmpy = self.my + dy / 2
            cmds = 'm {0} {1} {2} 50\nc\nm {0} {3} {4} 50\nc\n'.format(contact, int(tmpx), int(tmpy), int(x), int(y))
        else:
            cmds = 'm {0} {1} {2} 50\nc\n'.format(contact, int(x), int(y))
       # print(cmds)
        self.touch_cmd_queue.put(cmds)
        self.mx = x
        self.my = y

    def downMoveUp(self, x, y, tx, ty, contact=0):
        cmds = 'd {0} {1} {2} 50\nc\nm {0} {3} {4} 50\nc\nu {0}\nc\n'.format(contact, int(x), int(y), int(tx), int(ty))
        self.touch_cmd_queue.put(cmds)

    def wait(self, waitMS):
        cmds = 'w {0}\nc\n'.format(waitMS)
        self.touch_cmd_queue.put(cmds)

    def getScreenResolution(self):
        return (self._MinitouchStream__screenWidth, self._MinitouchStream__screenHeight)

    def stop(self):
        if  self.sub_process:
            self.sub_process.kill()
            excute_adb_process(REMOVE_FORWARD)

def get_minitouch(width=360, height=640):
    if get_minitouch.instance:
        return get_minitouch.instance
    get_minitouch.instance = Minitouch()
    return get_minitouch.instance


get_minitouch.instance = None

if __name__ == "__main__":
    minitoucher = get_minitouch()
    time.sleep(5)
    pt=transfer_display_coordinate_to_image((293,520),(1920,1080),1,minitoucher.getScreenResolution())
    print(pt)
    # minitoucher.click(pt[0],pt[1])

    start_pt=transfer_display_coordinate_to_image((274,768),(1920,1080),1,minitoucher.getScreenResolution())
    end_pt=transfer_display_coordinate_to_image((365,765),(1920,1080),1,minitoucher.getScreenResolution())
    start_pt2 = transfer_display_coordinate_to_image((1673,768), (1920, 1080), 1, minitoucher.getScreenResolution())
    end_pt2 = transfer_display_coordinate_to_image((1537,765), (1920, 1080), 1, minitoucher.getScreenResolution())
    print(start_pt,end_pt)
    minitoucher.touchDown(start_pt[0],start_pt[1],0)
    minitoucher.touchDown(start_pt2[0],start_pt2[1],1)
    minitoucher.touchMove(end_pt[0],end_pt[1],0)
    minitoucher.touchMove(end_pt2[0], end_pt2[1], 1)
    minitoucher.wait(1000)
    minitoucher.touchUp(0)
    minitoucher.wait(2000)
    minitoucher.touchUp(1)

    #minitoucher.DownMoveUp(263,321,259,407)
    # for i in range(0,30):
    #     time.sleep(10)
    #     minitoucher.click(pt)
        # minitoucher.touchDown(263, 407)
        # minitoucher.touchMove(800, 407)
        # minitoucher.wait(1000)
        # minitoucher.touchUp()

    minitoucher.stop()
