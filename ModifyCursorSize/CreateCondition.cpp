#include <iostream>
#include <UIAutomation.h>

// One function to create UIAutomation conditions for better readability
IUIAutomationCondition* CreateCondition(IUIAutomation* root, const wchar_t* wideStr, PROPERTYID UIA_Prop)
{
	VARIANT var;
	var.vt = VT_BSTR;
	var.bstrVal = SysAllocString(wideStr); // Defines property's name/value

	IUIAutomationCondition* condition;
	root->CreatePropertyCondition(UIA_Prop, var, &condition);
	if (!condition)
	{
		SysFreeString(var.bstrVal);
		throw std::runtime_error("Error creating condition");
	}
	SysFreeString(var.bstrVal);
	return condition;
}
