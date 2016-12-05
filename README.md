# GAutomator
[![Wetest](https://img.shields.io/badge/wetest-2.2.0-brightgreen.svg)](wetest.qq.com)  [![license](https://img.shields.io/badge/license-mit-red.svg)](https://github.com/Tencent/tinker/blob/master/LICENSE)

GAutomator是一个针对Unity手游的UI自动化测试框架。设计理念与使用方式,类似于Android的UIAutomator。GAutomator以Unity中的GameObject为操作对象，通过操作GameObject实现UI自动化测试。基于GameObject的方式，不存在手机分辨率适配的问题，一份脚本能够运行在不同手机之上，基于GameObject的另外一个优点为鲁棒性较强，游戏的UI界面经常发生变化，GameObject变化频率相对较低。

<img src="https://github.com/Tencent/GAutomator/blob/master/doc/image/1.gif" alt="SGame" width="400px" />  <img src="https://github.com/Tencent/GAutomator/blob/master/doc/image/2.gif" alt="Drawing" width="400px" />

## 一 运行环境要求
window平台下运行，linux可运行脚本（GAutomator）。

- python 2.7版本
- 环境变量中包含有adb

工程中已包含所有的库，打开即可编写测试用例，写完即可运行（考虑到国内公司网络限制较多，python库的安装非常麻烦）。

## 测试用例编写

GAutomator被测试的游戏需要集成**SDK**，[WeTest SDK及打包方式](http://wetest.qq.com/cloud/index.php/phone/blrooike "SDK")。GAutomator中在Sample目录下自带了一个集成有WeTest SDK的demo游戏，可以使用该游戏进行自动化的练习。[GAutomator使用说明文档](https://github.com/Tencent/GAutomator/blob/master/doc/GAutomator%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.md "Document")，在doc下面也有详细的接入文档与使用说明文档。GAutomator与UIAutomator类似，提供了一个UI控件信息查看器[GAutomatorView](http://cdn.wetest.qq.com/com/c/GAutomatorView.zip),可以查看UI对于的GameObject及相关信息，[GAutomatorView使用说明文档](https://github.com/Tencent/GAutomator/blob/master/doc/GAutomatorView%E6%B8%B8%E6%88%8F%E6%8E%A7%E4%BB%B6%E6%9F%A5%E7%9C%8B%E5%99%A8.md "GAutomatorView")。
<img src="https://github.com/Tencent/GAutomator/blob/master/doc/image/behaviour.png" alt="Drawing" width="800px" />


强烈建议使用[pycharm](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC,"pycharm")编写python代码
```python

import wpyscripts.manager as manager
from testcase.tools import *

def test():
    engine=manager.get_engine()
    logger=manager.get_logger()

    version=engine.get_sdk_version()
    logger.debug("Version Information : {0}".format(version))

    scene=engine.get_scene()
    logger.debug("Scene :   {0}".format(scene))

    sample_button=engine.find_element("/Canvas/Panel/Sample")
    logger.debug("Button : {0}".format(sample_button))
	#engine.click(sample_button)
    screen_shot_click(sample_button)

test()

```
- step 1:代码保存为sample.py，位置与main.py同级目录，这样能够查找到GAutomator的相关库；
- step 2:拉起游戏，然后运行上面的代码；
- step 3:点击sample，跳出一个气球

## GAutomator结构
### GAutomator框架原理
GAutomator目前仅支持Unity。GAutomator是非跨进程的，所以需要在游戏中集成SDK。集成SDK之后会在游戏中启动一个socket服务，GAutomator Python端通过adb与wetest sdk建立端口映射。GAutomator通过socket向WeTest SDK发送请求，包括查询GameObject、获取UI的位置信息、执行点击操作等。手游自动化测试过程中，还需要操作Android标准控件，如QQ登录等。GAutomator使用[xiaocong uiautomator](https://github.com/xiaocong/uiautomator)作为pc端调用uiautomator的解决方案。
<img src="https://github.com/Tencent/GAutomator/blob/master/doc/image/atricle.jpg" alt="Drawing" width="600px" />

### GAutomator工程结构
严格意义上来说，GAutomator并不算一个库，算是一个工程。GAutomator并没有采用setup.py安装的方式。主要在公司网络环境下，安装Python库可能并不是一件容易的事情。我们想提供一种方式，编写完拷贝到任何一台安装有python环境的电脑上都能运行，免去打包和安装库的烦恼。
<img src="https://github.com/Tencent/GAutomator/blob/master/doc/image/GAutomator.png" alt="Drawing" width="800px" />









