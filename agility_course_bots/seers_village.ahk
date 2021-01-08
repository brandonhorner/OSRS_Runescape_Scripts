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
global XTOOLTIP := 500, YTOOLTIP := 500


;clicks on a pixel of a certain color closest to the center of the screen. searches entire screen.
click_colored_world_tile(color_of_tile)
{
    if (click_closest_pixel(color_of_tile, "left"))
    {
        ToolTip, Clicking on the colored world tile. `r    (8.5 - 12 second pause), XTOOLTIP, YTOOLTIP, 1
        sleep_random(8500, 12000)
        return true
    }
    return false
}

;check for marks of grace and collect them
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
        ;TODO EDIT OFFSET FOR MARK OF GRACE
            Random, offset_x, -5, 5
            Random, offset_y,-5, 5
            if (pixel_search_and_click(0, 0, A_ScreenWidth - 200, A_ScreenHeight, mark_of_grace_color, "mouseover"))
            {
                if (image_search_and_click(mark_of_grace_text, "top_left"))
                {
                    ToolTip, Clicking on the mark of grace! `r      (5-8 second pause), XTOOLTIP, YTOOLTIP, 1
                    ctrl_click_in_place()
                    sleep_random(5000, 8000)
                    return true
                }
            }
            tries --
        }
    }
    return false
}

on_ground(world_tile_color)
{
    if(pixel_search_and_click(0, 0, A_ScreenWidth, A_ScreenHeight, world_tile_color, "left"))
    {
        ToolTip, on the ground - zooming out - starting over`r      (5-8 second pause), XTOOLTIP, YTOOLTIP, 1
        zoom_out()
        return true
    }
    return false
}


click_obstacle(obstacle)
{
    tries := 5
    
    while (tries > 0)
    {
        switch obstacle     ;based on the obstacle we have different areas to
        {                   ;   randomize our clicks within
            case "climb_bank_wall":
                x1 := 1000, y1 := 75, x2 := 1375, y2 := 750
                Random, offset_x, 2, 20
                Random, offset_y, 2, 20
                sleep_time_min = 9500 ;8 seconds
                sleep_time_max = 12500
                in_game_verification_text := "image_library\agility_course\climb_bank_text.png"
                message := "climbing bank wall"

            case "jump_gap_1":
                x1 := 160, y1 := 100, x2 := 550, y2 := 400
                Random, offset_x, -10, -3
                Random, offset_y, -5, 50
                sleep_time_min = 6500 ;5 seconds
                sleep_time_max = 8500
                in_game_verification_text := "image_library\agility_course\jump_gap_text.png"
                message := "jumping first gap"
                
            case "cross_tightrope":
                x1 := 690, y1 := 900, x2 := 730, y2 := 980
                Random, offset_x, -30, 30
                Random, offset_y, 5, 60
                sleep_time_min = 9000
                sleep_time_max = 9500
                in_game_verification_text := "image_library\agility_course\cross_tightrope_text.png"
                message := "crossing tightrope"
                
            case "jump_gap_2":
                x1 := 950, y1 := 800, x2 := 1200, y2 := 880
                Random, offset_x, -20, 200
                Random, offset_y, 5, 60
                sleep_time_min = 4500
                sleep_time_max = 6500
                in_game_verification_text := "image_library\agility_course\jump_gap_text.png"
                message := "jumping second gap"
                
            case "jump_gap_3":
                x1 := 100, y1 := 750, x2 := 315, y2 := 800
                Random, offset_x, -30, 100
                Random, offset_y, 5, 60
                sleep_time_min = 5500
                sleep_time_max = 7500
                in_game_verification_text := "image_library\agility_course\jump_gap_text.png"
                message := "jumping third gap"
                
            case "jump_edge":
                x1 := 960, y1 := 550, x2 := 1020, y2 := 800
                Random, offset_x, 10, 100
                Random, offset_y, 5, 300
                sleep_time_min = 200
                sleep_time_max = 300
                in_game_verification_text := "image_library\agility_course\jump_edge_text.png"
                message := "jumping off edge"
        }
        ToolTip, obstacle is %obstacle% `rtries are %tries% `rtrying to find the colorz, XTOOLTIP, YTOOLTIP, 1
        if (pixel_search_and_click(x1, y1, x2, y2, obstacle_color, "mouseover", offset_x, offset_y) 
            or pixel_search_and_click(x1, y1, x2, y2, obstacle_alternate_color, "mouseover", offset_x, offset_y)
            or pixel_search_and_click(0, 0, A_ScreenWidth - 355, A_ScreenHeight, obstacle_color, "mouseover", offset_x, offset_y)
            or pixel_search_and_click(0, 0, A_ScreenWidth - 355, A_ScreenHeight, obstacle_alternate_color, "mouseover", offset_x, offset_y))
        {
            if (image_search_and_click(in_game_verification_text, "top_left"))
            {
                ToolTip, obstacle is %obstacle% `r%tries% tries left. `rsleeping %sleep_time_min%ms to %sleep_time_max%ms, XTOOLTIP, YTOOLTIP, 1
                ctrl_click_in_place()
                sleep_random(sleep_time_min, sleep_time_max)
                return true
            }
        }
        ;always put a sleep in your loop
        sleep_random(100, 200)
        tries--
        ToolTip, tries = %tries%... failed to find the colorz, XTOOLTIP, YTOOLTIP, 1
    }
    return false        
}

;presses down ctrl just before clicking and then lets up off of the ctrl key.
ctrl_click_in_place()
{
    Send, {Ctrl down}
    sleep_random(100,200)
    Click
    sleep_random(100,200)
    Send, {Ctrl up}
    return
}