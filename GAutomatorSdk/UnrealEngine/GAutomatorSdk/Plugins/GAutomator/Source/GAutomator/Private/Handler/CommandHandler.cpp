
#include "Handler/CommandHandler.h"
#include "Common/Log.h"
#include "UI/UIManager.h"
#include "Common/GXmlJsonTools.h"
#include "Engine.h"
#include <cstdint>

namespace WeTestU3DAutomation
{

	FCommandHandler::~FCommandHandler() {

	}

	FString FCommandHandler::HandleCommand(){
		Dispatcher();
		FString ReponseJsonStr = CommandResponse.ToJson();
		return ReponseJsonStr;
	}
	
	FString FCommandHandler::GetResponse() {
		return CommandResponse.ToJson();
	}

	bool FCommandHandler::Dispatcher() {
		if (!Request.IsValid()) {
			CommandResponse.ResponseJson = TEXT("Request is null");
			CommandResponse.status = ResponseStatus::UNPACK_ERROR;
			return false;
		}
		int32 cmd;
		bool JsonGetRes = Request->AsObject()->TryGetNumberField(TEXT("cmd"), cmd);
		CommandResponse.cmd = cmd;
		FString ValueField(TEXT("value"));
		ValuePtr = Request->AsObject()->TryGetField(ValueField);

		if (!JsonGetRes||!ValuePtr.IsValid()) {
			CommandResponse.ResponseJson = TEXT("Request data format is invaild");
			CommandResponse.status = ResponseStatus::UNPACK_ERROR;
			return false;
		}

		switch (cmd) {
		case Cmd::GET_VERSION:
		{
			HandleGetVersion();
			break;
		}
		case Cmd::DUMP_TREE:
		{
			HandleDumpTree();
			break;
		}
		case Cmd::FIND_ELEMENTS:
		{
			HandleFindElements();
			break;
		}
		case Cmd::GET_ELEMENTS_BOUND:
		{
			HandleGetElementsBound();
			break;
		}
		case Cmd::GET_CURRENT_SCENE:
		{
			HandleGetCurrentLevelName();
			break;
		}
		case Cmd::FIND_ELEMENT_BY_POS:
		{
			HandleGetElementByPos();
			break;
		}
		case Cmd::GET_ELEMENT_TEXT:
		{
			HandleGetText();
			break;
		}
		case Cmd::GET_CHARACTER_SWIP:
		{
			FCommandHandler::flag = 1;
			HandleSwipCharacter();
			break;
		}
		case Cmd::SET_CHANGEROTATOR:
		{
			HandleSetRotator();
			break;
		}
		case Cmd::GET_SCALE:
		{
			GetInputScale();
			break;
		}
		case Cmd::GET_BOUND:
		{
			GetBound();
			break;
		}
		case Cmd::SET_LOCATION:
		{
			SetLocation();
			break;
		}
		case Cmd::GET_ROTATOR:
		{
			GetRotator();
			break;
		}
		case Cmd::SET_CHARACTER:
		{
			SetCharacter();
			break;
		}
		case Cmd::CALL_REGISTER_HANDLER:
		{
			CallRegisterHandler();
			break;
		}
		case Cmd::GET_EQUIPMETN_INFO:
		{
			GetEqInfo();
			break;
		}
		default:
		{
			CommandResponse.ResponseJson = FString::Printf(TEXT("unknow cmd %d"),cmd);
			CommandResponse.status = ResponseStatus::NO_SUCH_CMD;
		}
		}
		return true;
	}

	void FCommandHandler::HandleGetVersion() {
		UE_LOG(GALog, Log, TEXT("Get Sdk version"));
		FVersionData VersionData;
		CommandResponse.ResponseJson = VersionData.ToJson();
		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		UE_LOG(GALog, Log, TEXT("SDK Version Info"), *CommandResponse.ResponseJson);
	}

	void FCommandHandler::HandleDumpTree()
	{
		UE_LOG(GALog, Log, TEXT("HandleDumpTree"));
		FDumpTree DumpTree;
		DumpTree.xml = GetCurrentWidgetTree();

		CommandResponse.ResponseJson = DumpTree.ToJson();
		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;

		UE_LOG(GALog, Log, TEXT("Dump Tree Information :"), *CommandResponse.ResponseJson);
	}

	void FCommandHandler::HandleFindElements()
	{
		UE_LOG(GALog, Log, TEXT("HandleFindElements"));

		const TArray<TSharedPtr<FJsonValue>> names = ValuePtr->AsArray();
		TArray<FElementInfo> ElementInfos;

		for (const TSharedPtr<FJsonValue> SearchElement : names)
		{
			FElementInfo ElementInfo;
			FString name = SearchElement->AsString();
			
			const UWidget* Object=FindUWidgetObject(name);


			ElementInfo.name = MoveTemp(name);
			if (Object == nullptr) {
				ElementInfo.instance = -1;
			}
			else {
				auto i = reinterpret_cast<std::uintptr_t>(Object);
				ElementInfo.instance = i;
			}

			ElementInfos.Add(ElementInfo);
		}

		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		CommandResponse.ResponseJson = ArrayToJson<FElementInfo>(ElementInfos);
		
	}


	void FCommandHandler::HandleGetElementsBound()
	{
		UE_LOG(GALog, Log, TEXT("HandleGetElementsBound"));

		const TArray<TSharedPtr<FJsonValue>> names = ValuePtr->AsArray();
		TArray<FBoundInfo> BoundInfos;

		FUWidgetHelper WidgetHelper;
		bool res=WidgetHelper.Initialize();

		for (const TSharedPtr<FJsonValue> name : names)
		{
			FString NameStr = name->AsString();
			FBoundInfo BoundInfo;

			UE_LOG(GALog,Log,TEXT("Get %s bound"),*NameStr);

			BoundInfo.path = NameStr;
			BoundInfo.instance = 0;
			res=WidgetHelper.GetElementBound(NameStr, BoundInfo);

			BoundInfos.Push(BoundInfo);
		}

		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		CommandResponse.ResponseJson = ArrayToJson<FBoundInfo>(BoundInfos);
	}

	void FCommandHandler::HandleGetCurrentLevelName()
	{
		UE_LOG(GALog, Log, TEXT("HandleGetCurrentLevelName"));

		FString Scene;

		bool Result = GetCurrentLevelName(Scene);

		if(Result)
		{
			CommandResponse.ResponseJson = MoveTemp(Scene);
		}
		else
		{
			CommandResponse.status = ResponseStatus::UN_KNOW_ERROR;
			CommandResponse.ResponseJson = "GEngine or GWorld Is Null";
			return;
		}
		CommandResponse.ReponseJsonType = ResponseDataType::STRING;
	}

	void FCommandHandler::HandleGetElementByPos()
	{
		UE_LOG(GALog, Log, TEXT("HandleGetElementByPos"));

		const TArray<TSharedPtr<FJsonValue>> Pos = ValuePtr->AsArray();
		
		if (Pos.Num() != 2) 
		{
			CommandResponse.status = ResponseStatus::UNPACK_ERROR;
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "Parameter is invaild";
			return;
		}

		float x=Pos[0]->AsNumber();
		float y = Pos[1]->AsNumber();

		FUWidgetHelper WidgetHelper;
		bool res = WidgetHelper.Initialize();

		const UWidget* WidgetPtr=WidgetHelper.FindUWidgetObjectByPos(x, y);

		if (WidgetPtr == nullptr)
		{
			CommandResponse.status = ResponseStatus::GAMEOBJ_NOT_EXIST;
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "";
			return;
		}

		FElementInfo ElementInfo;

		ElementInfo.name = WidgetPtr->GetName();
		auto i = reinterpret_cast<std::uintptr_t>(WidgetPtr);
		ElementInfo.instance = i;
		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		CommandResponse.ResponseJson = ElementInfo.ToJson();
	}

	void FCommandHandler::HandleGetText()
	{
		UE_LOG(GALog, Log, TEXT("HandleGetText"));


		const UWidget* Widget=FindUWidgetObject(ValuePtr->AsString());

		if (Widget == nullptr) 
		{
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.status = ResponseStatus::GAMEOBJ_NOT_EXIST;
			CommandResponse.ResponseJson = FString::Printf(TEXT("UObject %s not exited"), *ValuePtr->AsString());
			return;
		}


		FString Label=GetUWidgetLabelText(Widget);
		UE_LOG(GALog, Log, TEXT("Get label = %s"), *Label);

		CommandResponse.ReponseJsonType = ResponseDataType::STRING;
		CommandResponse.ResponseJson = Label;
	}

	void FCommandHandler::HandleSwipCharacter()
	{
		UE_LOG(GALog, Log, TEXT("MoveCharacter"));

		TArray<FCharacterPos> characterposs;
		
		const TArray<TSharedPtr<FJsonValue>> Pos = ValuePtr->AsArray();
		if (Pos.Num() != 3)
		{
			CommandResponse.status = ResponseStatus::UNPACK_ERROR;
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "Parameter is invaild";
			return;
		}
		TimeTemp* timeEv = new TimeTemp(CommandResponse);
		timeEv->scales = Pos[0]->AsNumber();
		timeEv->tickTime = Pos[1]->AsNumber();
		timeEv->loop = Pos[2]->AsBool();
		if (timeEv->SetTimerHandle())
		{
			UE_LOG(GALog, Log, TEXT("SETTIMER SUCCESS"));
		}
		else
		{
			UE_LOG(GALog, Log, TEXT("SETTIMER FAILURE"));
			CommandResponse.status = ResponseStatus::UN_KNOW_ERROR;
			CommandResponse.ResponseJson = FString::Printf(TEXT("Error"), *ValuePtr->AsString());
			return;
		}
	}

	void FCommandHandler::HandleSetRotator()
	{
		UE_LOG(GALog, Log, TEXT("SetRotator"));

		if (ChangeRotator(ValuePtr->AsString()))
		{
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "success";
		}
		else
		{
			CommandResponse.status = ResponseStatus::UN_KNOW_ERROR;
			CommandResponse.ResponseJson = FString::Printf(TEXT("Error"), *ValuePtr->AsString());
		}
	}

	void FCommandHandler::GetInputScale()
	{
		UE_LOG(GALog, Log, TEXT("GetScale"));
		float scale = getScale();
		FString scaleStr = FString::SanitizeFloat(scale);
		CommandResponse.ReponseJsonType = ResponseDataType::STRING;
		CommandResponse.ResponseJson = MoveTemp(scaleStr);
		return;
	}

	void FCommandHandler::GetBound()
	{
		UE_LOG(GALog, Log, TEXT("GetBound"));
		FVector vector = getLevelBound(ValuePtr->AsString());
		TArray<FBound> Bounds;
		FBound Bound;
		Bound.x = vector.X;
		Bound.y = vector.Y;
		Bound.z = vector.Z;
		Bounds.Push(Bound);

		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		CommandResponse.ResponseJson = ArrayToJson<FBound>(Bounds);
		
		return;
	}

	void FCommandHandler::SetLocation()
	{
		UE_LOG(GALog, Log, TEXT("SetLocation"));
		
		if (setLocation(ValuePtr->AsString()))
		{
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "success";
		}
		else
		{
			CommandResponse.status = ResponseStatus::UN_KNOW_ERROR;
			CommandResponse.ResponseJson = FString::Printf(TEXT("Error"), *ValuePtr->AsString());
		}
	}

	void FCommandHandler::GetRotator()
	{
		UE_LOG(GALog, Log, TEXT("GetRotator"));

		FRotator rotator = getRotation();
		TArray<FBound> Bounds;
		FBound Bound;
		Bound.x = rotator.Roll;
		Bound.y = rotator.Pitch;
		Bound.z = rotator.Yaw;
		Bounds.Push(Bound);

		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		CommandResponse.ResponseJson = ArrayToJson<FBound>(Bounds);

		return;
	}

	void FCommandHandler::SetCharacter()
	{
		UE_LOG(GALog, Log, TEXT("SetCharacter"));

		const TArray<TSharedPtr<FJsonValue>> Pos = ValuePtr->AsArray();

		if (Pos.Num() != 2)
		{
			CommandResponse.status = ResponseStatus::UNPACK_ERROR;
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "Parameter is invalid";
			return;
		}

		float x = Pos[0]->AsNumber();
		float y = Pos[1]->AsNumber();

		if (setCharacter(x, y))
		{
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "success";
		}
		else
		{
			CommandResponse.status = ResponseStatus::UN_KNOW_ERROR;
			CommandResponse.ResponseJson = FString::Printf(TEXT("Error"), *ValuePtr->AsString());
		}
	}

	void FCommandHandler::CallRegisterHandler()
	{
		UE_LOG(GALog, Log, TEXT("CallRegisterHandler"));

		const TArray<TSharedPtr<FJsonValue>> Pos = ValuePtr->AsArray();

		if (Pos.Num() != 2)
		{
			CommandResponse.status = ResponseStatus::UNPACK_ERROR;
			CommandResponse.ReponseJsonType = ResponseDataType::STRING;
			CommandResponse.ResponseJson = "Parameter is invalid";
			return;
		}

		FName funcname = FName(*(Pos[0]->AsString()));
		FString funcparms = Pos[1]->AsString();

		FString outpar = callRegisterHandler(funcname, funcparms);
		TArray<FCallInfo> callinfos;
		FCallInfo callinfo;
		callinfo.info = outpar;
		callinfos.Push(callinfo);

		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		CommandResponse.ResponseJson = ArrayToJson<FCallInfo>(callinfos);

		return;
	}

	void FCommandHandler::GetEqInfo()
	{
		UE_LOG(GALog, Log, TEXT("GetMobileInof"));

		FUWidgetHelper WidgetHelper;
		bool res = WidgetHelper.Initialize();
		FVector vector = WidgetHelper.GetMobileinfo();

		//FRotator rotator = getRotation();
		TArray<FBound> Bounds;
		FBound Bound;
		Bound.x = vector.X;
		Bound.y = vector.Y;
		Bound.z = vector.Z;
		Bounds.Push(Bound);

		CommandResponse.ReponseJsonType = ResponseDataType::OBJECT;
		CommandResponse.ResponseJson = ArrayToJson<FBound>(Bounds);

		return;
	}


}