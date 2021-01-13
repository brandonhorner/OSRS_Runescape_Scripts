#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance

#Include seers_village.ahk

/*Created by Brandon Horner 12/29/2020

Driver file for Seer's Village agility course bot.
Ctrl+g to reload the script
Ctrl+r to run the script
*/
global runelite_window := "RuneLite - BinaryBilly"

;Hotkey to reload the script.
Home::
{
    reload
    return
}

;Main hotkey to run the script.
End::
    MsgBox, starting bot, click continue
    WinActivate, %runelite_window%
    sleep_random(2000, 3000)
    main()
    return

main()
{
    IfWinActive, %runelite_window%
    {
        successful_runs := 0
        pink_tile := 0xFF00FF
        
        ;setup character
        setup()
        
        while (successful_runs < 500)
        {
            if(successful_runs >= 20 and Mod(successful_runs, 10) = 0)
            {
                ToolTip, sleeping 10-30 seconds, XTOOLTIP, YTOOLTIP, 1
                sleep_random(10000, 30000)
            }
            ToolTip, %successful_runs% successful runs completed!, XTOOLTIP, 775, 2
            
            ;click the bank wall
            click_obstacle("climb_bank_wall")
            zoom("in", 30)
            zoom("out", 11)
            ;check for marks of grace and collect them
            click_existing_marks()
            
            ;click to jump gap
            click_obstacle("jump_gap_1")
            
            if(on_ground(pink_tile))
                continue
            
            ;check for marks
            click_existing_marks()
            
            ;click to cross rope
            click_obstacle("cross_tightrope")
            
            if(on_ground(pink_tile))
                continue
            
            ;check for marks
            click_existing_marks()
            
            ;click to jump gap 
            click_obstacle("jump_gap_2")

            if(on_ground(pink_tile))
                continue
                
            zoom("out", 7)
            
            ;check for marks
            click_existing_marks()
            
            ;click to jump gap
            click_obstacle("jump_gap_3")
            
            if(on_ground(pink_tile))
                continue

            ;check for marks
            click_existing_marks()
            
            ;click to jump edge
            if (click_obstacle("jump_edge"))
                successful_runs++
            
            zoom("out", 30)
            click_colored_world_tile(pink_tile)
        }
    }
    return
}