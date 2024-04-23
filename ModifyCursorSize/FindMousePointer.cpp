#include <iostream>
#include <UIAutomation.h>
#include "CreateCondition.h"

void FindMousePointer(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	// Define the class name to search for
	IUIAutomationCondition* condition = CreateCondition(root, L"ListView", UIA_ClassNamePropertyId);

	// Search children in settings element for the element with specified class name
	IUIAutomationElement* listItem;
	settingsElement->FindFirst(TreeScope_Children, condition, &listItem);
	if (!listItem)
	{
		condition->Release();
		throw std::runtime_error("Error finding list element");
	}
	condition->Release();

	IUIAutomationElement* visionElement = GetVisionElement(listItem, root);
}

IUIAutomationElement* GetVisionElement(IUIAutomationElement* listItem, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"Vision", UIA_NamePropertyId);

	IUIAutomationElement* visionElement;
	listItem->FindFirst(TreeScope_Children, condition, &visionElement);
	if (!visionElement)
	{
		throw std::runtime_error("Error getting Vision element")
	}
	return visionElement;
}
