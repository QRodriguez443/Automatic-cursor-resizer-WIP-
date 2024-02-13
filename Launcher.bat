@echo off

start "" "F:\SteamLibrary\steamapps\common\Star Wars - The Old Republic\Launcher.exe"
timeout /t 3 /nobreak > nul
start /B python "F:\SteamLibrary\steamapps\common\Star Wars - The Old Republic\Launcher_check.py"

set "targetProcess=swtor.exe"
 
:SetFalse
    set target=false

    :LOOP
    REM Waits until the executable is running to execute Mouse_Cursor_Size_Adjust.bat
        timeout /t 5 /nobreak > nul
        tasklist | findstr /i "%targetProcess%" >nul

        if %errorlevel% neq 0 (
            REM If false
            set target=true 
            goto :LOOP
            
        ) else ( start /b "" "F:\SteamLibrary\steamapps\common\Star Wars - The Old Republic\Mouse_Cursor_Size_Adjust.bat" 
                 exit )

:Main
    call :SetFalse