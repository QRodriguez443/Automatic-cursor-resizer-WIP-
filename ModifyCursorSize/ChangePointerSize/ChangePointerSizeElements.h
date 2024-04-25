#pragma once
#ifndef CHANGE_POINTER_SIZE_ELEMENTS_H
#define CHANGE_POINTER_SIZE_ELEMENTS_H

#include <UIAutomation.h>

IUIAutomationElement* GetGroupElement(IUIAutomationElement* settingsElement, IUIAutomation* root);
IUIAutomationElement* GetPaneElement(IUIAutomationElement* settingsElement, IUIAutomation* root);
IUIAutomationElement* GetSizeColorElement(IUIAutomationElement* settingsElement, IUIAutomation* root);
IUIAutomationElement* GetSizeElement(IUIAutomationElement* settingsElement, IUIAutomation* root);

#endif
