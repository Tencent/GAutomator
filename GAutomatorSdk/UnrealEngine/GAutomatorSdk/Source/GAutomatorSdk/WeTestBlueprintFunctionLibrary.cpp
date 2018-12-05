// Fill out your copyright notice in the Description page of Project Settings.

#include "WeTestBlueprintFunctionLibrary.h"


void UWeTestBlueprintFunctionLibrary::Crash()
{
	UE_LOG(LogTemp, Log, TEXT("Crash get stack"));
	FString* s=nullptr;
	s->Find("1");
}

