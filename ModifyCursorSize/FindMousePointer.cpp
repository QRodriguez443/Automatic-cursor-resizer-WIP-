#include <iostream>
#include <UIAutomation.h>

void FindMousePointer(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	// Define the class name to search for
	VARIANT pClass;
	pClass.vt = VT_BSTR;
	pClass.bstrVal = SysAllocString(L"ListView");
	IUIAutomationCondition* condition;
	root->CreatePropertyCondition(UIA_ClassNamePropertyId, pClass, &condition);

	// Search children in settings element for the element with specified class name
	IUIAutomationElement* listItem;
	settingsElement->FindFirst(TreeScope_Children, condition, &listItem);
	if (!listItem)
	{
		SysFreeString(pClass.bstrVal);
		condition->Release();
		throw std::runtime_error("Error finding list element");
	}
	SysFreeString(pClass.bstrVal);
	condition->Release();
}