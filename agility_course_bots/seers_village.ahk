#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%\..  ; Ensures a consistent starting directory.

#Include ..\utilities.ahk

;constants
global TRIES := 5

;click the bank wall
click_bank_wall()
{
    green = 0x00FF4D
    mining_text := "image_library\mining_text.bmp"

    tries := TRIES
    while (tries > 0)
    {
        if (pixel_search_and_click(424, 35, 1628, 866, green, "mouseover"))
        {
            if(image_search_and_click(mining_text, "top_left"))
            {
                Send, {Ctrl down}
                sleep_random(100,200)
                Click
                sleep_random(100,200)
                Send, {Ctrl up}
            }
            else
            {
                sleep_random(500, 1000)
            }
        }
    }
    return true
}

;check for marks of grace and collect them
click_existing_marks()
{
    return true
}

;click on obstacle to jump the gap
click_jump_gap()
{
    return true
}

;click on the rope obstacle to cross it
click_cross_rope()
{
    return true
}

click_jump_edge()
{
    return true
}

