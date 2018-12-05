# Functions
## init_device

Init a device instance specified by serialid（udid） to which the following operations will send.
### input
* type : Only DeviceType.DEVICE_IOS is supported for now.
* serial : UDID of IOS device.

### output
returns the device instance if succeed , otherwise returns None.

## launch_app

launch an app on device. If an launch failure occured, checking the log of wda is a quick way to see what happened.
### precondition
a device is inited (init_device is called) .
### input
* appid : the bundleid of app in iOS.
* timeout [60]: max wating seconds to launch app and connect to SDK . 

### output
returns ERR\_SUCCEED(0) if the app is launched and sdk is connected.otherwise returns the other err code indicating the failed reason.

## init\_engine\_sdk

connect to GA SDK.
### precondition
a device is inited (init_device is called) and the game integrated with GA SDK is on top.
### input
* enginetype [None]: the engine type of app integrated with GA SDK. Only EngineType.Unity is supported for now. If None is set , no sdk will be connected.
* local\_engine\_port ["53001"]: A PC port to forward to the SDK port of device. Please make sure it's a freeport.
* timeout [60]: max wating seconds to launch app and connect to SDK . 

### output
returns ERR\_SUCCEED(0) if the app is launched and sdk is connected.otherwise returns the other err_code indicating the failed reason.


## find\_element

find an element  specified by params
### precondition
* a device is inited (init_device is called) 
* if the method is  By.NAME\_IN\_ENGINE ,the GA SDK of app is inited(init\_engine\_sdk is called)
### input
* method : the locating method typed by By. By.NAME_IN_ENGINE   is supported for now.
* param : the locating params needed by method. if method is By.NAME\_IN\_ENGINE, the param is the element name in engine.
* timeout: waiting timeout(seconds)

### output
returns the element instance if succeed , otherwise returns None.

## touch\_element
touch  an element  specified by params
### precondition
* a device is inited (init_device is called) 
* if the method is  By.NAME\_IN\_ENGINE ,the GA SDK of app is inited(init\_engine\_sdk is called)
### input
* method : the locating method typed by By. By.NAME\_IN\_ENGINE   is supported for now.
* param : the locating params needed by method. if method is By.NAME_IN_ENGINE, the param is the element name in engine.

### output
returns the element instance if succeed , otherwise returns None.

## double\_touch\_element

double touch  an element  specified by params
### precondition
* a device is inited (init_device is called) 
* if the method is  By.NAME\_IN\_ENGINE ,the GA SDK of app is inited(init\_engine\_sdk is called)
### input
* method : the locating method typed by By. By.NAME\_IN\_ENGINE   is supported for now.
* param : the locating params needed by method. if method is By.NAME\_IN\_ENGINE, the param is the element name in engine.

### output
returns the element instance if succeed , otherwise returns None.

## long\_press\_element

logn press an element  specified by params
### precondition
* a device is inited (init_device is called) 
* if the method is  By.NAME\_IN\_ENGINE ,the GA SDK of app is inited(init\_engine\_sdk is called)
### input
* method : the locating method typed by By. By.NAME\_IN\_ENGINE   is supported for now.
* param : the locating params needed by method. if method is By.NAME\_IN\_ENGINE, the param is the element name in engine.

# Demo Using Functions
	import ga2
	
	udid="426b98156533915ae82a13d9c3e750018c3a932f"
	bundleId="com.tencent.wetest.demo"
	
	ga2.init_device(DeviceType.DEVICE_IOS, udid)
	ga2.launch_app(bundleId)
	ga2.init_engine_sdk(enginetype=EngineType.Unity)
	ga2.touch_element(ga2.By.NAME_IN_ENGINE,"/Canvas/Panel/FindElements")


# Class IOSDevice

## launch
the same as launch\_app function

## init\_engine\_sdk
the same as init\_engine\_sdk function

## kill
stop the running app.
### precondition
the target app is launched by launch_app
### input
* appid [None]: the bundleid to kill . In iOS, it's limited to the app launched by launch_app

## get\_top\_app
get the current top app.

### output
returns the bundleid of top app,otherwise returns None.


## home
press the home button on device

## screenshot
take a screenshot of device. Saved it to local path.
### input
localpath [None]: the path to save image.
### output
returns the image as opencv mat, otherwise returns None

## text
input text to device
### precondition
the device is in input state
### input
* content: the string to input 

## display_size
get the current resolution of device
### output
* (width,height): width and height resolution of device

## orientation
get the current orientation of device
### output
* DeviceOrientation value. One of {DeviceOrientation.PORTRAIT,DeviceOrientation.LANSCAPE,DeviceOrientation.PORTRAIT_UPSIDEDOWN,DeviceOrientation.LANDSCAPERIGHT}

## touch
touch at the target position on device
### input
* x: x coordinate. if 0<x<1, it will be regarded as rate of screen 
* y: y coordinate. if 0<y<1, it will be regarded as rate of screen

## long_\press
touch and hold at the target position on device
### input
* x: x coordinate. if 0<x<1, it will be regarded as rate of screen 
* y: y coordinate. if 0<y<1, it will be regarded as rate of screen
* duration[2]: holding seconds

## drag_pos
touch hold at a position and drag to another position on device
### input
* sx: x coordinate of source position. if 0<sx<1, it will be regarded as rate of screen 
* sy: y coordinate of source position. if 0<sy<1, it will be regarded as rate of screen
* dx: x coordinate of source position. if 0<dx<1, it will be regarded as rate of screen 
* dy: y coordinate of source position. if 0<dy<1, it will be regarded as rate of screen
* duration [1]: holding seconds( not moving seconds)

## wda_session
 used to interact with native controls.
### output
* a session instance of wda. see https://github.com/openatx/facebook-wda for details.

## engine_connector
 Used to interact with GA sdk in engine.
### precondition
GA SDK is inited(init\_engine\_sdk is called)
### output
* returns a instance of current connector to engine . If no sdk is connected, returns None. 

# Demo Using IOSDevice
	import ga2
	import cv2
	import random
	
	udid="426b98156533915ae82a13d9c3e750018c3a932f"
	bundleId="com.tencent.helloworld"
	
	device=ga2.init_device(DeviceType.DEVICE_IOS, udid)
	device.launch(bundleId)
	device.init_engine_sdk(enginetype=EngineType.Unity)
	(width,height)=device.display_size()
	device.touch_pos(width/2,height/2)
	scenename,elements = device.engine_connector().get_touchable_elements_bound()
    if elements:
    	elem=random.sample(elements,1)[0]
    	bound=elem[1]
    	device.touch_bound([bound.x,bound.y,bound.width,bound.height])
	image=device.screenshot()
	cv2.imshow("current device screen",image)
	cv2.waitKey()
	
