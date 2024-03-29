﻿#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

Loop
{
    If WinExist("TeamViewer Panel") or WinExist("Sponsored session")
    {
        Sleep, 2000
        WinClose, Sponsored session
	Sleep, 1000
	SetKeyDelay 30,50
	Send, {Alt down}{Tab}{Alt up}
    }
    Sleep, 2000
}
