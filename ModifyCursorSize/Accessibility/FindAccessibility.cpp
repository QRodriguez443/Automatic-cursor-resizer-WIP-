#include "AccessibilityElements.h"
#include "CreateCondition.h"
#include "RestartSettingsWindow.h"
#include <iostream>
#include <UIAutomation.h>

void GotoAccessibility(IUIAutomationElement* AccessibilityElement);

// Find the accessibility element and access its page
void FindAccessibilityButton(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"ScrollViewer", UIA_ClassNamePropertyId);

	// Get child of settingsElement: pane
	IUIAutomationElement* paneElement = nullptr;
	while (!paneElement)
	{
		settingsElement->FindFirst(TreeScope_Children, condition, &paneElement);
		if (!paneElement)
		{
			std::cerr << "Error finding pane" << '\n';
			// Memory Release
			condition->Release();
			settingsElement->Release();
			root->Release();
			CoUninitialize();

			RestartSettingsWindow();
			system("start ./x64/Debug/ModifyCursorSize.exe");
			Sleep(10);
			exit(1);
		}
	}

	IUIAutomationElement* listElement = GetList(paneElement, root);

	IUIAutomationElement* AccessibilityElement = GetAccessibility(listElement, root);

	GotoAccessibility(AccessibilityElement);

	// Memory release
	AccessibilityElement->Release();
	listElement->Release();
	paneElement->Release();
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