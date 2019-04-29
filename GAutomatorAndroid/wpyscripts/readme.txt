v 1.1.1 版本更新日志：
====================
-----------------------------------
device=manager.get_device():
*新增接口get_element_world_bound，能够获取到节点的世界坐标。该方法只支持wetest sdk 8版本及其以上
*新增接口get_registered_handlers，获取可用的自定义函数。该方法只支持wetest sdk 8版本及其以上
*新增接口call_registered_handler，调用在游戏中注册的自定义函数，并返回对应的值。该方法只支持wetest sdk 8版本及其以上
~修复:NGUI部分版本,调用Input会出错的

main.py:
*添加游戏包名后，运行main.py能够直接拉起游戏，并进行全逻辑的测试

trave.py
*增加自动化探索测试接口，即便不写代码也可以直接遍历游戏


v 1.2.1 版本更新日志
====================
-----------------------------------
engine=manager.get_engine():
*新增接口get_touchable_elements_bound，能够获取可点击节点及节点左上角坐标，节点长宽高
*新增接口get_element_text,获取GameObject文字信息，NGUI控件则获取UILable、UIInput、GUIText组件上的文字信息，UGUI控件则获取Text、GUIText组件上的问题信息
*新增接口get_element_image,获取GameObject图片名称,NGUI控件则获取UITexture、UISprite、SpriteRenderer组件上的图片名称,UGUI控件则获取Image、RawImage、SpriteRenderer组件上的图片名称

-----------------------------------
device=manager.get_device():
*get_display_size,云端获取失败后，直接通过uiautomator获取。本地直接通过Uiautomator获取
*get_rotation，云端从平台获取失败后，直接通过UIAutomator获取。本地直接通过UIAutomator获取
*get_top_package_activity,云端从平台获取失败后，直接通过UIAutomator获取。本地UIAutomator获取失败后，通过adb shell dumpsys获取
*back，本地方式修改为UIAutomator

-----------------------------------
登陆实现进行了修改
-----------------------------------
将uiautomator独立出来，以备后用
-----------------------------------
main.py修改，修改native的游戏拉起时机。先拉起游戏，再进行socket的初始化


v 2.0.0版本
====================
V2版本将不再兼容老版本的SDK，新的SDK也不能兼容老的脚本GAutomator框架。

V2版本主要对GAutomator的框架进行了改进，通信协议全部改为json，对python的版本也没有windows 32的要求。新架构将支持与SDK的重连，与标准控件的操作也更加稳定。
SDK的性能更加高效，自动化测试基本对FPS的影响基本可以忽略，CPU的影响一般在1%的左右。
-----------------------------------
engine=manager.get_engine():
*新增get_component_field,能够反射获取游戏中对象的属性值

v 2.1.0版本
====================
V2.1.0版本主要对框架的结构进行了调整

-----------------------------------
1、支持一台pc同时控制多台手机
2、将于对外接口无关的wpyscripts.wetest.tools移到wpyscripts.common.utils.py，wpyscripts.platform_helper.py移到wpyscripts.common.platform_helper.py
3、将logger_config.py移除，日志初始化放置到wpyscripts.__init__.py
4、get_touchable_elements_bound、get_touchable_element处理默认的compnent为可点击候选之外，可以增加自定义的UI可点击控件组件。如，lua脚本编写的内容
5、根据component组件名称获取gameobject

------------------------------------
GAutomatorView
1、修复android 5.0以上图片倒转，不能使用的bug
2、修复调整窗口大小时，红色框留在原地，位置发生偏移的bug
3、新增gameobject树搜索的功能，支持正则表达式搜索
4、复制路径功能进行调整。2.0.0版本复制时会复制全路径，2.1.0版本会对gameobject进行判断，如果名称唯一只复制名称，如果名称不唯一则复制全路径
5、修复出现富文本，带有<时不支持的bug


v 2.2.0版本
====================

-----------------------------------
1、默认摄像机选择。一个物体可能会被多个摄像机渲染，允许设置一个最恰当的摄像机
2、修复QQ和微信在三星部分手机上无法登陆的BUG
3、移除runTest.sh与endTest.sh，如果需要拉起则交由end.py与prepare.py
4、修改了在Linux和Mac本地不能运行的bug
5、修改get_element_bound，不可见的内容返回ElementBound，visible属性置为false;主要针对3D物体，转化为屏幕坐标时，摄像机范围之外的置为visible=false
6、增加urllib3库，避免用户安装。增加urllib3库之后，能够真正做到，python环境0配置，一份脚本可以移植到任意地方。
7、增加linux的测试，本地在linux下可运行

v 2.3.0 版本
====================

------------------------------------
1、增加获取组件上方法和执行对应方法的接口。
2、修复若干bug。


v 2.3.1　版本
====================

------------------------------------
1、修复SDK在部分unity版本上，获取应用长宽高不准的bug

V 2.4.0 版本
=====================
1、修复脚本的若干bug
2、report接口增加report_error接口，用户用能测试的断言。在本地运行会在运行目录下生成_wetest_testcase_result.txt的统计信息


V 2.5.0 版本
=====================
1、非激活的gameobject，返回get_element_bound返回的visible为false
2、修复部分boxcolidr，返回长宽有误的bug
3、新增第三方C#脚本调用，可动态获取与调用游戏内接口


V 2.6.0 版本
=====================
GAutomato SDK发布版本为1.4.1版本
1、新增本地弹出框点击，android手机的权限框。可调动device中的start_handle_popbox开启，stop_handle_popbox关闭
2、新增C#脚本调用python端注册的函数，engine中的register_game_callback可注册python端委托。SDK最新版本1.4.0以上版本，可通过WeTest.U3DAutomation.ClientCaller的相关接口与python端进行互动
3、修复微信6.50版本以上无法登陆的问题

V 2.7.0 版本
=====================
1、新增UE4引擎接口
2、集成minitouch，可通过device接口实现多点触控
3、适配复微信QQ新版本登陆

V 2.8.0 版本
=====================
支持py3

V 2.8.1 版本
=====================
支持qq 8.0.0登录
sdk支持刘海屏

