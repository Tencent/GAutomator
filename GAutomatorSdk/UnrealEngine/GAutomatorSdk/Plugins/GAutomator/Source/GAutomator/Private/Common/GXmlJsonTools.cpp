#include "GXmlJsonTools.h"
#include "Common/Log.h"

namespace WeTestU3DAutomation
{
	TSharedPtr<FXmlFile> CreateFXmlFile()
	{
		const FString FileTemplate = "<?xml version=\"1.0\" encoding=\"UTF - 8\"?>\n<AbstractRoot engine=\"ue4\">\n</AbstractRoot>";

		TSharedPtr<FXmlFile> xml = MakeShareable(new FXmlFile(FileTemplate, EConstructMethod::ConstructFromBuffer));

		return MoveTemp(xml);
	}

	FXmlNode* AddFXmlNode(FXmlNode* InParent, const FString& InTag, const FString& InContent)
	{
		if (InParent == nullptr) {
			UE_LOG(GALog, Warning, TEXT("Parent XmlNode Can't be nullptr"));
			return nullptr;
		}

		InParent->AppendChildNode(InTag, InContent);

		TArray<FXmlNode*> ChildrenNodes = InParent->GetChildrenNodes();

		if (ChildrenNodes.Num() > 0) {
			FXmlNode* OutValue = ChildrenNodes.Last();
			return OutValue;
		}
		return nullptr;
	}

	void WriteNodeHierarchy(const FXmlNode& Node, const FString& Indent, FString& Output) {
		Output += Indent + FString::Printf(TEXT("<%s"), *Node.GetTag());
		for (const FXmlAttribute& Attribute : Node.GetAttributes())
		{
			FString EscapedValue = Attribute.GetValue();
			EscapedValue.ReplaceInline(TEXT("&"), TEXT("&amp;"), ESearchCase::CaseSensitive);
			EscapedValue.ReplaceInline(TEXT("\""), TEXT("&quot;"), ESearchCase::CaseSensitive);
			EscapedValue.ReplaceInline(TEXT("'"), TEXT("&apos;"), ESearchCase::CaseSensitive);
			EscapedValue.ReplaceInline(TEXT("<"), TEXT("&lt;"), ESearchCase::CaseSensitive);
			EscapedValue.ReplaceInline(TEXT(">"), TEXT("&gt;"), ESearchCase::CaseSensitive);
			Output += FString::Printf(TEXT(" %s=\"%s\""), *Attribute.GetTag(), *EscapedValue);
		}

		// Write the node contents
		const FXmlNode* FirstChildNode = Node.GetFirstChildNode();
		if (FirstChildNode == nullptr)
		{
			const FString& Content = Node.GetContent();
			if (Content.Len() == 0)
			{
				Output += TEXT(" />") LINE_TERMINATOR;
			}
			else
			{
				Output += TEXT(">") + Content + FString::Printf(TEXT("</%s>"), *Node.GetTag()) + LINE_TERMINATOR;
			}
		}
		else
		{
			Output += TEXT(">") LINE_TERMINATOR;
			for (const FXmlNode* ChildNode = FirstChildNode; ChildNode != nullptr; ChildNode = ChildNode->GetNextNode())
			{
				WriteNodeHierarchy(*ChildNode, Indent + TEXT("\t"), Output);
			}
			Output += Indent + FString::Printf(TEXT("</%s>"), *Node.GetTag()) + LINE_TERMINATOR;
		}
	}
}