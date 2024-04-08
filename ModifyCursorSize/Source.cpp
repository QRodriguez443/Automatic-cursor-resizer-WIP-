#define OEMRESOURCE
#include <windows.h>
#include <UIAutomation.h>
#include <iostream>
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "oleaut32.lib")
#pragma comment(lib, "uiautomationcore.lib")

HWND getSettingsHandle() // Executes and retrieves Settings window handle
{
	bool errorThrown = false;
	for (int i = 0; i <= 5; i++) // Limit thrown errors
	{
		ShellExecuteW(NULL, L"Open", L"ms-settings:", NULL, NULL, SW_NORMAL);

		HWND settingsHwnd = FindWindowW(L"ApplicationFrameWindow", L"Settings");
		if (settingsHwnd == NULL)
		{
			std::cerr << "Error: Window not found, attempting to resolve..." << std::endl;
			errorThrown = true;
		}
		if (i == 5)
		{
			try {
			    throw std::runtime_error("Too many errors occurred");
			}
			catch (const std::runtime_error& e) {
				// Handle the exception
				std::cerr << "Caught a runtime error: " << e.what() << '\n';
			}
		}
		else if ( errorThrown && settingsHwnd)
		{
			std::cout << "Error resolved!" << " Settings handle retrieved" << std::endl;
			return settingsHwnd;
		}
		else if (settingsHwnd)
		{
			std::cout << "Settings handle retrieved" << std::endl;
			return settingsHwnd;
		}
	}
}

int main() 
{
	/* Open the settings window, navigate to accessibility, Mouse pointer, and focus into pointer
	size slider */

	// Get Setting's top window element
	HWND settingsHwnd = getSettingsHandle();

}
