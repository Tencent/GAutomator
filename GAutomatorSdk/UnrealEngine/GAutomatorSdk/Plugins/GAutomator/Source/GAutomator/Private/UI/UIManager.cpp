#include "UIManager.h"
#include "Layout/Children.h"
#include "EngineUtils.h"
#include "Components/Widget.h"
#include "Blueprint/UserWidget.h"
#include "Blueprint/WidgetTree.h"
#include "Engine/UserInterfaceSettings.h"
#include "Engine.h"
#include "Common/Log.h"
#include "XmlParser.h"
#include "Common/GXmlJsonTools.h"
#include "Engine/UserInterfaceSettings.h"
#include "TextBlock.h"
#include "RichTextBlock.h"
#include "MultiLineEditableTextBox.h"
#include "Handler/CommandHandler.h"
#include "MultiLineEditableText.h"
#include <ctime> 
#ifdef __ANDROID__
#include "Android/AndroidWindow.h"
#endif

namespace WeTestU3DAutomation
{

	FXmlNode* TransformUmg2XmlElement(UWidget* Widget, FXmlNode* Parent) {

		FXmlNode* WidgetXmlNode = AddFXmlNode(Parent, "UWidget", FString());

		TArray<FXmlAttribute>& Attributes = const_cast<TArray<FXmlAttribute>&>(WidgetXmlNode->GetAttributes());
		UClass* WidgetClass = Widget->GetClass();

		Attributes.Add(FXmlAttribute("name", Widget->GetName()));
		Attributes.Add(FXmlAttribute("components", WidgetClass->GetName()));
		Attributes.Add(FXmlAttribute("id", FString("0")));

		const UTextBlock* TextBlock = Cast<UTextBlock>(Widget);

		if (TextBlock != nullptr)
		{
			Attributes.Add(FXmlAttribute("txt", TextBlock->GetText().ToString()));
		}

		return WidgetXmlNode;
	}

	void ForWidgetAndChildren(UWidget* Widget, FXmlNode* Parent)
	{

		if (Widget == nullptr || Parent == nullptr || !Widget->IsVisible()) {
			return;
		}
		FXmlNode* WidgetXmlNode = TransformUmg2XmlElement(Widget, Parent);
		// Search for any named slot with content that we need to dive into.
		if (INamedSlotInterface* NamedSlotHost = Cast<INamedSlotInterface>(Widget))
		{
			TArray<FName> SlotNames;
			NamedSlotHost->GetSlotNames(SlotNames);

			for (FName SlotName : SlotNames)
			{
				if (UWidget* SlotContent = NamedSlotHost->GetContentForSlot(SlotName))
				{

					ForWidgetAndChildren(SlotContent, WidgetXmlNode);
				}
			}
		}

		// Search standard children.
		if (UPanelWidget* PanelParent = Cast<UPanelWidget>(Widget))
		{
			for (int32 ChildIndex = 0; ChildIndex < PanelParent->GetChildrenCount(); ChildIndex++)
			{
				if (UWidget* ChildWidget = PanelParent->GetChildAt(ChildIndex))
				{
					ForWidgetAndChildren(ChildWidget, WidgetXmlNode);
				}
			}
		}
	}

	FString GetCurrentWidgetTree() {
		TSharedPtr<FXmlFile> xml = CreateFXmlFile();
		FString XmlStr;
		FXmlNode* RootNode = xml->GetRootNode();

		for (TObjectIterator<UUserWidget> Itr; Itr; ++Itr)
		{
			UUserWidget* UserWidget = *Itr;

			if (UserWidget == nullptr || !UserWidget->GetIsVisible() || UserWidget->WidgetTree == nullptr) {
				UE_LOG(GALog, Log, TEXT("UUserWidget Iterator get a null(unvisible) UUserWidget"));
				continue;
			}

			ForWidgetAndChildren(UserWidget->WidgetTree->RootWidget, RootNode);
		}

		WriteNodeHierarchy(*RootNode, FString(), XmlStr);

		return MoveTemp(XmlStr);
	}


	const UWidget* FindUWidgetObject(const FString& name)
	{
		for (TObjectIterator<UUserWidget> Itr; Itr; ++Itr)
		{
			UUserWidget* UserWidget = *Itr;

			if (UserWidget == nullptr || !UserWidget->GetIsVisible() || UserWidget->WidgetTree == nullptr) {
				UE_LOG(GALog, Log, TEXT("UUserWidget Iterator get a null(unvisible) UUserWidget"));
				continue;
			}

			UWidget* Widget = UserWidget->GetWidgetFromName(FName(*name));
			if (Widget != nullptr) {
				return Widget;
			}
		}

		return nullptr;
	}


	void GetElementBound(const FString& name, FBoundInfo& BoundInfo)
	{
		const UWidget* Widget = FindUWidgetObject(name);
	}

	bool GetCurrentLevelName(FString& LevelName)
	{
		for (TObjectIterator<UUserWidget> Itr; Itr; ++Itr)
		{
			UUserWidget* UserWidget = *Itr;

			if (UserWidget == nullptr || !UserWidget->GetIsVisible() || UserWidget->WidgetTree == nullptr) {
				continue;
			}


			UWorld* World = Itr->GetWorld();

			if (World != nullptr)
			{
				LevelName = World->GetMapName();
				return true;
			}
		}

		return false;
	}



	FString GetUWidgetLabelText(const UWidget* Widget)
	{
		if (Widget == nullptr)
		{
			return FString();
		}
		const UMultiLineEditableText* MultiLineEditableText = Cast<UMultiLineEditableText>(Widget);

		if (MultiLineEditableText != nullptr)
		{
			return MultiLineEditableText->GetText().ToString();
		}

		const UTextBlock* TextBlock = Cast<UTextBlock>(Widget);
		if (TextBlock != nullptr)
		{
			return TextBlock->GetText().ToString();
		}

		const UMultiLineEditableTextBox* MultiLineEditableTextBox = Cast<UMultiLineEditableTextBox>(Widget);
		if (MultiLineEditableTextBox != nullptr)
		{
			return MultiLineEditableTextBox->GetText().ToString();
		}

		return FString();
	}

	int32 FUWidgetHelper::SurfaceViewWidth = 0;
	int32 FUWidgetHelper::SurfaceViewHeight = 0;
	float FUWidgetHelper::WidthScale = -1.0f;
	float FUWidgetHelper::HeightScale = -1.0f;
	float FUWidgetHelper::ViewportScale = -1.0f;

	bool FUWidgetHelper::Initialize()
	{
		if (!CheckGEngine())
		{
			UE_LOG(GALog, Error, TEXT("FUWidgetHelper Initialize failed"));
			Inited = false;
			return false;
		}

#ifdef  __ANDROID__
		bool AndroidInitResult = InitScaleByAndroid();
		if (!AndroidInitResult)
		{
			InitViewPortScale();
		}
#else
		//Not Anroid,use general,DPI method.
		InitViewPortScale();
#endif
		Inited = true;
		return true;

	}

	bool FUWidgetHelper::InitViewPortScale()
	{
		if (!CheckGEngine())
		{
			UE_LOG(GALog, Error, TEXT("FUWidgetHelper Initialize failed"));
			Inited = false;
			return false;
		}
		const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());

		const UUserInterfaceSettings* setting = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass());
		if (setting != nullptr) {
			ViewportScale = setting->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));

			if (ViewportScale <= 0.0) {
				UE_LOG(GALog, Error, TEXT("ViewportScale = %f,invaild"), ViewportScale);
				Inited = false;
				return false;
			}
			WidthScale = ViewportScale;
			HeightScale = ViewportScale;
			SurfaceViewWidth = GSystemResolution.ResX / ViewportScale;
			SurfaceViewHeight = GSystemResolution.ResY / ViewportScale;
			UE_LOG(GALog, Log, TEXT("Screen(GSystemResolution) with scale %f, size width= %f,height=%f"), ViewportScale, GSystemResolution.ResX / ViewportScale, GSystemResolution.ResY / ViewportScale);
		}
		return true;
	}

	bool FUWidgetHelper::InitScaleByAndroid()
	{
#ifdef  __ANDROID__
		if (!CheckGEngine())
		{
			UE_LOG(GALog, Error, TEXT("FUWidgetHelper Initialize failed"));
			Inited = false;
			return false;
		}
		const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());

		if (SurfaceViewWidth != 0.0f&&SurfaceViewHeight != 0.0f) {
			return true;
		}
		void* NativeWindow = FAndroidWindow::GetHardwareWindow();

		FAndroidWindow::CalculateSurfaceSize(NativeWindow, SurfaceViewWidth, SurfaceViewHeight);
		if (SurfaceViewWidth == 0.0f)
		{
			UE_LOG(GALog, Error, TEXT("SurfaceWidth error = 0.0 "));
			SurfaceViewWidth = ViewportSize.X;
		}
		if (SurfaceViewHeight == 0.0f)
		{
			UE_LOG(GALog, Error, TEXT("SurfaceViewHeight error = 0.0 "));
			SurfaceViewHeight = ViewportSize.Y;
		}
		WidthScale = ViewportSize.X / SurfaceViewWidth;
		HeightScale = ViewportSize.Y / SurfaceViewHeight;
		UE_LOG(LogTemp, Log, TEXT("Surfaceview WidthScale=%f ,HeightScale=%f,SurfaceViewWidth = %d,SurfaceViewHeight=%d"), WidthScale, HeightScale, SurfaceViewWidth, SurfaceViewHeight);
		return true;
#else
		return false;
#endif
	}

	bool FUWidgetHelper::CheckGEngine()
	{
		if (GEngine == nullptr || GEngine->GameViewport == nullptr || GEngine->GameViewport->Viewport == nullptr)
		{
			UE_LOG(GALog, Error, TEXT("Global GEngine(GameViewPort) is null"));
			return false;
		}
		return true;
	}

	bool FUWidgetHelper::GetElementBound(const FString& name, FBoundInfo& BoundInfo)
	{
		if (!Inited&&Initialize())
		{
			UE_LOG(GALog, Error, TEXT("Mobile Screen size get error"));
			BoundInfo.existed = false;
			BoundInfo.instance = -1;
			BoundInfo.visible = false;
			return false;
		}

		const UWidget* WidgetPtr = FindUWidgetObject(name);

		if (WidgetPtr == nullptr || !WidgetPtr->IsVisible()) {
			UE_LOG(GALog, Log, TEXT("UObject %s can't find"), *name);
			BoundInfo.existed = false;
			BoundInfo.instance = -1;
			BoundInfo.visible = false;
			return true;
		}

		const FGeometry geometry = WidgetPtr->GetCachedGeometry();

		FVector2D Position = geometry.GetAbsolutePosition();
		FVector2D Size = geometry.GetAbsoluteSize();

		BoundInfo.x = Position.X / WidthScale;
		BoundInfo.y = Position.Y / HeightScale;
		BoundInfo.width = Size.X / WidthScale;
		BoundInfo.height = Size.Y / HeightScale;
		return true;
	}

	bool FUWidgetHelper::PositionInRect(const FGeometry& geometry, float x, float y)
	{
		FVector2D Position = geometry.GetAbsolutePosition();
		FVector2D Size = geometry.GetAbsoluteSize();

		if (x >= Position.X&&y >= Position.Y&&x <= (Position.X + Size.X) && y <= (Position.Y + Size.Y))
		{
			return true;
		}
		return false;
	}

	const UWidget* FUWidgetHelper::FindUWidgetObjectByPos(float x, float y)
	{
		if (!Inited&&Initialize())
		{
			UE_LOG(GALog, Error, TEXT("Mobile Screen size get error"));
			return nullptr;
		}
		float GeometryX = x*WidthScale;
		float GeometryY = y*HeightScale;
		UWidget* ContainPosWidget = nullptr;

		for (TObjectIterator<UUserWidget> Itr; Itr; ++Itr)
		{
			UUserWidget* UserWidget = *Itr;

			if (UserWidget == nullptr || !UserWidget->GetIsVisible() || UserWidget->WidgetTree == nullptr) {
				UE_LOG(GALog, Log, TEXT("UUserWidget Iterator get a null(unvisible) UUserWidget"));
				continue;
			}

			UserWidget->WidgetTree->ForEachWidgetAndDescendants([&ContainPosWidget, this, GeometryX, GeometryY](UWidget* WidgetPtr) {
				if (WidgetPtr == nullptr || !WidgetPtr->IsVisible()) {
					return;
				}
				const FGeometry geometry = WidgetPtr->GetCachedGeometry();

				if (this->PositionInRect(geometry, GeometryX, GeometryY))
				{
					ContainPosWidget = WidgetPtr;
				}

			});
		}

		return ContainPosWidget;
	}


	//设置定时器进行碰撞检测
	bool TimeEvent::SetTimerCheck(FCommand& command,const FString& str,const FString& frontDistance,const FString& sideDistance)
	{
		UInputSettings * Settings = const_cast <UInputSettings *>(GetDefault < UInputSettings >());
		TArray<FInputAxisKeyMapping> AxisMap;
		Settings->GetAxisMappingByName(FName("Turn"), AxisMap);
		if (str == "0")
		{
			for (int i = 0; i < AxisMap.Num(); i++)
			{
				if (AxisMap[i].Key == "A" || AxisMap[i].Key == "D" || AxisMap[i].Key == "Gamepad_LeftX")
				{
					Settings->RemoveAxisMapping(AxisMap[i]);
					scales.Add(AxisMap[i].Scale);
					AxisMap[i].Scale = 0.0f;
					Settings->AddAxisMapping(AxisMap[i]);
				}
			}
		}
		Settings->SaveKeyMappings();

		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* UserWidget = *Itr;

			if (UserWidget == nullptr) {
				continue;
			}

			world = Itr->GetWorld();

			character = world->GetFirstPlayerController()->GetCharacter();

			//character->EnableInput(NULL);

			if (world)
			{
				/*FCheckHit checkHit(World);
				if (checkHit.Initialize())
				{
					return true;
				}*/
				FTimerDelegate del;
				FString out = str;
				int32 out2 = FCString::Atoi(*frontDistance);
				int32 out3 = FCString::Atoi(*sideDistance);
				del.BindLambda([this,&command,out,out2,out3]() {TraceLine(command,out,out2,out3); });
				world->GetTimerManager().SetTimer(*checkHit, del, 0.2f, str == "0" ? true : false);
				return true;
			}
		}
		return false;
		
	}

	static TArray<FCharacterPos> characterposs;

	//开启射线检测
	void TimeEvent::TraceLine(FCommand& command, FString str,int32 frontDistance,int32 sideDistance)
	{
		UWorld* worldTemp = nullptr;
		APlayerController* characterControll = nullptr;
		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* UserWidget = *Itr;

			if (UserWidget == nullptr) {
				continue;
			}

			worldTemp = Itr->GetWorld();

			character = Itr->GetWorld()->GetFirstPlayerController()->GetCharacter();

			characterControll = Itr->GetWorld()->GetFirstPlayerController();

			break;
		}
		FHitResult Hit,Hit2;
		UE_LOG(GALog, Log,TEXT("Timer Start"));
		FVector vectorStart = character->GetActorLocation();
		vectorStart.Z = 0.0f;
		FVector actorRotator = character->GetActorForwardVector();
		FVector actorRotator2 = actorRotator;
		float tempaxis = actorRotator2.X;
		actorRotator2.X = actorRotator2.Y;
		actorRotator2.Y = tempaxis;
		if (actorRotator2.X > 0)
		{
			actorRotator2.Y *= -1;
		}
		else
		{
			actorRotator2.X *= -1;
		}
		//修改正向射线检测距离，单位cm
		FVector vectorEnd = vectorStart + actorRotator * frontDistance;
		//修改侧向射线检测距离，单位cm
		FVector vectorEnd2 = vectorStart + actorRotator2 * sideDistance;
		vectorEnd.Z = character->GetDefaultHalfHeight() * 2;
		vectorEnd2.Z = character->GetDefaultHalfHeight() * 2;
		DrawDebugLine(worldTemp, vectorStart + FVector(0.0f, 0.0f, 25.0f), vectorEnd, FColor(255, 0, 0), false, 0, 0, 10);
		DrawDebugLine(worldTemp, vectorStart + FVector(0.0f, 0.0f, 25.0f), vectorEnd2, FColor(255, 0, 0), false, 0, 0, 10);
		FCollisionObjectQueryParams checkTrace(ECollisionChannel::ECC_WorldStatic);
		checkTrace.AddObjectTypesToQuery(ECollisionChannel::ECC_PhysicsBody);
		worldTemp->LineTraceSingleByObjectType(Hit, vectorStart + FVector(0.0f, 0.0f, 25.0f)
			, vectorEnd, FCollisionObjectQueryParams(checkTrace));
		worldTemp->LineTraceSingleByObjectType(Hit2, vectorStart + FVector(0.0f, 0.0f, 25.0f)
			, vectorEnd2, FCollisionObjectQueryParams(checkTrace));
		AActor* actor = Hit.GetActor();
		AActor* actor2 = Hit2.GetActor();
		if (actor2==nullptr&&str=="0")
		{
			if (FCharacterPos::flag == 0)
			{
				FCharacterPos characterpos;
				characterpos.instance = 0;
				characterpos.x = character->GetActorLocation().X;
				characterpos.y = character->GetActorLocation().Y;
				characterpos.z = character->GetActorLocation().Z;
				FCharacterPos characterpos2;
				characterpos2 = characterpos;
				characterpos2.instance = 1;
				characterposs.Push(characterpos);
				characterposs.Push(characterpos2);	
				FCharacterPos::flag = 1;
			}
			else
			{
				characterposs.Last().x = character->GetActorLocation().X;
				characterposs.Last().y = character->GetActorLocation().Y;
				characterposs.Last().z = character->GetActorLocation().Z;
			}
		}
		else
		{
			FCharacterPos::flag = 0;
		}
		if (actor)
		{
			worldTemp->GetTimerManager().ClearTimer(*checkHit);
			checkHit = nullptr;
			UE_LOG(GALog, Log, TEXT("Disable monitor"));
			character->DisableInput(NULL);
			FCharacterPos characterpos;
			auto i = reinterpret_cast<std::uintptr_t>(actor);
			characterpos.instance = i;
			characterpos.x = character->GetActorLocation().X;
			characterpos.y = character->GetActorLocation().Y;
			characterpos.z = character->GetActorLocation().Z;
			command.ReponseJsonType = ResponseDataType::OBJECT;
			characterposs.Push(characterpos);
			command.ResponseJson = ArrayToJson<FCharacterPos>(characterposs);
			FCommandHandler::cond_var->notify_one();
			FPlatformProcess::Sleep(1);
			character->EnableInput(NULL);
			UE_LOG(GALog, Log, TEXT("Timer Stop."));
			UInputSettings * Settings = const_cast <UInputSettings *>(GetDefault < UInputSettings >());
			TArray<FInputAxisKeyMapping> AxisMap;
			Settings->GetAxisMappingByName(FName("Turn"), AxisMap);
			int j = 0;
			if (scales.Num() > 0)
			{
				for (int m = 0; m < AxisMap.Num(); m++)
				{
					if (AxisMap[m].Key == "A" || AxisMap[m].Key == "D" || AxisMap[m].Key == "Gamepad_LeftX")
					{
						Settings->RemoveAxisMapping(AxisMap[m]);
						AxisMap[m].Scale = scales[j++];
						Settings->AddAxisMapping(AxisMap[m]);
					}
				}
			}
			
			Settings->SaveKeyMappings();
			characterposs.Empty();
			return;
		}
		if (str != "0")
		{
			worldTemp->GetTimerManager().ClearTimer(*checkHit);
			checkHit = nullptr;
			UE_LOG(GALog, Log, TEXT("Disable monitor"));
			FCharacterPos characterpos;
			characterpos.instance = 0;
			characterpos.x = 0;
			characterpos.y = 0;
			characterpos.z = 0;
			command.ReponseJsonType = ResponseDataType::OBJECT;
			characterposs.Push(characterpos);
			command.ResponseJson = ArrayToJson<FCharacterPos>(characterposs);
			FCommandHandler::cond_var->notify_one();
			characterposs.Empty();
		}
	}

	//进行人物转向操作
	const bool ChangeRotator(const FString& str)
	{
		APawn* pawn = nullptr;
		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* UserWidget = *Itr;

			if (UserWidget == nullptr) {
				continue;
			}

			pawn = Itr->GetWorld()->GetFirstPlayerController()->GetPawn();

			break;
		}
		
		pawn->AddControllerYawInput(FCString::Atof(*str));

		return true;
	}

	//获得角色当前偏移量
	const FRotator getRotation()
	{
		FRotator rotator = FRotator(90.0f, 90.0f, 90.0f);

		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* UserWidget = *Itr;

			if (UserWidget == nullptr) {
				continue;
			}

			rotator = Itr->GetWorld()->GetFirstPlayerController()->GetPawn()->GetActorRotation();
			break;
		}

		return rotator;
	}


	//获取转向值
	const float getScale()
	{
		UWorld* world = nullptr;
		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* UserWidget = *Itr;

			if (UserWidget == nullptr) {
				continue;
			}

			world = Itr->GetWorld();

			break;
		}
		return world->GetFirstPlayerController()->InputYawScale;
	}


	//获取地图的大小
	const FVector getLevelBound(const FString& str)
	{	
		FVector origin = FVector(0, 0, 0);
		FVector boxextent = FVector(0, 0, 0);
		
		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* actor = *Itr;

			if (actor == nullptr)
				continue;

			if (actor->GetName() == FString(str))
			{
				actor->GetActorBounds(false, origin, boxextent);
				return boxextent;
			}
		}

		return boxextent;
	}

	//人物向前位移
	const bool setLocation(const FString& str)
	{
		ACharacter* character = nullptr;
		FVector vec = FVector(0, 0, 0);

		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* actor = *Itr;

			if (actor == nullptr)
				continue;

			if (!character)
			{
				character = Itr->GetWorld()->GetFirstPlayerController()->GetCharacter();
				vec = Itr->GetWorld()->GetFirstPlayerController()->GetPawn()->GetActorForwardVector() * FCString::Atof(*str);
				vec += character->GetTargetLocation();
				UE_LOG(GALog, Log, TEXT("%f,%f,%f"), vec.X, vec.Y, vec.Z);
				if (character->SetActorLocation(vec))
				{
					return true;
					
				}
				else
					return false;
			}
				
		}
		return false;
	}

	//重新设置人物的位置
	const bool setCharacter(float& posx,float& posy)
	{
		ACharacter* character = nullptr;
		FVector vec = FVector(0, 0, 0);

		for (TObjectIterator<AActor> Itr; Itr; ++Itr)
		{
			AActor* actor = *Itr;

			if (actor == nullptr)
				continue;

			if (!character)
			{
				character = Itr->GetWorld()->GetFirstPlayerController()->GetCharacter();
				vec = character->GetTargetLocation();
				vec.X = posx;
				vec.Y = posy;
				UE_LOG(GALog, Log, TEXT("%f,%f,%f"), vec.X, vec.Y, vec.Z);
				if (character->SetActorLocation(vec))
					return true;
				break;

			}

		}
		return false;
	}

}