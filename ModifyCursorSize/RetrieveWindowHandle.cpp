#include <windows.h>
#include <UIAutomation.h>
#include <iostream>

HWND GetSettingsChild(HWND returnedHwnd);
int PrimeInit(HWND settingsHwnd);

// Executes and retrieves Settings window handle, returns its child.
HWND GetSettingsHandle()
{
	//Check if Settings is already running
	HWND settingsHwnd = FindWindowW(L"ApplicationFrameWindow", L"Settings");

	/* Searching for handle is prone to a bug (retrieving non-existant handle), so check that
	   the element exists. */
	int settingsExists = PrimeInit(settingsHwnd);
	if (settingsHwnd && settingsExists)
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
			ShellExecuteW(nullptr, L"Open", L"ms-settings:", nullptr, nullptr, SW_NORMAL);

			Sleep(500); // Ensure process is fully initialized

			HWND settingsHwnd = FindWindowW(L"ApplicationFrameWindow", L"Settings");
			if (!settingsHwnd)
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
	bool errorThrown = false;
	for (int i = 0; i <= 5; i++) // Limit thrown errors
	{
		// Get the child of top-level Settings window
		HWND settingsChild = FindWindowExW(returnedHwnd, nullptr, L"Windows.UI.Core.CoreWindow", L"Settings");
		if (settingsChild)
		{
			if (errorThrown)
			{
				std::wcout << "Error resolved..." << std::endl;
			}
			std::wcout << "Child of Settings window: " << settingsChild << std::endl;
			return settingsChild;
		}
		else if (i == 5)
		{
			throw std::runtime_error("Too many errors occurred");
		}
		else
		{
			try
			{
				throw std::runtime_error("Could not find Settings window's child");
			}
			catch (const std::runtime_error& e)
			{
				errorThrown = true;
				std::cerr << e.what() << '\n';
			}
		}
	}
}

// Init UIAutomation and get settings' top window element from handle
int PrimeInit(HWND settingsHwnd)
{
	IUIAutomation* root = nullptr;
	CoInitialize(nullptr);
	HRESULT result = CoCreateInstance(__uuidof(CUIAutomation), nullptr, CLSCTX_INPROC_SERVER, __uuidof(IUIAutomation), (void**)&root);
	if (FAILED(result))
	{
		throw std::runtime_error("Error: Init failed");
	}

	IUIAutomationElement* settingsTopElement;
	root->ElementFromHandle(settingsHwnd, &settingsTopElement);
	if (settingsTopElement)
	{
		std::wcout << "Top Settings element exists: " << settingsTopElement << std::endl;

		// Memory release
		settingsTopElement->Release();
		root->Release();
		CoUninitialize();

		return 0;
	}
	// Memory release
	root->Release();
	CoUninitialize();

	return 1;
}