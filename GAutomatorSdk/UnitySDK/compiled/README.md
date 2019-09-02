# GA2 SDK for Unity

基于Unity引擎的游戏的GAutomator SDK包分为NGUI与UGUI版本。
用户可按照如下步骤在为Unity游戏集成GAutomator SDK.

## 步骤1：导入Unity项目工程
a. U3DAutomation.dll中包含一个WeTest.U3DAutomation.U3DAutomationBehaviour组件，放在Assets目录下的任意位置均可。

b. 如果是针对android平台，u3dautomation.jar需要被打包进游戏, 放在Assets\Plugins\Android或Builds\Plugin\Android目录下

## 步骤2：初始化WeTest SDK
选择第一个Scene,创建一个空的GameObject，然后挂载WeTest.U3DAutomation.U3DAutomationBehaviour组件。

	public class WeTestManager : MonoBehaviour {
		Application.LogCallback logCall;
		void Start () {
			\#if WETEST_SDK
			this.gameObject.AddComponent<WeTest.U3DAutomation.U3DAutomationBehaviour>();
			\#endif
		}
	}
备注：可以通过全局宏定义控制是否集成GAutomator SDK( 由smcs.rsp和gmcs.rsp两个文件控制预编译内容)，如：

	def ModifyMacro(workSpacePath, appName, mode):
	fsmcs = open(workSpacePath + /Assets/smcs.rsp", 'w')
	fgmcs = open(workSpacePath + /Assets/gmcs.rsp", 'w')
	if mode == "debug":
	fsmcs.write("-define:WETEST_SDK")
	fgmcs.write("-define:WETEST_SDK")
## 步骤3：检查是否集成成功
编译出apk包之后，启动游戏，同时通过`idevicesyslog |grep "U3DAutomation"`
查看日志。如果看到U3DAutomation Init OK，则表示SDK已经集成成功。
