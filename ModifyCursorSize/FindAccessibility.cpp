#include "AccessibilityElements.h"
#include <iostream>
#include <UIAutomation.h>

// Find the accessibility element and access its page
void FindAccessibilityButton(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	// Define property's name
	VARIANT pValue;
	pValue.vt = VT_BSTR;
	pValue.bstrVal = SysAllocString(L"ScrollViewer");

	// Create condition
	IUIAutomationCondition* condition = nullptr;
	root->CreatePropertyCondition(UIA_ClassNamePropertyId, pValue, &condition);

	// Get child of settingsElement: pane
	IUIAutomationElementArray* pane;
	settingsElement->FindAll(TreeScope_Children, condition, &pane);
	if (!pane)
	{
		SysFreeString(pValue.bstrVal);
		throw std::runtime_error("Error finding pane");
	}
	SysFreeString(pValue.bstrVal);

	// Get pane element
	IUIAutomationElement* paneElement = GetPaneElement(pane);

	// Get pane's child: list
	IUIAutomationElement* listElement = GetList(paneElement, root);

	// Get Accessibility element
	IUIAutomationElement* AccessibilityElement = GetAccessibility(listElement, root);

	// Access the Accessibility page
	GotoAccessibility(AccessibilityElement);

	// Memory release
	AccessibilityElement->Release();
	listElement->Release();
	paneElement->Release();
	pane->Release();
	settingsElement->Release();
	condition->Release();
	CoUninitialize();
}

void GotoAccessibility(IUIAutomationElement* AccessibilityElement)
{
	IUIAutomationInvokePattern* access = nullptr;
	AccessibilityElement->GetCurrentPattern(UIA_InvokePatternId, (IUnknown**)&access);
	if (!access)
	{
		throw std::runtime_error("Error getting access");
	}
	access->Invoke();

	access->Release();
}
