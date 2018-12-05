// Fill out your copyright notice in the Description page of Project Settings.

#include "FindElementsGameMode.h"
#include "Button.h"
#include "Image.h"

void AFindElementsGameMode::ChangeMenuWidget(UButton* button, UImage* image, UTexture2D* texture) {
	UE_LOG(LogTemp, Log, TEXT("Button name %s"), *button->GetName());

	image->SetBrushFromTexture(texture);
	image->SetVisibility(ESlateVisibility::Visible);
}


