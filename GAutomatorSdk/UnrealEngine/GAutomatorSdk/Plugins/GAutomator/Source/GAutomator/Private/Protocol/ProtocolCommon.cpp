#include "ProtocolCommon.h"
#include "CoreMinimal.h"
#include "Serialization/JsonSerializer.h"
#include "Runtime/Launch/Resources/Version.h"
#include "Policies/CondensedJsonPrintPolicy.h"

namespace WeTestU3DAutomation
{
	FString FCommand::ToJson() {
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("cmd", cmd);
		JsonWriter->WriteValue("status", (int32)status);
		if (ResponseJson.IsEmpty()) {
			ResponseJson = TEXT("\"\"");
		}
		if (ReponseJsonType == ResponseDataType::STRING) {
			JsonWriter->WriteValue("data", ResponseJson);
		}
		else {
			JsonWriter->WriteRawJSONValue("data", ResponseJson);
		}
		
		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		UE_LOG(LogTemp, Log, TEXT("Serialize data:%s"), *JsonStr);

		return MoveTemp(JsonStr);
	}

	FString FVersionData::ToJson() 
	{
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("sdkVersion", sdkVersion);
		JsonWriter->WriteValue("engine", engine);
		JsonWriter->WriteValue("engineVersion", engineVersion);
		JsonWriter->WriteValue("sdkUIType", sdkUIType);

		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}

	FString FDumpTree::ToJson()
	{
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("scene", scene);
		JsonWriter->WriteValue("xml", xml);

		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}

	FString FElementInfo::ToJson()
	{
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("name", name);
		JsonWriter->WriteValue("instance", instance);

		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}

	FString FBoundInfo::ToJson()
	{
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);
		
		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("instance", instance);
		JsonWriter->WriteValue("visible", visible);
		JsonWriter->WriteValue("existed", existed);
		JsonWriter->WriteValue("width", width);
		JsonWriter->WriteValue("height", height);
		JsonWriter->WriteValue("x", x);
		JsonWriter->WriteValue("y", y);
		JsonWriter->WriteValue("path", path);

		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}

	FString FCharacterPos::ToJson()
	{
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("instance", instance);
		JsonWriter->WriteValue("x", x);
		JsonWriter->WriteValue("y", y);
		JsonWriter->WriteValue("z", z);

		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}

	FString FBound::ToJson()
	{
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("x", x);
		JsonWriter->WriteValue("y", y);
		JsonWriter->WriteValue("z", z);

		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}

	FString FCallInfo::ToJson()
	{
		FString JsonStr;

		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteObjectStart();

		JsonWriter->WriteValue("info", info);

		JsonWriter->WriteObjectEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}

}
