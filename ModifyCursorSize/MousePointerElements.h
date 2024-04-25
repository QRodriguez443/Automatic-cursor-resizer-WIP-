#pragma once
#ifndef MOUSE_POINTER_ELEMENTS_H
#define MOUSE_POINTER_ELEMENTS_H

#include <UIAutomation.h>

IUIAutomationElement* GetVisionElement(IUIAutomationElement* listItem, IUIAutomation* root);
IUIAutomationElement* GetMousePointerElement(IUIAutomationElement* visionElement, IUIAutomation* root);

#endif