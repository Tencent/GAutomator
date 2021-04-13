#pragma once

#include "CoreMinimal.h"
#include "Common/Log.h"
#include "Dispatcher/CommandDispatcher.h"
#include "Templates/SharedPointerInternals.h"
#include "Serialization/JsonSerializer.h"
#include "Protocol/ProtocolCommon.h"
#include <condition_variable>

namespace WeTestU3DAutomation
{
	class FCommandHandler
	{
	public:
		explicit FCommandHandler(const TSharedPtr<FJsonValue> InRequest) :Request(InRequest){};
		virtual ~FCommandHandler();

		FString HandleCommand();
		FString GetResponse();
		static std::condition_variable* cond_var;
		static int flag;
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
		void HandleSwipCharacter();
		void HandleSetRotator();
		void GetInputScale();
		void GetBound();
		void SetLocation();
		void GetRotator();
		void SetCharacter();
		void CallRegisterHandler();
		void GetEqInfo();

	};



}