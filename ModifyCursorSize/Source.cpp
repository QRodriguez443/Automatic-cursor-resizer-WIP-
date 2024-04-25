#include "RetrieveWindowHandle.h"
#include "FindAccessibility.h"
#include "FindMousePointer.h"
#include "FindChangePointerSize.h"
#include <UIAutomation.h>
#include <iostream>

AInitElements InitUIA(HWND settingsHwnd);

int main()
{
	/* Open the settings window, navigate to accessibility, Mouse pointer, and focus into pointer
	size slider */

	// Get Setting's bottom window element
	HWND settingsHwnd = GetSettingsHandle();
	AInitElements AIE = InitUIA(settingsHwnd);
	
	// 1.
	FindAccessibilityButton(AIE.settingsElement, AIE.root);
	// 2.
	FindMousePointer(AIE.settingsElement, AIE.root);
	// 3.
	FindChangePointerSize(AIE.settingsElement, AIE.root);

}

// Initialize UIAutomation and retrieve settings element
AInitElements InitUIA(HWND settingsHwnd)
{
	IUIAutomation* root = nullptr;
	CoInitialize(nullptr);
	HRESULT result = CoCreateInstance(__uuidof(CUIAutomation), nullptr, CLSCTX_INPROC_SERVER, __uuidof(IUIAutomation), (void**)&root);
	if (FAILED(result))
	{
		throw std::runtime_error("Error: Init failed");
	}

	bool errorThrown = false;
	IUIAutomationElement* settingsElement = nullptr;

	for (int i = 0; i <= 5; i++) // Limit thrown errors
	{
		root->ElementFromHandle(settingsHwnd, &settingsElement);
		if (!settingsElement)
		{
			std::cerr << "Error getting settingsElement" << '\n';
			errorThrown = true;
		}
		else if (i == 5)
		{
			throw std::runtime_error("Too many errors occurred");
		}
		else
		{
			if (errorThrown)
			{
				std::wcout << "Error resolved..." << std::endl;
			}
			std::wcout << "Bottom settings element found: " << settingsElement << std::endl;
			break;
		}
	}

	AInitElements AIE;
	AIE.settingsElement = settingsElement;
	AIE.root = root;

	return AIE;
}
