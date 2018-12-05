// Fill out your copyright notice in the Description page of Project Settings.

#include "PressLableUserWidget.h"
#include "TextBlock.h"


void  UPressLableUserWidget::NativeConstruct() {
	UE_LOG(LogTemp,Log,TEXT("Create UPressLableUserWidget"));
	if (UTextBlock* text = Cast<UTextBlock>(GetWidgetFromName(FName(TEXT("Label")))))
	{
		Label = text;
	}
	CountTime = 0;
}

void UPressLableUserWidget::NativeTick(const FGeometry& MyGeometry, float DeltaTime) {


	CountTime += DeltaTime;

	if (Label != nullptr)
	{
		FString Content = FString::Printf(TEXT("Exp +%f"), CountTime);
		UE_LOG(LogTemp, Log, TEXT("Exp Label %s"), *Content);
		Label->SetText(FText::FromString(Content));
	}
}