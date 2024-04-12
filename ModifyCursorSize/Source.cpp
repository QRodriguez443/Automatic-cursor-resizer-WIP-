#include "RetrieveWindowHandle.h"
#include <UIAutomation.h>
#include <iostream>
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "oleaut32.lib")
#pragma comment(lib, "uiautomationcore.lib")

// Initialize UIAutomation and retrieve settings element
IUIAutomationElement* InitUIA(HWND settingsHwnd)
{
	IUIAutomation* root = nullptr;
	CoInitialize(NULL);
	CoCreateInstance(__uuidof(CUIAutomation), NULL, CLSCTX_INPROC_SERVER, __uuidof(IUIAutomation), (void**)&root);

	IUIAutomationElement* settingsElement;
	root->ElementFromHandle(settingsHwnd, &settingsElement);
	if (!settingsElement)
	{
		std::cerr << "Error getting settingsElement" << '\n';
	}
	return settingsElement;
}

int main() 
{
	/* Open the settings window, navigate to accessibility, Mouse pointer, and focus into pointer
	size slider */

	// Get Setting's bottom window element
	HWND settingsHwnd = GetSettingsHandle();
	IUIAutomationElement* settingsElement = InitUIA(settingsHwnd);
	
	// Get "pane" element
}
