#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance

#Include seers_village.ahk

/*  Created by Brandon Horner 12/29/2020

    Driver file for Seer's Village agility course bot.
    Ctrl+g to reload the script
    Ctrl+r to run the script
*/

global runelite_window := "RuneLite - BinaryBilly"
global runelite_unlogged := "RuneLite"

global successful_runs := 0 

GroupAdd, active_windows, %runelite_window% ;create a group of windows
GroupAdd, active_windows, "RuneLite"


;Hotkey to reload the script.
+`::
{
    reload
    return
}

^1::
{   
    login()
    return
 }

;Main hotkey to run the script.
^`::
{
    MsgBox, starting bot, click continue
    GroupActivate, active_windows
    sleep_random(2000, 3000)
    main()
    return
}

main()
{
    If WinActive("ahk_group active_windows")
    {
        pink_tile := 0xFF00FF
        MouseMove, 0, 0
        check_logged_in()
        
        ;setup character
        setup()
        
        while (successful_runs <= 1000)
        {
            ; every 15 runs, check again if logged in.
            if (Mod(A_Index, 15) = 0)
                check_logged_in()
                
            ;after 20 runs; sleep every 10 runs for a random amount
            if (successful_runs >= 20 and Mod(successful_runs, 10) = 0)
            {
                ToolTip, sleeping 10-90 seconds, XTOOLTIP, YTOOLTIP, 1
                sleep_random(10000, 90000)
            }
            ToolTip, %successful_runs% successful runs completed!, XTOOLTIP, 775, 2
            
            ;click the bank wall
            click_obstacle("climb bank wall")
            zoom("in", 19)
            
            ;check for marks of grace and collect them every time there is an obstacle
            click_existing_marks()
            
            ;click to jump gap
            click_obstacle("jump gap 1")
            
            if(on_ground(pink_tile))
                continue
            
            click_existing_marks()
            
            ;click to cross rope
            click_obstacle("cross tightrope")
            
            if(on_ground(pink_tile))
                continue
            
            click_existing_marks()
            
            ;click to jump gap 
            click_obstacle("jump gap 2")

            if(on_ground(pink_tile))
                continue
                
            zoom("out", 7)
            
            ;check for marks
            click_existing_marks()
            
            ;click to jump gap
            click_obstacle("jump gap 3")
            
            if(on_ground(pink_tile))
                continue

            ;check for marks
            click_existing_marks()
            
            ;click to jump edge
            if (click_obstacle("jump edge"))
                successful_runs++
            
            zoom("out", 30)
            click_colored_world_tile(pink_tile)
        }
    }
    return
}