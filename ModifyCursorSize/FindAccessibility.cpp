#include <iostream>
#include <UIAutomation.h>

void FindAccessibilityButton(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	// Define property's name
	VARIANT pValue;
	pValue.vt = VT_BSTR;
	pValue.bstrVal = SysAllocString(L"ScrollViewer");

	// Create condition
	IUIAutomationCondition* condition = nullptr;
	root->CreatePropertyCondition(UIA_ClassNamePropertyId, pValue, &condition);

	IUIAutomationElementArray* pane;
	settingsElement->FindAll(TreeScope_Children, condition, &pane);
}