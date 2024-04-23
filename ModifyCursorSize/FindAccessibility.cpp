#include "AccessibilityElements.h"
#include "CreateCondition.h"
#include <iostream>
#include <UIAutomation.h>

// Find the accessibility element and access its page
void FindAccessibilityButton(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"ScrollViewer", UIA_ClassNamePropertyId);

	// Get child of settingsElement: pane
	IUIAutomationElementArray* pane;
	settingsElement->FindAll(TreeScope_Children, condition, &pane);
	if (!pane)
	{
		throw std::runtime_error("Error finding pane");
	}

	IUIAutomationElement* paneElement = GetPaneElement(pane);

	IUIAutomationElement* listElement = GetList(paneElement, root);

	IUIAutomationElement* AccessibilityElement = GetAccessibility(listElement, root);

	GotoAccessibility(AccessibilityElement);

	// Memory release
	AccessibilityElement->Release();
	listElement->Release();
	paneElement->Release();
	pane->Release();
	condition->Release();
	// settingsElement and root will be re-used
}

void GotoAccessibility(IUIAutomationElement* AccessibilityElement)
{
	IUIAutomationInvokePattern* access = nullptr;
	AccessibilityElement->GetCurrentPattern(UIA_InvokePatternId, (IUnknown**)&access);
	if (!access)
	{
		throw std::runtime_error("Error getting access");
	}
	access->Invoke(); // Press the button

	access->Release();
}