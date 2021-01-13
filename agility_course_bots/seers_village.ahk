#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%\..  ; Ensures a consistent starting directory.

#Include ..\utilities.ahk

/*  Must change your color scheme in 'Agility' app to the colors below. 
    Must add pink squares within view of the climb bank wall spot.
    If you have problems with the bot, try changing the following values to a new unique color.
    Change the color in the RuneLite default app 'Agility' and change the colors there as well.
*/ 
global obstacle_color := 0x2190E5    ;cyan/teal
global obstacle_alternate_color := 0x00FFFF    ;teal
global world_tile_color := 0xFF00FF ;pink

;constants
global TRIES := 5   ; how many tries you want the functions to run before giving up.
global XTOOLTIP := 1300, YTOOLTIP := 800


;clicks on a pixel of a certain color closest to the center of the screen. searches entire screen.
click_colored_world_tile(color_of_tile)
{   
    if (click_closest_pixel(color_of_tile, "mouseover"))
    {
        sleep_time_min := 8500
        sleep_time_max := 12000
        ToolTip, Clicking on the colored world tile. `r    (%sleep_time_min% - %sleep_time_max% second pause), XTOOLTIP, YTOOLTIP, 1
        Random, offset_x, -50, 70
        Random, offset_y, -50, 5
        MouseClick, left, offset_x, offset_y,,,, Relative
        sleep_random(sleep_time_min, sleep_time_max)
        return true
    }
    return false
}

/*
    Check for marks of grace and click them
*/
click_existing_marks()
{
    tries := 5
    mark_of_grace_color := 0x9A8713
    mark_of_grace_text := "image_library\agility_course\mark_of_grace_text.png"
    
    if (pixel_search_and_click(0, 0, A_ScreenWidth, A_ScreenHeight, obstacle_alternate_color))
    {
        while (tries > 0)
        {
            ToolTip, click_existing_marks():`r%tries% tries left. `rtrying to find the mark of grace color, XTOOLTIP, YTOOLTIP, 1
            sleep_time_min := 2000
            sleep_time_max := 3000
            Random, offset_x, -5, 5
            Random, offset_y,-5, 5
            if (pixel_search_and_click(0, 0, A_ScreenWidth - 355, A_ScreenHeight, mark_of_grace_color, "mouseover"))
            {
                sleep_random(50, 75)
                if (image_search_and_click(mark_of_grace_text, "top_left"))
                {
                    ToolTip, Clicking on the mark of grace! `rWaiting %sleep_time_min%ms to %sleep_time_max%ms, XTOOLTIP, YTOOLTIP, 1
                    ctrl_click()
                    sleep_random(sleep_time_min, sleep_time_max)
                    return true
                }
            }
            tries --
        }
    }
    return false
}

/*
    If user has fallen to the ground, this should click on user placed tiles that are within 
    sight of the bank wall obstacle.
    Parameter
    world_tile_color - the color of the user placed tiles (should match your in game tiles)
*/
on_ground(world_tile_color)
{
    if(pixel_search_and_click(0, 0, A_ScreenWidth - 355, A_ScreenHeight, world_tile_color, "left"))
    {
        ToolTip, On the ground - zooming out - starting over, XTOOLTIP, YTOOLTIP, 1
        zoom("out")
        return true
    }
    return false
}

/* 
   Depending on the obstacle that we are at, we have different areas to search/click on,
   different sleep times, and different text to be looking for during verification.
   Parameter
   obstacle - the current obstacle should input in the correct order as they appear
    (the obstacles of seers village are seen below in the switch cases).
   
*/ 
click_obstacle(obstacle)
{
    tries := 5
    
    while (tries > 0)
    {
        IfWinActive, %runelite_window%
        {
            switch obstacle 
            {   
                case "climb_bank_wall":
                    x1 := 800, y1 := 75, x2 := 1375, y2 := 600
                    Random, offset_x, 5, 12
                    Random, offset_y, 5, 12
                    sleep_time_min = 9500  ;9.5 seconds
                    sleep_time_max = 12500
                    in_game_verification_text1 := "image_library\agility_course\climb_bank_text1.png"
                    in_game_verification_text2 := "image_library\agility_course\climb_bank_text2.png"
                    message := "climbing bank wall"

                case "jump_gap_1":
                    x1 := 100, y1 := 100, x2 := 825, y2 := 825
                    Random, offset_x, -5, -3
                    Random, offset_y, -5, 50
                    sleep_time_min = 6500 
                    sleep_time_max = 8500
                    in_game_verification_text1 := "image_library\agility_course\jump_gap_text1.png"
                    in_game_verification_text2 := "image_library\agility_course\jump_gap_text2.png"
                    message := "jumping first gap"
                    
                case "cross_tightrope":
                    x1 := 660, y1 := 575, x2 := 1375, y2 := 1025
                    Random, offset_x, -30, 30
                    Random, offset_y, 5, 60
                    sleep_time_min = 8500
                    sleep_time_max = 9000
                    in_game_verification_text1 := "image_library\agility_course\cross_tightrope_text1.png"
                    in_game_verification_text2 := "image_library\agility_course\cross_tightrope_text2.png"
                    message := "crossing tightrope"
                    
                case "jump_gap_2":
                    x1 := 555, y1 := 550, x2 := 1370, y2 := 990
                    Random, offset_x, -20, 200
                    Random, offset_y, 5, 60
                    sleep_time_min = 4500
                    sleep_time_max = 6500
                    in_game_verification_text1 := "image_library\agility_course\jump_gap_text1.png"
                    in_game_verification_text2 := "image_library\agility_course\jump_gap_text2.png"
                    message := "jumping second gap"
                    
                case "jump_gap_3":
                    x1 := 50, y1 := 610, x2 := 1165, y2 := 930
                    Random, offset_x, -30, 100
                    Random, offset_y, 5, 60
                    sleep_time_min = 5500
                    sleep_time_max = 7500
                    in_game_verification_text1 := "image_library\agility_course\jump_gap_text1.png"
                    in_game_verification_text2 := "image_library\agility_course\jump_gap_text2.png"
                    message := "jumping third gap"
                    
                case "jump_edge":
                    x1 := 960, y1 := 550, x2 := 1020, y2 := 800
                    Random, offset_x, 10, 75
                    Random, offset_y, 5, 300
                    sleep_time_min = 200
                    sleep_time_max = 300
                    in_game_verification_text1 := "image_library\agility_course\jump_edge_text1.png"
                    in_game_verification_text2 := "image_library\agility_course\jump_edge_text2.png"
                    message := "jumping off edge"
            } ;end switch
            
            ToolTip, Current obstacle is: %obstacle% `r%tries% tries left`rtrying to find the obstacle colors, XTOOLTIP, YTOOLTIP, 1
            
            ;search both obstacle colors, sometimes an obstacle will be the alternate color, and you must travel to the mark of grace at another obstacle.
            if (pixel_search_and_click(x1, y1, x2, y2, obstacle_color, "mouseover", offset_x, offset_y) 
              or pixel_search_and_click(x1, y1, x2, y2, obstacle_alternate_color, "mouseover", offset_x, offset_y))
            {
                if (image_search_and_click(in_game_verification_text1, "top_left") 
                  && image_search_and_click(in_game_verification_text2, "top_left"))
                {
                    ToolTip, %message%`rWaiting %sleep_time_min%ms to %sleep_time_max%ms, XTOOLTIP, YTOOLTIP, 1
                    ctrl_click()
                    sleep_random(sleep_time_min, sleep_time_max)
                    return true
                }
            }
            tries--
            ToolTip, tries = %tries%... failed to find the colorz, XTOOLTIP, YTOOLTIP, 1
        } ;end IfWinActive
    } ;end while
    
    return false        
}

;presses down ctrl just before clicking and then lets up off of the ctrl key.
ctrl_click()
{
    Send, {Ctrl down}
    sleep_random(30, 60)
    Click
    sleep_random(30, 60)
    Send, {Ctrl up}
    return
}