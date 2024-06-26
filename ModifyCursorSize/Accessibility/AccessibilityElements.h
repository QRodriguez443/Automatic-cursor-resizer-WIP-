#pragma once
#ifndef ACCESSIBILITYELEMENTS_H
#define ACCESSIBILITYELEMENTS_H

#include <UIAutomation.h>

IUIAutomationElement* GetList(IUIAutomationElement* paneElement, IUIAutomation* root);
IUIAutomationElement* GetAccessibility(IUIAutomationElement* listElement, IUIAutomation* root);

#endif