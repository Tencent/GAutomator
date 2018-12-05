// Fill out your copyright notice in the Description page of Project Settings.

#include "BollonUserWidget.h"
#include "UserWidget.h"
#include "Button.h"




void UBollonUserWidget::NativeTick(const FGeometry& MyGeometry, float DeltaTime) {


	CountTime -= DeltaTime;

	if (CountTime <= 0.0) {
		UE_LOG(LogTemp, Log, TEXT("Destory ,remove from parent"));
		this->RemoveFromParent();
		this->RemoveFromViewport();
	}
	else {
		FLinearColor color = this->ColorAndOpacity;
		color.A = CountTime / MaxCountTime;
		this->SetColorAndOpacity(color);
	}
}

void  UBollonUserWidget::NativeConstruct() {
	if (UImage* img = Cast<UImage>(GetWidgetFromName(FName(TEXT("BollonTexture")))))
	{
		bollonImage = img;
		
	}
	MaxCountTime = 3.0;
	CountTime = MaxCountTime;
}