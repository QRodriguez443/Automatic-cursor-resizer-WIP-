#include <iostream>
#include <UIAutomation.h>

IUIAutomationElement* GetList(IUIAutomationElement* paneElement, IUIAutomation* root);

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
		throw std::runtime_error("Error finding pane");
	}
	// Get the first element in the array.
	IUIAutomationElement* paneElement;
	pane->GetElement(0, &paneElement);

	// Get the name of the element.
	VARIANT name;
	paneElement->GetCurrentPropertyValue(UIA_ClassNamePropertyId, &name);
	std::wcout << "Child of settings element: " << name.bstrVal << std::endl;

	// Get pane's child: list
	IUIAutomationElement* listElement = GetList(paneElement, root);
}

IUIAutomationElement* GetList(IUIAutomationElement* paneElement, IUIAutomation* root)
{
	// Define property's name
	VARIANT pAID;
	pAID.vt = VT_BSTR;
	pAID.bstrVal = SysAllocString(L"PageGroupsListView");

	// Create condition
	IUIAutomationCondition* condition = nullptr;
	root->CreatePropertyCondition(UIA_AutomationIdPropertyId, pAID, &condition);

	IUIAutomationElementArray* list;
	paneElement->FindAll(TreeScope_Children, condition, &list);
	if (!list)
	{
		SysFreeString(pAID.bstrVal);
		throw std::runtime_error("Error finding list");
	}
	SysFreeString(pAID.bstrVal);

	IUIAutomationElement* listElement;
	list->GetElement(0, &listElement);
	
	return listElement;
}
