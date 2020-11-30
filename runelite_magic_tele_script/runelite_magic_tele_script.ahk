#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

+`::
Random, runtime, 3000000, 4800000 ;between 50 mins and 80 mins (1.2hrs)
SetTimer, StopScript, %runtime%
Loop, 
{
    Random, current_sleep_fast, 450, 1000
    Random, current_sleep_slow, 900, 2000
    Random, loop_time1, 15, 50
    Random, loop_time2, 15, 35
    Random, afk_time, 5000, 100000
    IfWinActive, RuneLite - Jormb
    {
        ; start the quick looping
        Loop, %loop_time1%
        {
            Random, delay, 75, 200
            SetMouseDelay, %delay%
            Sleep, %current_sleep_fast%
            IfWinActive, RuneLite - Jormb
            {
                Click
            }
        }
        ; start the slow looping
        Loop, %loop_time2%
        {
            Random, delay, 75, 200
            SetMouseDelay, %delay%
            Sleep, %current_sleep_slow%
            IfWinActive, RuneLite - Jormb
            {
                Click
            }
        }
        Sleep, %afk_time%
    }
} 
return

^`::
    StopScript:
        MsgBox, stopping script!
reload
