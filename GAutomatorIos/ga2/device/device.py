
import abc, six


from enum import Enum

class DeviceOrientation(Enum):
    PORTRAIT = 0,
    LANSCAPE = 1,
    PORTRAIT_UPSIDEDOWN=2,
    LANDSCAPERIGHT=3

class DeviceType(Enum):
    DEVICE_ANDROID=0,
    DEVICE_IOS=1

@six.add_metaclass(abc.ABCMeta)
class Device():
    defaultDevice=None

    @staticmethod
    def getDefaultDevice():
        return Device.defaultDevice

    def setDefault(self):
        Device.defaultDevice=self

    @abc.abstractmethod
    def device_type(self):
        pass

    # @abc.abstractmethod
    # def install(self,appfile):
    #     pass
    #
    # @abc.abstractmethod
    # def uninstall(self,app):
    #     pass


    def engine_connector(self):
        pass

    @abc.abstractmethod
    def init_engine_sdk(self,enginetype=None,local_engine_port="53001",timeout=60):
        pass



    # @abc.abstractmethod
    # def connect_to_engine_sdk(self,enginetype,local_engine_port="53001",timeout=60):
    #     pass

    @abc.abstractmethod
    def get_top_app(self):
        pass

    @abc.abstractmethod
    def launch(self, appid, timeout=60, alert_handler = None):
        pass

    @abc.abstractmethod
    def kill(self,app):
        pass

    @abc.abstractmethod
    def screenshot(self,localpath=None):
        pass

    @abc.abstractmethod
    def display_size(self):
        pass

    @abc.abstractmethod
    def orientation(self):
        pass

    # @abc.abstractmethod
    # def forward(self, local_port,remote_port):
    #     pass
    #
    # @abc.abstractmethod
    # def remove_forward(self, local_port):
    #     pass

    @abc.abstractmethod
    def home(self):
        pass

    @abc.abstractmethod
    def text(self,content):
        pass

    # @abc.abstractmethod
    # def find_element(self,elem,wait_time,sleep_time=1):
    #     pass
    #
    # @abc.abstractmethod
    # def touch_element(self,elem,wait_time,sleep_time=1):
    #     pass
    #
    # @abc.abstractmethod
    # def touch_hold_element(self,elem,wait_time,sleep_time=1):
    #     pass

    @abc.abstractmethod
    def touch(self,x,y):
        pass

    @abc.abstractmethod
    def double_touch(self,x,y):
        pass


    @abc.abstractmethod
    def long_press(self,x,y,duration=2):
        pass


    @abc.abstractmethod
    def drag(self,sx,sy,dx,dy,duration=1):
        pass



    # @abc.abstractmethod
    # def touch_down_android(self,name,x,y):
    #     pass
    #
    # @abc.abstractmethod
    # def touch_move_android(self,name,x,y):
    #     pass
    #
    # @abc.abstractmethod
    # def touch_up_android(self,name):
    #     pass

