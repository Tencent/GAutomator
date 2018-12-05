// Copyright 1998-2017 Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "ModuleManager.h"
#include "Dispatcher/CommandDispatcher.h"

class FGAutomatorModule : public IModuleInterface
{
public:
	FGAutomatorModule() :CommandDispatcherPtr(nullptr) {};
	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

private:
	WeTestU3DAutomation::FCommandDispatcher* CommandDispatcherPtr;

};