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

	bool GetCurrentLevelName(FString& LevelName);

	FString GetUWidgetLabelText(const UWidget* Widget);

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
}