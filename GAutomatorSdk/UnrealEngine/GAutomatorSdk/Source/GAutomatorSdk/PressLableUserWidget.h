// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "TextBlock.h"
#include "PressLableUserWidget.generated.h"

/**
 * 
 */
UCLASS()
class GAUTOMATORSDK_API UPressLableUserWidget : public UUserWidget
{
	GENERATED_BODY()
	
public:
	virtual void NativeTick(const FGeometry& MyGeometry, float DeltaTime) override;
	float CountTime;

protected:
	virtual void NativeConstruct() override;

private:
	UTextBlock* Label;
	
};
