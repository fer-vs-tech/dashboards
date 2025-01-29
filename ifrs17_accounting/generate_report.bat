@REM Usage:
@REM Sample: .\generate_report.bat <dashboard_path> <wvr_path> <record_type> <output_path> <reversed_flag>
@REM .\generate_report.bat C:\Program Files\RNA Analytics\Dashboard C:/temp/Profit_Center_688.wvr primary C:/temp/dashboard/Deves/output False

@REM Set the parameters
@echo off
set dashboard_path=%1
set wvr=%2
set type=%3
set output_path=%4
set reversed=%5

@REM Print the parameters
echo Dashboard path: %dashboard_path%
echo WVR path: %wvr%
echo Record type: %type%
echo Output path: %output_path%
echo Reversed: %reversed%

@REM Change the directory to the dashboard path
cd %dashboard_path% || exit /b %ERRORLEVEL%

@REM Run the command to generate the report
echo Generating report...
if %reversed% == False (
    dashboard --generate-report -w %wvr% -t %type% --no-reversed -o %output_path%
    if ERRORLEVEL 1 (
        echo "An error occurred while generating the report."
        exit /b %ERRORLEVEL%
    )
) else (
    dashboard --generate-report -w %wvr% -t %type% --reversed -o %output_path%
    if ERRORLEVEL 1 (
        echo "An error occurred while generating the report."
        exit /b %ERRORLEVEL%
    )
)

echo Report generated successfully!