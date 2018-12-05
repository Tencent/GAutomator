// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameMode.h"
#include "Button.h"
#include "Image.h"
#include "FindElementsGameMode.generated.h"

/**
 * 
 */
UCLASS()
class GAUTOMATORSDK_API AFindElementsGameMode : public AGameMode
{
	GENERATED_BODY()
	
public:

	UFUNCTION(BlueprintCallable, Category = "FindElements")
	void ChangeMenuWidget(UButton* button, UImage* image, UTexture2D* texture);
	
	
};
