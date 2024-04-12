#include <windows.h>
#include <iostream>

HWND GetSettingsChild(HWND returnedHwnd);

HWND GetSettingsHandle() // Executes and retrieves Settings window handle, returns its child.
{
	Sleep(500); // Hopefully solves error with settingsHwnd retrieving non-existent handle

	//Check if Settings is already running
	HWND settingsHwnd = FindWindowW(L"ApplicationFrameWindow", L"Settings");
	if (settingsHwnd != NULL)
	{
		std::cout << "Window already open, Settings handle retrieved:"<< settingsHwnd << std::endl;
		HWND settingsChild = GetSettingsChild(settingsHwnd);
		return settingsChild;
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
				try 
				{
					throw std::runtime_error("Too many errors occurred");
				}
				catch (const std::runtime_error& e) 
				{
					// Handle the exception
					std::cerr << e.what() << '\n';
				}
			}
			else if (errorThrown && settingsHwnd)
			{
				std::cout << "Error resolved!" << " Settings handle retrieved" << std::endl;
				HWND settingsChild = GetSettingsChild(settingsHwnd);
				return settingsChild;
			}
			else if (settingsHwnd)
			{
				std::cout << "Settings handle retrieved" << std::endl;
				HWND settingsChild = GetSettingsChild(settingsHwnd);
				return settingsChild;
			}
		}
	}
}

HWND GetSettingsChild(HWND returnedHwnd) // Call this function within the one above
{
	// Get the child of top-level Settings window
	HWND settingsChild = FindWindowExW(returnedHwnd, NULL, L"Windows.UI.Core.CoreWindow", L"Settings");
	if (settingsChild != NULL)
	{
		std::wcout << "Child of Settings window: " << settingsChild << std::endl;
		return settingsChild;
	}
	else
	{
		try
		{
			throw std::runtime_error("Could not find Settings window's child");
		}
		catch (const std::runtime_error& e)
		{
			std::cerr << e.what() << '\n';
		}
	}
}
