# GAutomator
[![Wetest](https://img.shields.io/badge/wetest-green.svg)](wetest.qq.com) 

GAutomator(Game Automator) is an open source test automation framework for mobile games. Designed just like android uiautomator, GAutomator also includes ui automator functions. GAutomator interacts  with engine elements such as GameObject(GameObjects are the fundamental objects in Unity that represent characters, props and scenery) . GameObject-based approach will not suffer from device resolution adaptation problems so that a single testing script is able to be executed on various devices.

<img src="GAutomatorAndroid/doc/image/1.gif" alt="SGame" width="400px" /><img src="GAutomatorAndroid/doc/image/2.gif" alt="Drawing" width="400px" />

## Usage
1. integrate your game with GAutomator SDK as [docs](GAutomatorSdk/docs)
2. write your iOS or Android testing scripts（ see [GAutomatorAndroid](GAutomatorAndroid) and [GAutomatorIos](GAutomatorIos) for details）


## GAutomatorAndroid
python test project for games on Android(with Unity/UE4 UI interaction)

## GAutomatorIos
python scripts library for games on iOS(with Unity UI interaction)

## GAutomatorSDK
SDK source code . In order to interact with Game Engine Elements, the SDK is required to be integrated to game.

## wt-wda
A project based on [WebDriverAgent](https://github.com/facebook/WebDriverAgent) used for iOS testing.


## Contact
For more information about contributing issues or pull requests, [Issues](https://github.com/Tencent/GAutomator/issues)，your can also contact（QQ:800024531）

--------------------------------------------------------------------------------------------------------------------------------------

# GAutomator
[![Wetest](https://img.shields.io/badge/wetest-green.svg)](wetest.qq.com) 

GAutomator是一个针对手游的UI自动化测试框架。设计理念与使用方式,类似于Android的UIAutomator。GAutomator以引擎中的元素为操作对象（如Unity中的GameObject），通过操作GameObject实现UI自动化测试。基于GameObject的方式，不存在手机分辨率适配的问题，一份脚本能够运行在不同手机之上。基于GameObject的另外一个优点为鲁棒性较强，游戏的UI界面经常发生变化，GameObject变化频率相对较低。

<img src="GAutomatorAndroid/doc/image/1.gif" alt="SGame" width="400px" />  <img src="GAutomatorAndroid/doc/image/2.gif" alt="Drawing" width="400px" />

## 基本使用步骤
1. 集成GAutomator SDK到游戏中，参照[docs](GAutomatorSdk/docs)
2. 编写Android或者iOS的python自动化脚本实现游戏交互（参照[GAutomatorAndroid](GAutomatorAndroid)以及[GAutomatorIOS](GAutomatorIos)中的说明）

## GAutomatorAndroid
针对android游戏的Python测试工程。（目前支持Unity与UE4引擎的交互）

## GAutomatorIos
针对iOS游戏的Python库。（目前支持Unity引擎交互）

## GAutomatorSDK
GAutomator SDK的源码。为了实现测试脚本或工具与游戏引擎的交互，需要将GAutomator SDK集成到游戏包中。

## wt-wda
一个基于[WebDriverAgent](https://github.com/facebook/WebDriverAgent)的工程，用于iOS自动化测试。


## 联系
bug,需求或使用过程中的疑问均可直接发布在[Issues](https://github.com/Tencent/GAutomator/issues)，有专人负责回答。也可直接联系wetest助手（800024531）
