@echo off

set "folder=.venv"
set "pipPath=.\%folder%\Scripts\pip.exe"
set "libFolder=.\%folder%\Lib\site-packages"
set "pillow=PIL"
set "opencv=cv2"
set "promptKit=prompt_toolkit"

set show_message=0

if not exist "%folder%" (
    	echo Virtuelles Enviroment wurde nicht gefunden.
    	python -m venv "%folder%"
    	echo Neues Virtuelles Enviroment wurde erstellt.
	echo.
	echo Installing Pillow
	"%pipPath%" install Pillow==9.4.0
	echo Installing opencv
	"%pipPath%" install opencv-python==4.7.0.72
	echo Installing prompt_toolkit
	"%pipPath%" install prompt_toolkit==3.0.38
pause
) else (
    	echo Das Virtuelle Enviroment existiert bereits.
	if not exist "%libFolder%\%pillow%" (
	echo Installing Pillow
	"%pipPath%" install Pillow==9.4.0
	set %show_message% = 1
	) else (
	echo Pillow installed
	)
	if not exist "%libFolder%\%opencv%" (
	echo Installing opencv
	"%pipPath%" install opencv-python==4.7.0.72
	set %show_message% = 1
	) else (
	echo opencv installed
	)
	if not exist "%libFolder%\%promptKit%" (
	echo Installing prompt_toolkit
	"%pipPath%" install prompt_toolkit==3.0.38
	set %show_message% = 1
	) else (
	echo prompt_toolkit installed
	)

	if %show_message% == 1 (
	pause
	)
)

.\%folder%\Scripts\python.exe .\Video_zu_Text\Video_Processing.py