// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Image.h"
#include "BollonUserWidget.generated.h"

/**
 *
 */
UCLASS()
class GAUTOMATORSDK_API UBollonUserWidget : public UUserWidget
{
	GENERATED_BODY()


public:
	virtual void NativeTick(const FGeometry& MyGeometry, float DeltaTime) override;
	float CountTime;
	float MaxCountTime;

protected:
	virtual void NativeConstruct() override;

private:
	UImage* bollonImage;


};
