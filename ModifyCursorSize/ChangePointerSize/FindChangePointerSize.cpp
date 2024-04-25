#include "ChangePointerSizeElements.h"
#include "CreateCondition.h"
#include <iostream>
#include <UIAutomation.h>

void ChangePointerSize(IUIAutomationElement* sizeElement);

void FindChangePointerSize(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationElement* groupElement = GetGroupElement(settingsElement, root);

	IUIAutomationElement* paneElement = GetPaneElement(groupElement, root);
	
	IUIAutomationElement* scElement = GetSizeColorElement(paneElement, root);
	
	IUIAutomationElement* sizeElement = GetSizeElement(scElement, root);

	ChangePointerSize(sizeElement);

	// Memory release
	sizeElement->Release();
	scElement->Release();
	paneElement->Release();
	groupElement->Release();
	settingsElement->Release();
	root->Release();
	CoUninitialize();

}

void ChangePointerSize(IUIAutomationElement* sizeElement)
{
	IRangeValueProvider* pValuePattern;
	sizeElement->GetCurrentPattern(UIA_RangeValuePatternId, (IUnknown**)&pValuePattern);

	double checkValue = 1.0;
	double currentValue;
	pValuePattern->get_Value(&currentValue);

	if (currentValue == checkValue)
	{
		pValuePattern->SetValue(4.0);
	}
	else
	{
		pValuePattern->SetValue(1.0);
	}
	pValuePattern->Release();
}
