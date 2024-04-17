#include <UIAutomation.h>
#include <iostream>

IUIAutomationElement* GetPaneElement(IUIAutomationElementArray* pane)
{
	// Get the first element in the array.
	IUIAutomationElement* paneElement;
	pane->GetElement(0, &paneElement);

	// Get the name of the element.
	VARIANT name;
	paneElement->GetCurrentPropertyValue(UIA_ClassNamePropertyId, &name);
	std::wcout << "Child of settings element: " << name.bstrVal << std::endl;

	SysReleaseString(name.bstrVal);

	return paneElement;
}

IUIAutomationElement* GetList(IUIAutomationElement* paneElement, IUIAutomation* root)
{
	// Define property's name
	VARIANT pValue;
	pValue.vt = VT_BSTR;
	pValue.bstrVal = SysAllocString(L"PageGroupsListView");

	// Create condition
	IUIAutomationCondition* condition = nullptr;
	root->CreatePropertyCondition(UIA_AutomationIdPropertyId, pValue, &condition);

	// Get list element
	IUIAutomationElementArray* list;
	paneElement->FindAll(TreeScope_Children, condition, &list);
	if (!list)
	{
		SysFreeString(pValue.bstrVal);
		throw std::runtime_error("Error finding list");
	}
	SysFreeString(pValue.bstrVal);

	IUIAutomationElement* listElement;
	list->GetElement(0, &listElement);

	// Memory release
	condition->Release();

	return listElement;
}

IUIAutomationElement* GetAccessibility(IUIAutomationElement* listElement, IUIAutomation* root)
{
	// Define property's name
	VARIANT pValue;
	pValue.vt = VT_BSTR;
	pValue.bstrVal = SysAllocString(L"SettingsPageGroupEaseOfAccess");

	// Create condition
	IUIAutomationCondition* condition;
	root->CreatePropertyCondition(UIA_AutomationIdPropertyId, pValue, &condition);

	// Get accessibility element
	IUIAutomationElement* AccessibilityElement;
	listElement->FindFirst(TreeScope_Children, condition, &AccessibilityElement);
	if (!AccessibilityElement)
	{
		SysFreeString(pValue.bstrVal);
		throw std::runtime_error("Error finding Accessibility");
	}
	SysFreeString(pValue.bstrVal);

	// Memory release
	condition->Release();

	return AccessibilityElement;
}