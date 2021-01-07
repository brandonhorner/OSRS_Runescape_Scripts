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

/*
^`::
    cross_tightrope_text := "image_library\agility_course\cross_tightrope_text.png"
    jump_edge_text := "image_library\agility_course\jump_edge_text.png"
    jump_gap_text := "image_library\agility_course\jump_gap_text.png"
    climb_bank_text := "image_library\agility_course\climb_bank_text.png"
    verification_texts := [(climb_bank_text), (jump_gap_text), (cross_tightrope_text), (jump_edge_text)]
    for index, text in verification_texts
    {
        s .= index "=" text "`n"
        MsgBox % s
    }
    return
*/

;Hotkey to reload the script.
^g::
{
    reload
    return
}
/*
^`::
{
    PixelSearch, Px, Py, 0, 50, 1645, 1100, 0x00FF00, 0, RGB fast
    if(Px)
        ToolTip, %Px%x%Py%, 800, 800, 13
    if(!click_closest_pixel(0x00FF00, "mouseover"))
    {
        ToolTip, failed ya boy, 500, 500, 1
    }
    return
}
*/

^,::
    zoom_in(19)
    return
    
^`::
{
    click_obstacle("jump_edge")
    return
}
;Main hotkey to run the script.
^r::
{
    IfWinActive, %runelite_window%
    {
        loop_count := 500
        pink_tile := 0xFF00FF
        
        ;setup character
        setup()
        
        while (loop_count > 0)
        {
            ToolTip, %loop_count% runs left., XTOOLTIP, 475, 2
            
            ;click the bank wall
            click_obstacle("climb_bank_wall")
            zoom_in(19)

            ;check for marks of grace and collect them
            click_existing_marks()
            
            ;click to jump gap
            click_obstacle("jump_gap_1")
            
            if(on_ground(pink_tile))
                goto LoopEnd
            
            ;check for marks
            click_existing_marks()
            
            ;click to cross rope
            click_obstacle("cross_tightrope")
            
            if(on_ground(pink_tile))
                goto LoopEnd
            
            ;check for marks
            click_existing_marks()
            
            ;click to jump gap 
            click_obstacle("jump_gap_2")

            if(on_ground(pink_tile))
                goto LoopEnd

            ;check for marks
            click_existing_marks()
            
            ;click to jump gap
            click_obstacle("jump_gap_3")
            
            if(on_ground(pink_tile))
                goto LoopEnd

            ;check for marks
            click_existing_marks()
            
            ;click to jump edge
            click_obstacle("jump_edge")
            zoom_out()
            
            click_colored_world_tile(pink_tile)
        LoopEnd:
            loop_count --
        }
    }
    return
}