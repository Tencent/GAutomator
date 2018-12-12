#pragma once

#include "CoreMinimal.h"
#include "Sockets.h"
#include "Networking.h"
#include "Runnable.h"
#include "Interfaces/IPv4/IPv4Endpoint.h"
#include "JsonValue.h"

namespace WeTestU3DAutomation
{
	class FConnectionHandler;

	class FCommandDispatcher :public FRunnable
	{
	public:
		static const int32 MAX_BACK_CONNECTION = 5;//The number of connections to queue before refusing them.
		static const int32 LISTEN_PORT = 27019;
		static const int32 LISTEN_TIMEOUT_HOURS = 1;

		static constexpr const char* SOCKET_NAME = "GAutomatorSocket";

		explicit FCommandDispatcher();
		virtual ~FCommandDispatcher();
		/*
		* Create Listener socket
		* Create Accept thread
		* One connection one thread
		* @return Create Listener socket error return false
		*/
		bool Initialize();

		virtual bool Init() override;
		virtual uint32 Run() override;
		virtual void Exit() override;


	private:
		FSocket* ListenerSocket;
		FRunnableThread* SocketListenerThreadInstance;
		TArray<TSharedPtr<FConnectionHandler>> ConnectionHandlers;

		bool CreateTCPConnectionListener(
			const FString& SocketName,
			const FString& TheIP,
			const int32 ThePort,
			const int32 ReceiveBufferSize = 200 * 1024 * 1024
		);

		bool CloseTcpConnectionListener();

		void HandleConnection();

		//Format String IP4 to number array
		bool FormatIP4ToNumber(const FString& TheIP, uint8(&Out)[4]);

		//delete Closed FConnectionHandler
		void CleanClosedConnectionHandler();
	};

	/*
	* Receive command and deserialize command
	*/
	class FConnectionHandler :public FRunnable
	{
	public:
		explicit FConnectionHandler(FSocket* Socket, uint32 Index) :_Socket(Socket), _Index(Index), _Stop(false), _RunnableThread(nullptr), RecvLengthTimeOut(8, 0, 0), RecvContentTimeOut(0, 0, 10) {};
		virtual ~FConnectionHandler();

		virtual bool Init() override;
		virtual uint32 Run() override;
		virtual void Exit() override;

		void StartHandleCommand();
		bool IsStop() { return _Stop; };
		uint32 GetIndex() { return _Index; };

	private:
		const static int32 Int32Length = 4;

		FSocket* _Socket;
		uint32 _Index;
		bool _Stop;
		FRunnableThread* _RunnableThread;
		FTimespan RecvLengthTimeOut;
		FTimespan RecvContentTimeOut;

		void Close();

		//Command Request frame always start int32, 4bit. the length of body.
		int32 RecvIntLength();

		//Recv the body and convert to FString(encode) by utf-8
		bool RecvContent(int32 length, TArray<uint8>& Outer);

		FString StringFromBinaryArray(TArray<uint8>& BinaryArray);

		//Send Data,start int32 ,the length of body
		int32 SendData(const FString& Data);

		bool HandleCommandInGameThread(const TSharedPtr<FJsonValue>& InValue,FString& Response);

		/*
		* 1、recv the request length
		* 2、recv the request body
		* 3、handle the request in gamethread
		* 4、send the reponse
		*/
		bool HandleOneCommand();

	
	};
}