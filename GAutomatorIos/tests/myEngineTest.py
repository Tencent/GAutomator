
import ga2
from ga2.device.device import Device
from ga2_contrib.sample_engine_extention.myEngine import *



udid = "8b281ff151d795bfc81212e45068dea12b91b706"
if __name__ == "__main__":
    device = ga2.init_device(ga2.DeviceType.DEVICE_IOS, udid)  # get the instance of device
    ga2.launch_app("com.tencent.wetest.demo.ngui")  # if you are going to test a specific scene, just comment out this line.
    ga2.init_engine_sdk(enginetype=ga2.EngineType.MY_ENGINE, local_engine_port="42222")
    ga2.touch_element(ga2.By.NAME_IN_ENGINE,"/Canvas/Panel/FindElements")


