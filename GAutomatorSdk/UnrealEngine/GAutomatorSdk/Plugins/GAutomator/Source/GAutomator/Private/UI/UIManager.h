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
		//��ʱ��������
		FTimerHandle* handle;

		//��ʱί�к���
		FTimerDelegate timerDel;


		//ʱ�����
		float tickTime;

		//ѭ������
		bool loop;

		//���ö�ʱ��
		virtual bool SetTimerHandle() = 0;

		//��ʱ���߼�
		virtual void TimerHandleFunc() = 0;


	};

	//���߼��
	class TimeTemp :public TimeEve
	{


		~TimeTemp() {};


	public:
		TimeTemp(FCommand& coo):command(coo) {};

		FCommand& command;

		bool SetTimerHandle() override;

		void TimerHandleFunc() override;

		//���߼�����
		float scales;

	};


}