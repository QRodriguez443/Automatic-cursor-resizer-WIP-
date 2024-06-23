#include "ChangePointerSizeElements.h"
#include "CreateCondition.h"
#include <iostream>
#include <UIAutomation.h>
#include <thread>

void ChangePointerSize(IUIAutomationElement* sizeElement);
void GetCursorSize();
void OpenRegistryKey();
void CloseRegistryKey();

HKEY hKey = NULL;
HANDLE hEvent = NULL;
std::atomic_bool running(true);
std::atomic_int cursorSize(-1);

void FindChangePointerSize(IUIAutomationElement* settingsElement, IUIAutomation* root)
{
	IUIAutomationElement* groupElement = GetGroupElement(settingsElement, root);

	IUIAutomationElement* paneElement = GetPaneElement(groupElement, root);

	IUIAutomationElement* scElement = GetSizeColorElement(paneElement, root);

	IUIAutomationElement* sizeElement = GetSizeElement(scElement, root);

	ChangePointerSize(sizeElement);

	// Memory release
	sizeElement->Release();
	scElement->Release();
	paneElement->Release();
	groupElement->Release();
	settingsElement->Release();
	root->Release();
	CoUninitialize();
}

void ChangePointerSize(IUIAutomationElement* sizeElement)
{
	OpenRegistryKey();

	if (running)
	{

		std::thread monitorThread(GetCursorSize);

		IRangeValueProvider* pValuePattern = nullptr;
		while (running)
		{
			sizeElement->GetCurrentPattern(UIA_RangeValuePatternId, (IUnknown**)&pValuePattern);

			double checkValue = 1.0;
		    double currentValue;
			pValuePattern->get_Value(&currentValue);
			int currentSize = cursorSize.load(); // Read cursor size
			if (currentSize != -1) {
				std::cout << "Current cursor size: " << currentSize << std::endl;
			}

			bool looped = false;
			bool valueReset = false;

			if (currentSize == 32)
			{
				while (currentSize == 32)
				{
					
					pValuePattern->SetValue(4.0);
					
					currentSize = cursorSize.load();
					if (currentSize != -1) {
						std::cout << "Current cursor size: " << currentSize << std::endl;
					}
				}
			}
			else
			{
				while (currentSize != 32)
				{
					
					pValuePattern->SetValue(1.0);
					
					currentSize = cursorSize.load();
					if (currentSize != -1) {
						std::cout << "Current cursor size: " << currentSize << std::endl;
					}
					/* A bug in the windows UI sometimes causes the cursor size to be set to 1
					instead of the last set number (in this case: 4). So the value of the
					registry won't correlate with the UI value, so to fix this problem, we simply
					change the slider up then back down for the change to reflect in the registry */
					if (looped && !valueReset)
					{
						pValuePattern->SetValue(2.0);
						
						pValuePattern->SetValue(1.0);
						
						currentSize = cursorSize.load();
						if (currentSize != -1) {
							std::cout << "Current cursor size: " << currentSize << std::endl;
						}
						valueReset = true;
					}
					looped = true;
				}
			}

		    running = false;
			break;
		}
		CloseRegistryKey();
		monitorThread.join();
		std::cout << "Left Loop" << std::endl;
		pValuePattern->Release();
	}
}

void GetCursorSize() {
	while (running) {
		DWORD currentSize;
		DWORD dataSize = sizeof(DWORD);

		if (RegQueryValueExW(hKey, L"CursorBaseSize", NULL, NULL, reinterpret_cast<LPBYTE>(&currentSize), &dataSize) == ERROR_SUCCESS) {
			cursorSize = static_cast<int>(currentSize);
			RegNotifyChangeKeyValue(hKey, TRUE, REG_NOTIFY_CHANGE_LAST_SET, hEvent, TRUE);
			WaitForSingleObject(hEvent, INFINITE);
		}
		else {
			std::cout << "Failed to read cursor size from registry." << std::endl;
			running = false;
			break;
		}
	}
}

void OpenRegistryKey() {
	if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Control Panel\\Cursors", 0, KEY_READ, &hKey) != ERROR_SUCCESS) {
		std::cout << "Failed to open registry key." << std::endl;
	}

	hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
	if (hEvent == NULL) {
		std::cout << "Failed to create event." << std::endl;
	}
}

void CloseRegistryKey() {
	if (hKey != NULL) {
		RegCloseKey(hKey);
		hKey = NULL;
	}

	if (hEvent != NULL) {
		CloseHandle(hEvent);
		hEvent = NULL;
	}
}
