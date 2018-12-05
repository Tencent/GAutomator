GAutomator SDK是Unreal 4中的一个项目插件。GAutomator插件目前仅支持Android平台（PIE环境部分功能可用），项目中集成插件之后，可自动启动SDK。SDK支持获取游戏组件、获取位置信息等。
GAutomator UE版本的SDK以源码的形式发布，目前仅支持Android平台，默认运行在Runtime编译状态下，发型版本也会带上。

**注：发布版本关闭GAutomator 插件**
工程目录下,<ProjectName>.uproject，只需要把Plugins对应GAutomator设置为不启动即可

```json
"Plugins": [
		{
			"Name": "GAutomator",
			"Enabled": false
		}
	],
```

**GAutomator集成步骤：**
**step 1:**
将Unreal GAutomator的插件目录拷贝至项目的Plugins目录下。如果游戏项目目录中没有"Plugins"目录，创建"Plugins"目录。插件可拷贝至"Plugins"目录下的任何子目录下。
<img src="image/PluginSdk/plugin_dir.jpg"/>

**step 2:**
**重新生成** c++ 项目文件。插件模块和代码应该在项目文件中被体现出来。
<img src="image/PluginSdk/re_generate_sln.png"/>

**step 3:**
正常的** 编译游戏项目**。Unreal Build Tool 会检测到插件的存在，并将它们作为游戏的依赖项进行编译。

**step 4:**
**启动编辑器**（或者游戏）。插件一开始是处于禁用的状态，但可以在编辑器界面中启用它。

**step 5:**
打开插件编辑器（Window->Plugins），找到该插件并选中勾选框。
<img src="image/PluginSdk/enable_plugin.png"/>

**step 6:**
**重启编辑器。**插件就会自动在启动时被加载。正常编译，即会集成SDK


**集成成功**
集成GAutomator插件后，启动的时候会在左上角显示<span style="color:red">WeTest GAutomator</span>.
<img src="image/PluginSdk/started.png"/>

GAutomator插件启动成功之后，会在手机上开启27019端口，可通过以下命令查看
```shell
adb shell netstat -an|findstr 27019
```
