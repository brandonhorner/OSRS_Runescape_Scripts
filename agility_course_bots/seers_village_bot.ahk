#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#Include seers_village.ahk
/*Created by Brandon Horner 12/29/2020

Driver file for Seer's Village agility course bot.
Ctrl+g to reload the script
Ctrl+r to run the script
*/
global runelite_window := "RuneLite - BinaryBilly"

global mark_of_grace_color := "0x9A8713"
global red_color := "0xFF0000"

;Hotkey to reload the script.
^g::
    reload
    return

^`::
    click_bank_wall()
    return
;Main hotkey to run the script.
^r::
IfWinActive, %runelite_window%
{
    ;setup character
    setup()
    
    ;click the bank wall
    click_bank_wall()
    
    zoom_in(25)
  
    ;check for marks of grace and collect them
    if(pixel_search_and_click(0, 0, A_ScreenWidth, A_ScreenHeight, red_color))
    
    click_existing_marks()
    
    ;click to jump gap
    click_jump_gap()
    
    ;check for marks
    click_existing_marks()
    
    ;click to cross rope
    click_cross_rope()
    
    ;check for marks
    click_existing_marks()
    
    ;click to jump gap
    click_jump_gap()
    
    ;check for marks
    click_existing_marks()
    
    ;click to jump gap
    click_jump_gap()
    
    ;check for marks
    click_existing_marks()
    
    ;click to jump edge
    click_jump_edge()
    
    
    ;if anything fails too many times, or we are finished click teal world square
    ;sleep
    ;end loop
}
return