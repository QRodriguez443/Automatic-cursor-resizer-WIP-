#include "CreateCondition.h"
#include <iostream>
#include <UIAutomation.h>

IUIAutomationElement* GetGroupElement(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"group", UIA_LocalizedControlTypePropertyId);

	IUIAutomationElement* groupElement = nullptr;
	while (!groupElement)
	{
		settingsElement->FindFirst(TreeScope_Children, condition, &groupElement);
		if (!groupElement)
		{
			std::cerr << "Error getting Group element..." << '\n';
		}
	}
	condition->Release();
	return groupElement;
}

IUIAutomationElement* GetPaneElement(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"pane", UIA_LocalizedControlTypePropertyId);

	IUIAutomationElement* paneElement;
	settingsElement->FindFirst(TreeScope_Children, condition, &paneElement);
	if (!paneElement)
	{
		condition->Release();
		throw std::runtime_error("Error getting Pane element");
	}
	condition->Release();
	return paneElement;
}

IUIAutomationElement* GetSizeColorElement(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"Change pointer size and color", UIA_NamePropertyId);

	IUIAutomationElement* scElement;
	settingsElement->FindFirst(TreeScope_Children, condition, &scElement);
	if (!scElement)
	{
		condition->Release();
		throw std::runtime_error("Error getting Size & Color element");
	}
	condition->Release();
	return scElement;
}

IUIAutomationElement* GetSizeElement(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"Change pointer size", UIA_NamePropertyId);

	IUIAutomationElement* sizeElement;
	settingsElement->FindFirst(TreeScope_Children, condition, &sizeElement);
	if (!sizeElement)
	{
		condition->Release();
		throw std::runtime_error("Error getting Size element");
	}
	condition->Release();
	return sizeElement;
}
