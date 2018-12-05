// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "WeTestBlueprintFunctionLibrary.generated.h"

/**
 * 
 */
UCLASS()
class GAUTOMATORSDK_API UWeTestBlueprintFunctionLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, Category = "WeTest")
	static void Crash();
	
	
	
};
