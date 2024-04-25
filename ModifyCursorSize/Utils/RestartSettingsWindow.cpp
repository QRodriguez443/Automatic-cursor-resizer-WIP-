#include <iostream>
#include <windows.h>
#include "RetrieveWindowHandle.h"

/* If an error occurs related to finding a window element for main page, most likely settings 
are open (on the wrong page) before running the code. */
void RestartSettingsWindow()
{
	HWND settingsHwnd = GetSettingsHandle();

	SendMessageW(settingsHwnd, WM_CLOSE, NULL, NULL);
	Sleep(500);
	ShellExecuteW(nullptr, L"Open", L"ms-settings:", nullptr, nullptr, SW_NORMAL);
}
