#pragma once

#include "CoreMinimal.h"
#include "Common/Log.h"
#include "Dispatcher/CommandDispatcher.h"
#include "Templates/SharedPointerInternals.h"
#include "Serialization/JsonSerializer.h"
#include "Protocol/ProtocolCommon.h"

namespace WeTestU3DAutomation
{
	class FCommandHandler
	{
	public:
		explicit FCommandHandler(const TSharedPtr<FJsonValue> InRequest) :Request(InRequest){};
		virtual ~FCommandHandler();

		FString HandleCommand();
	private:
		const TSharedPtr<FJsonValue> Request;
		TSharedPtr<FJsonValue> ValuePtr;
		FCommand CommandResponse;
		
		/*
		*Find Command Handle function, and handle the command get the response
		*/
		bool Dispatcher();

		////////////////////////////////Handle Cmd Function //////////////////////////////
		void HandleGetVersion(); //GET_VERSION
		void HandleDumpTree(); //DUMP_TREE
		void HandleFindElements();//FIND_ELEMENTS
		void HandleGetElementsBound();//GET_ELEMENTS_BOUND
		void HandleGetCurrentLevelName();//GET_CURRENT_SCENE
		void HandleGetElementByPos(); //FIND_ELEMENT_BY_POS
		void HandleGetText(); //GET_ELEMENT_TEXT
	};
}