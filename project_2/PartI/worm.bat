@echo off

REM NOTE: To make this work, please replace "Mike" below with your user name

REM Copy and execute the worm 100 times
for /L %%i in (1, 1, 100) DO (
	REM Copy the worm!
	REM copy worm.bat c:\Users\franktosh

	REM Execute it!
	start c:\Users\franktosh\worm.bat

	REM Print a witty remark!
	echo "It's getting worm here...%%i"
)
