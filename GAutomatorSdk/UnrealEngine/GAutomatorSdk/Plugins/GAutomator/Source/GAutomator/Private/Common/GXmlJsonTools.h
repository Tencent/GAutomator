#pragma once

#include "XmlParser.h"
#include "Serialization/JsonSerializer.h"
#include "Policies/CondensedJsonPrintPolicy.h"

/*
*
* XmlParser less function, does not allow inheritance.Fuck
*/
namespace WeTestU3DAutomation
{
	TSharedPtr<FXmlFile> CreateFXmlFile();

	FXmlNode* AddFXmlNode(FXmlNode* InParent, const FString& InTag, const FString& InContent);

	void WriteNodeHierarchy(const FXmlNode& Node, const FString& Indent, FString& Output);

	template<typename T>
	FString ArrayToJson(TArray<T>& InArray)
	{
		FString JsonStr;
		auto JsonWriter = TJsonWriterFactory<TCHAR, TCondensedJsonPrintPolicy<TCHAR>>::Create(&JsonStr);

		JsonWriter->WriteArrayStart();

		for (T& e : InArray)
		{
			FString ElementInfoStr = e.ToJson();
			JsonWriter->WriteRawJSONValue(ElementInfoStr);
		}

		JsonWriter->WriteArrayEnd();
		JsonWriter->Close();

		return MoveTemp(JsonStr);
	}
}