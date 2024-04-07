#define OEMRESOURCE
#include <iostream>
#include <windows.h>
#include <UIAutomation.h>


int main() {
	ShellExecuteW(NULL, L"Open", L"ms-settings", NULL, NULL, SW_NORMAL);
}