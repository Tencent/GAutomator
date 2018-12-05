// Fill out your copyright notice in the Description page of Project Settings.

#include "TestActorComponent.h"
#include "InputCoreTypes.h"
#ifdef __ANDROID__
#include "Android/AndroidWindow.h"
#endif

// Sets default values for this component's properties
UTestActorComponent::UTestActorComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


// Called when the game starts
void UTestActorComponent::BeginPlay()
{
	Super::BeginPlay();
#ifdef __ANDROID__
	FPlatformRect Rect=FAndroidWindow::GetScreenRect();
	UE_LOG(LogTemp, Log, TEXT("Top = %d,Left = %d,Right = %d,Bottom = %d"), Rect.Top, Rect.Left, Rect.Right, Rect.Bottom);

	void* NativeWindow= FAndroidWindow::GetHardwareWindow();
	int32_t Width, Height;
	FAndroidWindow::CalculateSurfaceSize(NativeWindow,Width, Height);

	UE_LOG(LogTemp, Log, TEXT("Surfaceview Width=%d ,Height=%d"), Width,Height);
#endif
	
}


// Called every frame
void UTestActorComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	APlayerController* PlayerController = Cast<APlayerController>(GetWorld()->GetFirstPlayerController()->GetPawn()->GetController());

	float X, Y;
	bool Pressed;

	PlayerController->GetInputTouchState(ETouchIndex::Touch1, X, Y, Pressed);

	UE_LOG(LogTemp, Log, TEXT("Touch x = %f ,y=%f"), X, Y);
}

