# wt-wda

This project is based on [Facebook WebDriverAgent](https://github.com/facebook/WebDriverAgent )

Compared to the original wda , this version adds some interfaces for fast interaction and screen capturing required by GA Recorder

Some Private APIs are forbiddened in Xcode 10.2, two ways to solve this problem:
1. Using old versions of Xcode , and move the new DeviceSupport files to Xcode path.  Reference : https://github.com/iGhibli/iOS-DeviceSupport
2. Using new versions of Xcode(10.2+) , and replaced the framework files ( Path/to/Xcode/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/Frameworks/XCTest.framework) with old version.
--------------------------------------------------------------------------------------------------------------------------------------
# wt-wda


与facebook原版wda相比，增加了一些快速操作与截图接口,使用[GA Recorder](../GAutomatorIos/docs/GA%20Recorder.md)录制工具时需要使用该版本。
使用参考[Facebook WebDriverAgent](https://github.com/facebook/WebDriverAgent )

在Xcode10.2的默认安装包中，部分私有API已经被移除，有两种方法解决该问题 ：
1. 使用旧版Xcode，将新设备的DeviceSupport文件拷贝到Xcode安装目录即可，参考https://github.com/iGhibli/iOS-DeviceSupport
2. 使用新版Xcode，将其中的XCTest.frameworks替换成旧的 （Path/to/Xcode/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/Frameworks/XCTest.framework)


