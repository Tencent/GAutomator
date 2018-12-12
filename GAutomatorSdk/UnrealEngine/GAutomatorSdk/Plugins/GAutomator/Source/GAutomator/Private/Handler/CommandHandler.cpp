
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
}