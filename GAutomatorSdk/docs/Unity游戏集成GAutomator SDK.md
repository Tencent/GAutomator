GAutomator SDK Unity是专门给予Unity游戏引擎开发的组件感知、组件操作和崩溃异常捕获组件，能够感知和查询引擎的组件信息，比提供对应的操作。Unity SDK支持Android/IOS平台。GAutomator SDK Unity分为NGUI和UGUI版本，请根据自己的游戏[下载对应的版本](../UnitySDK/compiled)。SDK文件包括（iOS只需要U3DAutomation.dll）

```
- u3dautomation.jar
- U3DAutomation.dll
```

**注：对外发布版本不可接入SDK！！！**

**step 1:导入Unity项目工程**

1. U3DAutomation.dll中包含一个WeTest.U3DAutomation.U3DAutomationBehaviour组件，放在Assets目录下的任意位置均可
2. 如果是针对android平台, u3dautomation.jar需要被打包进游戏, 放在Assets\Plugins\Android或Builds\Plugin\Android目录下

`
如果使用python来进行编译。可以使用脚本来拷贝上述三个文件。编译完成后，从workspace目录中删除，这样可以避免发布版本带入WeTest SDK。
`

**step 2:初始化WeTest SDK**

选择第一个场景（Scene）,创建一个空的GameObject，然后挂载WeTest.U3DAutomation.U3DAutomationBehaviour组件

```C#
public class WeTestManager : MonoBehaviour {
	
    Application.LogCallback logCall;
	void Start () {
#if WETEST_SDK
        this.gameObject.AddComponent<WeTest.U3DAutomation.U3DAutomationBehaviour>();
        //this.gameObject.AddComponent<BuglyInitScript>();
        //BuglyAgent.RegisterLogCallback(WeTest.U3DAutomation.CrashMonitor._OnLogCallbackHandler);
#endif
        
    }
}
```
	
可以通过宏定义，来控制是否接入WeTest SDK。smcs.rsp和gmcs.rsp，两个文件控制预编译内容
![](image/smcp.png)

```python
def ModifyMacro(workSpacePath, appName, mode):
    fsmcs = open(workSpacePath + /Assets/smcs.rsp", 'w')
    fgmcs = open(workSpacePath + /Assets/gmcs.rsp", 'w')

    if mode == "debug":
        fsmcs.write("-define:WETEST_SDK")
        fgmcs.write("-define:WETEST_SDK")

```

**step 3:检查是否接入成功**
apk包编译好之后，拉起游戏，同时通过logcat查看日志
`adb logcat -vthreadtime -s Unity`
如果看到U3DAutomation Init OK代表，已经接入成功。
![](image/log_info.png)

