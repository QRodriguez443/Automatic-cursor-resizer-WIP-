#define OEMRESOURCE
#include "RetrieveWindowHandle.h"
#include <UIAutomation.h>
#include <iostream>
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "oleaut32.lib")
#pragma comment(lib, "uiautomationcore.lib")

int main() 
{
	/* Open the settings window, navigate to accessibility, Mouse pointer, and focus into pointer
	size slider */

	// Get Setting's top window element
	HWND settingsHwnd = getSettingsHandle();

}