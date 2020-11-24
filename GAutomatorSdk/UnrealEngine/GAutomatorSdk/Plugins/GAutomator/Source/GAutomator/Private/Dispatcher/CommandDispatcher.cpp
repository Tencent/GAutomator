#include "CommandDispatcher.h"
#include "Common/Log.h"
#include <thread>
#include <iostream>
#include <sstream>
#include <string>
#include "Async.h"
#include "Serialization/JsonSerializer.h"
#include "Handler/CommandHandler.h"
#include <condition_variable>
#include <mutex>

namespace WeTestU3DAutomation
{
	FCommandDispatcher::FCommandDispatcher():ListenerSocket(nullptr), SocketListenerThreadInstance(nullptr)
	{

	}

	FCommandDispatcher::~FCommandDispatcher()
	{
		if (SocketListenerThreadInstance) 
		{
			SocketListenerThreadInstance->Kill(true);

			delete SocketListenerThreadInstance;
		}
		CloseTcpConnectionListener();

	}


	bool FCommandDispatcher::Initialize()
	{
		SocketListenerThreadInstance=FRunnableThread::Create(this, TEXT("GAutomatorListenerThread"));

		return SocketListenerThreadInstance != nullptr;
	}

	bool FCommandDispatcher::CreateTCPConnectionListener(
		const FString& SocketName,
		const FString& TheIP,
		const int32 ThePort,
		const int32 ReceiveBufferSize
	) {
		uint8 IP4Nums[4];
		if (!FormatIP4ToNumber(TheIP, IP4Nums))
		{
			UE_LOG(GALog, Error, TEXT("Invalid IP! Expecting 4 parts separated by ."));
			return false;
		}

		FIPv4Endpoint Endpoint(FIPv4Address(IP4Nums[0], IP4Nums[1], IP4Nums[2], IP4Nums[3]), ThePort);
		ListenerSocket = FTcpSocketBuilder(*SocketName)
			.AsReusable()
			.BoundToEndpoint(Endpoint) // Only support local socket
			.AsBlocking() // Support block method
			.Listening(LISTEN_PORT);


		if (ListenerSocket == nullptr) 
		{
			UE_LOG(GALog, Error, TEXT("Fatal:Create Socket listener %d failed"), ThePort);
			return false;
		}
		//Set Buffer Size
		int32 NewSize = 0;
		bool SetResult= ListenerSocket->SetReceiveBufferSize(ReceiveBufferSize, NewSize);
		if(!SetResult&&NewSize==0)
		{
			UE_LOG(GALog, Error, TEXT("Set ReceiveBufferSize to %d"), NewSize);
			return false;
		}
		
		return true;
	}


	bool FCommandDispatcher::FormatIP4ToNumber(const FString& TheIP, uint8(&Out)[4]) {
		TheIP.Replace(TEXT(" "), TEXT(""));
		//String Parts
		TArray<FString> Parts;
		TheIP.ParseIntoArray(Parts, TEXT("."), false);
		if (Parts.Num() != 4)
			return false;

		for (int32 i = 0; i < 4; ++i)
		{
			Out[i] = FCString::Atoi(*Parts[i]);
		}

		return true;
	}

	bool FCommandDispatcher::CloseTcpConnectionListener() 
	{
		if (ListenerSocket) 
		{
			UE_LOG(GALog, Log, TEXT("Close Listener Socket"));
			bool CloseResult=ListenerSocket->Close();
			if (!CloseResult) {
				UE_LOG(GALog, Warning, TEXT("Close Listener Socket Fail"));
				return false;
			}
			ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ListenerSocket);
		}
		return true;
		
	}

	bool FCommandDispatcher::Init()
	{
		UE_LOG(GALog, Log, TEXT("GAutomator Thread Init"));
		return true;
	}
	uint32 FCommandDispatcher::Run()
	{
		bool CreateConnectionResult = CreateTCPConnectionListener(TEXT("GAutomatorSocket"), TEXT("127.0.0.1"), LISTEN_PORT);
		if (!CreateConnectionResult) {
			UE_LOG(GALog, Error, TEXT("Create Tcp Listener socket error"));
			return false;
		}
		UE_LOG(GALog, Log, TEXT("Create Tcp Listener socket on 127.0.0.1:%d"), LISTEN_PORT);

		HandleConnection();
		return 0;

	}
	void FCommandDispatcher::Exit()
	{
		UE_LOG(GALog, Log, TEXT("GAutomator Thread Exit"));
	}


	void FCommandDispatcher::HandleConnection() 
	{
		if (!ListenerSocket) return;
		bool Pending=false;
		FTimespan timeSpan(LISTEN_TIMEOUT_HOURS, 0, 0);
		int32 ThreadIndex = 0;
		while (true) 
		{
			CleanClosedConnectionHandler();
			if (!ListenerSocket->WaitForPendingConnection(Pending, timeSpan)&&Pending) {
				UE_LOG(GALog, Warning, TEXT("Wait connection timeout(more than 1 hours), socket failed"));
				FPlatformProcess::Sleep(0.1f);
				continue;
			}
			FSocket* ConnectionSocket = ListenerSocket->Accept(TEXT("GAutomator Received Socket Connection"));

			if (ConnectionSocket == nullptr) {
				UE_LOG(GALog, Error, TEXT("Accept Connection Failed"));
				break;
			}

			UE_LOG(GALog, Log, TEXT("Accept a connection"));

			TSharedPtr<FConnectionHandler> ConnectionHandler = MakeShareable(new FConnectionHandler(ConnectionSocket,ThreadIndex));

			ConnectionHandler->StartHandleCommand();

			ConnectionHandlers.Add(ConnectionHandler);

			ThreadIndex++;
		}

		UE_LOG(GALog, Log, TEXT("HandleConnection"));
	}

	void FCommandDispatcher::CleanClosedConnectionHandler() 
	{
		ConnectionHandlers.RemoveAll([](TSharedPtr<FConnectionHandler> ConnectionHandlerPtr) {
			if (ConnectionHandlerPtr->IsStop()) {
				UE_LOG(GALog, Log, TEXT("ConnectionHandler index = %d delete"),ConnectionHandlerPtr->GetIndex());
				return true;
			}
			return false;
		});
	}


	//////////////////////////////////////////////////////////////////////////

	FConnectionHandler::~FConnectionHandler()
	{
		if (_RunnableThread)
		{
			delete _RunnableThread;
		}
	}

	bool FConnectionHandler::Init()
	{
		UE_LOG(GALog, Log, TEXT("FConnectionHandler Init"));
		return true;
	}
	uint32 FConnectionHandler::Run()
	{
		bool result = true;
		do
		{
			result=HandleOneCommand();
		} while (result);

		return 0;
	}
	void FConnectionHandler::Exit()
	{
		Close();
		_Stop = true;
	}

	void FConnectionHandler::StartHandleCommand() 
	{
		 _RunnableThread = FRunnableThread::Create(this, *FString::Printf(TEXT("Connection_%d_Thread"), _Index));
		 _Stop = false;
	}

	bool FConnectionHandler::HandleOneCommand() 
	{
		int32 length = RecvIntLength();
		if (length <= 0) {
			return false;
		}
		TArray<uint8> BodyBinrary;

		bool RecvContentResult=RecvContent(length, BodyBinrary);
		if (!RecvContentResult) {
			return false;
		}
		FString ContentStr = StringFromBinaryArray(BodyBinrary);
		UE_LOG(GALog, Log, TEXT("Recv command:%s"), *ContentStr);


		///Deserialize Request
		TSharedPtr<FJsonValue> JsonParsed;
		TSharedRef< TJsonReader<TCHAR> > JsonReader = TJsonReaderFactory<TCHAR>::Create(ContentStr);

		bool BFlag = FJsonSerializer::Deserialize(JsonReader, JsonParsed);

		if (!BFlag) {
			UE_LOG(GALog, Error, TEXT("Deserialize request to json failed.\n %s"));
			return false;
		}

		FString Response;

		bool res=HandleCommandInGameThread(JsonParsed, Response);

		length= this->SendData(Response);


		return res;
	}

	void FConnectionHandler::Close()
	{
		if (_Socket)
		{
			UE_LOG(GALog, Log, TEXT("Close Index(%d) Socket"), _Index);
			bool CloseResult = _Socket->Close();
			if (!CloseResult) {
				UE_LOG(GALog, Warning, TEXT("Close Listener Socket Fail"));
			}
			ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(_Socket);
			_Socket = nullptr;
		}

	}
	int32 FConnectionHandler::RecvIntLength()
	{
		if (!_Socket) return -1;

		TArray<uint8> ReceivedData;
		uint32 Size = 0;

		bool result = _Socket->Wait(ESocketWaitConditions::WaitForRead, RecvLengthTimeOut);
		if (!result) {
			UE_LOG(GALog, Error, TEXT("Recv Error,connection is closed"));
			return -1;
		}

		int32 Read = 0;
		ReceivedData.Init(0, Int32Length);
		result = _Socket->Recv(ReceivedData.GetData(), Int32Length, Read, ESocketReceiveFlags::WaitAll);

		if (!result) {
			UE_LOG(GALog, Error, TEXT("Recv Failed Read Data = %d"),Read);
			return -1;
		}

		if (Int32Length != Read)
		{
			UE_LOG(GALog, Error, TEXT("Recv data %d less than require %d"), Int32Length, Read);
			return false;
		}
		
		int32 length = *((int32*)ReceivedData.GetData());

		return length;
	}
	
	bool FConnectionHandler::RecvContent(int32 length, TArray<uint8>& ReceivedData)
	{
		uint32 Size = 0;

		bool result = _Socket->Wait(ESocketWaitConditions::WaitForRead, RecvContentTimeOut);
		if (!result) {
			UE_LOG(GALog, Error, TEXT("Recv timeout ,timeout second = %d"), RecvContentTimeOut.GetSeconds());
			return false;
		}

		int32 Read = 0;
		ReceivedData.Init(0, length);
		result = _Socket->Recv(ReceivedData.GetData(), length, Read, ESocketReceiveFlags::WaitAll);

		if (!result) {
			UE_LOG(GALog, Error, TEXT("Recv content failed"));
			return false;
		}
		if (length != Read)
		{
			UE_LOG(GALog, Error, TEXT("Recv data %d less than require %d"),length,Read);
			return false;
		}
		return true;
	}

	FString FConnectionHandler::StringFromBinaryArray(TArray<uint8>& BinaryArray) {
		BinaryArray.Add(0);
		return FString(ANSI_TO_TCHAR(reinterpret_cast<const char*>(BinaryArray.GetData())));
	}

	bool FConnectionHandler::HandleCommandInGameThread(const TSharedPtr<FJsonValue>& InValue,FString& OutResponse)
	{

		FCommandHandler CommandHandler(InValue);
		std::mutex m;
		std::condition_variable* cond_var= FCommandHandler::cond_var;


		AsyncTask(ENamedThreads::GameThread, [&CommandHandler,&OutResponse,&m,cond_var]() {

			std::unique_lock<std::mutex> lock(m);
			OutResponse =CommandHandler.HandleCommand();

			UE_LOG(GALog, Log, TEXT("Response body : %s"), *OutResponse);
			if(FCommandHandler::flag==0)
				cond_var->notify_one();
		});
		std::unique_lock<std::mutex> lock(m);
		cond_var->wait(lock);
		if (FCommandHandler::flag != 0)
		{
			OutResponse = CommandHandler.GetResponse();
			FCommandHandler::flag = 0;
		}
		return true;
	}

	int32 FConnectionHandler::SendData(const FString& Data) 
	{
		if (!_Socket) return -1;

		FTCHARToUTF8 ResponseBin(*Data);

		int32 SendSize=0;
		int32 TotalSend = 0;
		int32 Length = ResponseBin.Length();
		UE_LOG(GALog, Log, TEXT("Send string size =%d, writer byte size =%d "), Length, Length);
		bool result = _Socket->Send(reinterpret_cast<const uint8*>(&Length), Int32Length, SendSize);

		if (!result) {
			UE_LOG(GALog, Error, TEXT("Send Data lenght Failed"));
			return -1;
		}

		SendSize = 0;

		while (TotalSend < Length) {
			result = _Socket->Send(reinterpret_cast<const uint8*>(ResponseBin.Get())+ TotalSend, Length, SendSize);
			if (!result) {
				UE_LOG(GALog, Error, TEXT("Send Data Failed"));
				return -1;
			}
			TotalSend += SendSize;
		}
		

		return TotalSend;
	}

	std::condition_variable* FCommandHandler::cond_var = new std::condition_variable();
	int FCommandHandler::flag = 0;
}