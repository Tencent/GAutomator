#pragma once

#include "CoreMinimal.h"
#include "Components/Widget.h"
#include "Protocol/ProtocolCommon.h"

namespace WeTestU3DAutomation
{
	/*
	* Get Current level visible UMG WidgetTree
	*/
	FString GetCurrentWidgetTree();

	const UWidget* FindUWidgetObject(const FString& name);

	const bool ChangeRotator(const FString& str);

	const float getScale();

	const FRotator getRotation();

	const FVector getLevelBound(const FString& str);

	const bool setLocation(const FString& str);

	bool GetCurrentLevelName(FString& LevelName);

	const bool setCharacter(float& posx, float& posy);

	const FString callRegisterHandler(FName& funcname, FString& funcparams);

	FString GetUWidgetLabelText(const UWidget* Widget);



	//bool GetCurrentCharacter(AActor* Character);

	class FUWidgetHelper
	{
	public:
		FUWidgetHelper() :Inited(false){ ; };
		bool Initialize();

		bool GetElementBound(const FString& name, FBoundInfo& BoundInfo);

		const UWidget* FindUWidgetObjectByPos(float x, float y);
		//获取移动设备屏幕信息
		FVector GetMobileinfo();

	
	private:
		bool Inited;
		static int32 SurfaceViewWidth;
		static int32 SurfaceViewHeight;
		static float WidthScale;
		static float HeightScale;
		static float ViewportScale;
		bool CheckGEngine();
		bool PositionInRect(const FGeometry& geometry,float x,float y);



		/*Use DPI not alway right,only not android or AndroidWindow can't use*/
		bool InitViewPortScale();
		bool InitScaleByAndroid();
		

	};

	class TimeEve
	{


	public:

		TimeEve() {};
		virtual ~TimeEve() {};
		//计时器句柄
		FTimerHandle* handle;

		//委托函数
		FTimerDelegate timerDel;


		//计时间隔
		float tickTime;

		//是否循环
		bool loop;

		//设置计时器
		virtual bool SetTimerHandle() = 0;

		//主体逻辑
		virtual void TimerHandleFunc() = 0;


	};

	//计时器设置样例
	class TimeTemp :public TimeEve
	{


		~TimeTemp() {};


	public:
		TimeTemp(FCommand& coo):command(coo) {};

		FCommand& command;

		bool SetTimerHandle() override;

		void TimerHandleFunc() override;

		//射线检测距离
		float scales;

	};


}