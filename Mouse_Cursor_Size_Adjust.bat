title Mouse_Cursor_Size_Adjust
@echo off

set targetProcess=
set timerActivated?=false
set Input=EnterInput.py
set InputLast=EnterInputEND.py

REM Start program with :MonitorTargetProgram section.
:Main
    call :MonitorTargetProgram


REM Detect if the task has ended
:Executor
    set targetEnd=false
:AltLoop
    tasklist | findstr /i %targetProcess% > nul
    if %errorlevel% neq 0 (
        REM If False, start separate program that sets cursor size back to default, else go into the input standby.
        set targetEnd=true
        start CursorSizeAdjustDefault.py
        timeout /t 3.5 /nobreak
        exit
    ) else (
        REM Start separate process that waits for targetProcess to end, restarts the loop when it has done so.
        start /b EnterInputEND.py
        set /p input=Waiting for program to end...
        goto :AltLoop 
    )

REM Detect if the program has started
:MonitorTargetProgram
    set foundTarget=false
:loop
    tasklist | findstr /i %targetProcess% > nul
    if %errorlevel% equ 0 (
        REM If True, goto the label
        set foundTarget=true
        goto :CreateCursor
    ) else (
        REM Open separate program that detects when targetProcess is found
        start /b EnterInput.py
        set /p input=Waiting for program to start...
        timeout /t 2 /nobreak
        goto :loop
    )

:CreateCursor
REM Search Registry for the default size of cursor, if the cursor size is default, 
REM then separate program launches to increase cursor size in control panel, and continues to next section. 
    reg query "HKCU\Control Panel\Cursors" /v CursorBaseSize /t REG_DWORD | find "0x20" && set "modificationAmount=true" || set "modificationAmount=false"
    if %errorlevel% neq 0 (
        exit /b
    ) else (
        start CursorSizeAdjust.py
        timeout /t 4 /nobreak
        exit /b
    )

REM Conditional determines if this section has already been executed, if true, then the "else" statement is ran
if "%timerActivated?%"=="false" (
    REM Failsafe in case the process is not already running, once process is detected, continues to go back to the :loop section.
    start /b EnterInput.py
    set /p input=Waiting for program to start...
) else (
    REM If this section was executed at least once, then wait 3 seconds and continue to the :Executor section.
    timeout /t 3 /nobreak
    goto :Executor
)

set timerActivated?=true
goto :loop