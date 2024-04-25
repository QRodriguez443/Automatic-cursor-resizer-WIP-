#pragma once
#ifndef CREATE_CONDITION_H
#define CREATE_CONDITION_H

#include <UIAutomation.h>

IUIAutomationCondition* CreateCondition(IUIAutomation* root, const wchar_t* wideStr, PROPERTYID UIA_Prop);

#endif
