#pragma once
#ifndef FIND_ACCESSIBILITY_H
#define FIND_ACCESSIBILITY_H

#include <UIAutomation.h>

struct AInitElements
{
	IUIAutomationElement* settingsElement;
	IUIAutomation* root;
};

void FindAccessibilityButton(IUIAutomationElement* settingsElement, IUIAutomation* root);

#endif