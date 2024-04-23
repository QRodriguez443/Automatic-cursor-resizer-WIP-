#include "CreateCondition.h"
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
	IUIAutomationCondition* condition = CreateCondition(root, L"PageGroupsListView", UIA_AutomationIdPropertyId);

	// Get list element
	IUIAutomationElementArray* list;
	paneElement->FindAll(TreeScope_Children, condition, &list);
	if (!list)
	{
		throw std::runtime_error("Error finding list");
	}

	IUIAutomationElement* listElement;
	list->GetElement(0, &listElement);

	// Memory release
	condition->Release();

	return listElement;
}

IUIAutomationElement* GetAccessibility(IUIAutomationElement* listElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"SettingsPageGroupEaseOfAccess", UIA_AutomationIdPropertyId);

	// Get accessibility element
	IUIAutomationElement* AccessibilityElement;
	listElement->FindFirst(TreeScope_Children, condition, &AccessibilityElement);
	if (!AccessibilityElement)
	{
		throw std::runtime_error("Error finding Accessibility");
	}

	// Memory release
	condition->Release();

	return AccessibilityElement;
}