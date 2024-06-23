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

	int loops = 0;
	IUIAutomationElement* mousePointerElement = nullptr;
	while (!mousePointerElement)
	{
		loops += 1;
		visionElement->FindFirst(TreeScope_Children, condition, &mousePointerElement);
		if (loops > 18)
		{
			throw std::runtime_error("Error getting Pointer element");
		}
	}
	condition->Release();
	return mousePointerElement;
}