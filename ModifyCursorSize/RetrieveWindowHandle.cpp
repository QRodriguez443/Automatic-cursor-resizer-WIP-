#include <windows.h>
#include <iostream>

HWND GetSettingsHandle() // Executes and retrieves Settings window handle
{
	Sleep(500); // Hopefully solves error with settingsHwnd retrieving non-existent handle

	//Check if Settings is already running
	HWND settingsHwnd = FindWindowW(L"ApplicationFrameWindow", L"Settings");
	if (settingsHwnd != NULL)
	{
		std::cout << "Window already open, Settings handle retrieved:"<< settingsHwnd << std::endl;
		return settingsHwnd;
	}
	else
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
			else if (errorThrown && settingsHwnd)
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
}

void GetSettingsChild(HWND returnedHwnd) // Call this function within the one above
{
	FindWindowExW(returnedHwnd, NULL, L"Windows.UI.Core.CoreWindow", L"Settings");
}