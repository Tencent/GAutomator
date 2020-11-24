// Copyright 1998-2017 Epic Games, Inc. All Rights Reserved.

#include "GAutomator.h"
#include "CoreMinimal.h"
#include "Engine.h"
#include "Common/Log.h"
#include "Dispatcher/CommandDispatcher.h"

#define LOCTEXT_NAMESPACE "FGAutomatorModule"

void FGAutomatorModule::StartupModule()
{

	UE_LOG(GALog, Log, TEXT("FGAutomatorModule StartupModule"));
#if defined PLATFORM_IOS || defined __ANDROID__

	CommandDispatcherPtr = new WeTestU3DAutomation::FCommandDispatcher();

	CommandDispatcherPtr->Initialize();

	if (GEngine != nullptr) 
	{
		GEngine->AddOnScreenDebugMessage(-1, 3.0f, FColor::Red, TEXT("WeTest GAutomator"));
	}
	else
	{
		UE_LOG(GALog, Error, TEXT("WeTest GAutomator Start"));
	}
	

#endif
}

void FGAutomatorModule::ShutdownModule()
{

}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FGAutomatorModule, GAutomator)
