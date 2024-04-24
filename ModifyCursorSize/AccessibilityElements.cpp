#include "CreateCondition.h"
#include "RestartSettingsWindow.h"
#include <UIAutomation.h>
#include <iostream>

void StartNewInstance();

IUIAutomationElement* GetList(IUIAutomationElement* paneElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"PageGroupsListView", UIA_AutomationIdPropertyId);

	// Get list element
	IUIAutomationElement* listElement = nullptr;
	while (!listElement)
	{
		paneElement->FindFirst(TreeScope_Children, condition, &listElement);
		if (!listElement)
		{
			std::cerr << "Error finding list" << '\n';
			// Memory Release
			condition->Release();
			paneElement->Release();
			root->Release();
			CoUninitialize();

			RestartSettingsWindow();
			StartNewInstance();
		}
	}

	// Memory release
	condition->Release();

	return listElement;
}

IUIAutomationElement* GetAccessibility(IUIAutomationElement* listElement, IUIAutomation* root)
{
	IUIAutomationCondition* condition = CreateCondition(root, L"SettingsPageGroupEaseOfAccess", UIA_AutomationIdPropertyId);

	// Get accessibility element
	IUIAutomationElement* AccessibilityElement = nullptr;
	while (!AccessibilityElement)
	{
		listElement->FindFirst(TreeScope_Children, condition, &AccessibilityElement);
		if (!AccessibilityElement)
		{
			std::cerr << "Error finding Accessibility" << '\n';
			// Memory Release
			condition->Release();
			listElement->Release();
			root->Release();
			CoUninitialize();

			RestartSettingsWindow();
			StartNewInstance();
		}
	}

	// Memory release
	condition->Release();

	return AccessibilityElement;
}

void StartNewInstance()
{
	system("start ./x64/Debug/ModifyCursorSize.exe");
	Sleep(10);
	exit(1);
}
