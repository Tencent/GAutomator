#pragma once

#include "CoreMinimal.h"
#include "VersionInfo.h"
#include "Runtime/Launch/Resources/Version.h"

namespace WeTestU3DAutomation
{
	namespace Cmd
	{
		static const ::int32 EXIT = 0;//退出游戏
									////////////////////////
		static const ::int32 GET_VERSION = 100;//获取版本号
		static const ::int32 FIND_ELEMENTS = 101;//查找节点
		static const ::int32 FIND_ELEMENT_PATH = 102;//模糊查找
		static const ::int32 GET_ELEMENTS_BOUND = 103;//获取节点的位置信息
		static const ::int32 GET_ELEMENT_WORLD_BOUND = 104;//获取节点的世界坐标
		static const ::int32 GET_UI_INTERACT_STATUS = 105;//获取游戏的可点击信息，包括scene、可点击节点，及位置信息
		static const ::int32 GET_CURRENT_SCENE = 106;//获取Unity的Scene名称
		static const ::int32 GET_ELEMENT_TEXT = 107;//获取节点的文字内容
		static const ::int32 GET_ELEMENT_IMAGE = 108;//获取节点的图片名称
		static const ::int32 GET_REGISTERED_HANDLERS = 109;//获取注册的函数的名称
		static const ::int32 CALL_REGISTER_HANDLER = 110;//调用注册的函数
		static const ::int32 SET_INPUT_TEXT = 111;//input控件更换文字信息
		static const ::int32 GET_OBJECT_FIELD = 112;//反射获取对象属性值
		static const ::int32 FIND_ELEMENTS_COMPONENT = 113;//获取所有包含改组件的gameobject
		static const ::int32 SET_CAMERA_NAME = 114;//设置渲染的最佳的Camera
		static const ::int32 GET_COMPONENT_METHODS = 115;//反射获取组件上的方法
		static const ::int32 CALL_COMPONENT_MOTHOD = 116;//通过反射调用组件的函数
		static const ::int32 LOAD_TEST_LIB = 117;//拉起test相关的库

		static const ::int32 PRC_SET_METHOD = 118;//注册python端的方法
		static const ::int32 RPC_METHOD = 119;//游戏内的接口可调用，python端的方法

		///////////////////////////////////////////////
		static const ::int32 HANDLE_TOUCH_EVENTS = 200;//发送down;move;up

		//////////////////////////////////////////////
		static const ::int32 DUMP_TREE = 300;//获取节点树xml
		static const ::int32 FIND_ELEMENT_BY_POS = 301;//根据位置信息获取节点内容

		//////////////////////////////////////////////
		static const ::int32 GET_FPS = 400;//获取FPS
		static const ::int32 GET_TRAFFIC_DATA = 401;//获取流量

		//////////////////////////////////////////////
		static const ::int32 ENTER_RECORD = 500;//开始录制
		static const ::int32 LEAVE_RECORD = 501;//结束录制
		static const ::int32 TOUCH_NOTIFY = 502;//返回点击的节点
	};

	enum class ResponseStatus :int32 {
		SUCCESS = 0,
		NO_SUCH_CMD = 1,//发送的命令不可识别
		UNPACK_ERROR = 2,//发生的body数据，json反序列化失败
		UN_KNOW_ERROR = 3,//一般是在执行任务的过程中抛出异常，未预料的问题
		GAMEOBJ_NOT_EXIST = 4,//gameobject 不存在
		COMPONENT_NOT_EXIST = 5,//component 不存在
		NO_SUCH_HANDLER = 6,//没有该自定义的handler

		REFLECTION_ERROR = 7,//反射获取某个对象时出错
		NO_SUCH_RESOURCE = 8,//没有所需的资源内容
	};

	enum class ResponseDataType :uint8 
	{
		STRING=0,
		OBJECT=1
	};

	struct FCommand {
		int32 cmd;
		ResponseStatus status;
		FString ResponseJson;
		ResponseDataType ReponseJsonType;


		FCommand(){
			cmd = 0;
			status = ResponseStatus::SUCCESS;
			ReponseJsonType = ResponseDataType::STRING;
		};

		FString ToJson();
	};

	struct FVersionData
	{
		FString sdkVersion;//SDK版本号如1.0.1,主版本.子版本.修正版本
		FString engine;
		FString engineVersion;
		FString sdkUIType;//UGUI,NGUI

		FVersionData()
		{
			sdkVersion = SDK_VERSION;
			engine = ENGINE;
			sdkUIType = SDK_UI;
			engineVersion = FString::Printf(TEXT("%d.%d.%d"), ENGINE_MAJOR_VERSION, ENGINE_MINOR_VERSION, ENGINE_PATCH_VERSION);
		}

		FString ToJson();
	};

	struct FDumpTree
	{
		FString scene;
		FString xml;

		FString ToJson();
	};

	struct FElementInfo
	{
		int64 instance;
		FString name;

		FString ToJson();
	};

	struct FBoundInfo
	{
		int64 instance;
		bool visible;
		bool existed;
		float width;
		float height;
		float x;
		float y;
		FString path;

		FBoundInfo():existed(true), visible(true),path(""),width(0.0f),height(0.0f),x(0.0f),y(0.0f)
		{
		};

		FString ToJson();
	};
}