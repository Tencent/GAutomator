GAutomator SDK基本协议格式如下：

![avatar](protocol.png)

Head: 32bit的int类型，表示body的length。
Body：json字符串。PC客户端（脚本）向手机端服务发送命令格式为
{“cmd”: number, ”value”: “what you want}
手机端服务向PC的回包格式为
{“cmd”:number, “status”: code,”data”: “result value”}
status为0表示正确。Status为其他数字，data中的内容表示错误原因。

具体的，游戏端至少需要实现如下几个TCP服务（端口27019)

**getSdkVersion:**

功能：获取当前SDK版本信息(cmd:100)

请求json：

	{
		"cmd": 100, 
		"value": ""
	}
回包json：
	
	{
	    "cmd": 300, 
	    "status": 0, 
	    "data": {
	        "engine": "Cocos2D", 
	        "sdkVersion": "1.5.0", 
	        "sdkUIType": "cocos", 
	        "engineVersion": "5.1.2f1"
	    }
	}
	
**dumpTree**

功能：dump当前界面的Node树结构，以xml形式返回

请求json：

	{
	    "cmd": 100, 
	    "value": ""
	}
	
回包json：

	{
	    "cmd": 300, 
	    "status": 0, 
	    "data": "<AbstractRoot engine='cocos'><GameObject name='WetestSDK'/></AbstractRoot>"
	}
	
Xml的具体格式：

	<AbstractRoot engine="cocos">
	  <GameObject name="WetestSDK"/>
	</AbstractRoot>
	
根节点约定为AbstractRoot。其他Node节点，xml节点名称为GameObject(为了兼容Unity)，name字段为Node的名称。

**findElements**
功能：根据name查找当前界面是否存在该Node（可同时查找多个）。
请求json：

	{
	    "cmd": 101, 
	    "value": [ "Sample",  "m_Btn" ]
	}
回包json：
{
    "cmd": 101, 
    "status": 0, 
    "data": [
	    {
	    "instance": -1,  "name": "Sample"
	    }, 
	    {
	    "instance": 12312312,  "name": "m_Btn"
	    }
    ]
}
instance（整型）：若Node存在可以用地址来表示。若不存在，则可以用-1来表示。

**getElementBounds**

功能：获取Node的屏幕坐标及长宽

请求json(value的每一项为instance）：
	
	{
	    "cmd": 103, 
	    "value": [
	        12312312, 
	        12312313
	    ]
	}
回包json:
	
	{
	    "cmd": 103, 
	    "status": 0, 
	    "data": [
	        {
	           "existed": true, 
			    "width": 0, 
			    "visible": false, 
			    "height": 0, 
			    "path": "Sample", 
			    "y": 0, 
			    "x": 0
		   }, 
		    {
			    "existed": true, 
			    "width": 0.2, 
			    "visible": true, 
			    "height": 0.1, 
			    "path": "m_btn", 
			    "y": 0.75, 
			    "x": 0.25
		    }
	    ]
	}
**getElementByPos**

功能：根据屏幕坐标，找到该位置下对应的Node节点。
请求json:
	
	{
	    "cmd": 301, 
	    "value": [
	        0.1, 
	        0.5
	    ]
	}
	
其中value为数组，value[0]表示x坐标，value[1]表示y坐标。x,y为屏幕坐标系，左上角为(0,0)坐标，返回为0~1的值。
回包json：

a.若能够找到对应元素：
	
	{
	    "cmd": 301, 
	    "status": 0,  
	    "data": {"name":"m_btn","instance":123123}
	}
	
b.若不能找到对应元素
	
	{
	    "cmd": 301, 
	    "status": 4,
	    "data": ""
	}
 
