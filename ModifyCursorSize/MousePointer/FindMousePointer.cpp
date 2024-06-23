#include <iostream>
#include <UIAutomation.h>
#include "CreateCondition.h"
#include "MousePointerElements.h"

void GotoMousePointer(IUIAutomationElement* mousePointerElement, IUIAutomation* root);

void FindMousePointer(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"list", UIA_LocalizedControlTypePropertyId);

	// Search children in settings element for the element with specified class name
	IUIAutomationElement* listItem = nullptr;
	while (!listItem)
	{
		settingsElement->FindFirst(TreeScope_Children, condition, &listItem);
		if (!listItem)
		{
			std::cerr << "Error finding list element..." << '\n';
		}
	}
	condition->Release();

	IUIAutomationElement* visionElement = GetVisionElement(listItem, root);

	IUIAutomationElement* mousePointerElement = GetMousePointerElement(visionElement, root);

	GotoMousePointer(mousePointerElement, root);

	// Memory Release
	mousePointerElement->Release();
	visionElement->Release();
	listItem->Release();
}

void GotoMousePointer(IUIAutomationElement* mousePointerElement, IUIAutomation* root)
{
	IUIAutomationInvokePattern* pattern = nullptr;
	mousePointerElement->GetCurrentPattern(UIA_InvokePatternId, (IUnknown**)&pattern);
	pattern->Invoke();

	pattern->Release();
}