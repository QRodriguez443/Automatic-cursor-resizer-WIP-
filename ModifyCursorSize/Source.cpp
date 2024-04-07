#define OEMRESOURCE
#include <iostream>
#include <windows.h>
#include <UIAutomation.h>
#include <UIAutomationCore.h>

int getSettingsHandle()
{
	bool errorThrown = false;
	for (int i = 0; i <= 5; i++) // Limit thrown errors
	{
		HWND settingsHwnd = FindWindowW(L"ApplicationFrameWindow", L"Settings");
		if (!settingsHwnd)
		{
			std::cerr << "Error: Window not found, attempting to resolve..." << std::endl;
			ShellExecuteW(NULL, L"Open", L"ms-settings:", NULL, NULL, SW_NORMAL);
			errorThrown = true;
		}
		if (i == 4)
		{
			return 1;
		}
		else if ( errorThrown && settingsHwnd)
		{
			std::cout << "Error resolved!" << std::endl;
			break; // If error resolves, continue with rest of code
		}
		else if (settingsHwnd)
		{
			std::cout << "Settings handle retrieved" << std::endl;
			break; // If no error thrown, continue with rest of code
		}
	}
	return 0; // Exit function
}

int main() 
{
	/* Open the settings window, navigate to accessibility, Mouse pointer, and focus into pointer
	size slider */
	ShellExecuteW(NULL, L"Open", L"ms-settings:", NULL, NULL, SW_NORMAL);

	// Get Setting's top window element
	getSettingsHandle();

	std::cout << "Continuing with code...";

	Sleep(5000);
}