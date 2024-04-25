#include <iostream>
#include <UIAutomation.h>
#include "CreateCondition.h"

IUIAutomationElement* GetVisionElement(IUIAutomationElement* listItem, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"Vision", UIA_NamePropertyId);

	IUIAutomationElement* visionElement;
	listItem->FindFirst(TreeScope_Children, condition, &visionElement);
	if (!visionElement)
	{
		condition->Release();
		throw std::runtime_error("Error getting Vision element");
	}
	condition->Release();
	return visionElement;
}

IUIAutomationElement* GetMousePointerElement(IUIAutomationElement* visionElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"Mouse pointer", UIA_NamePropertyId);

	IUIAutomationElement* mousePointerElement;
	visionElement->FindFirst(TreeScope_Children, condition, &mousePointerElement);
	if (!mousePointerElement)
	{
		condition->Release();
		throw std::runtime_error("Error getting Mouse pointer element");
	}
	condition->Release();
	return mousePointerElement;
}