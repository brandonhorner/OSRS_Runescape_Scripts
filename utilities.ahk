setup()
{
    IfWinActive, %runelite_window%
    {
        ;zoom all the way out
        zoom_out()
        sleep_random(100, 200)
        
        ;Face North (click compass)
        click_compass()
        sleep_random(100, 200)
        
        ;move camera angle to above character
        Send, {up down}
        sleep_random(3000,3500)
        Send, {up up}
        return
    }
}

;zooms the camera in to max by default
zoom_in(zoom_level:=35)
{
    Send, {Wheelup %zoom_level%}
    return
}

;zooms the camera out to max by default
zoom_out(zoom_level:=35)
{
    IfWinActive, %runelite_window%
    {
        Send, {Wheeldown %zoom_level%}
        return
    }
}

click_compass()
{   
    xp_minimap_button := "image_library\xp_minimap_button.bmp"
    shade_variation := 50
    ImageSearch, found_x, found_y, 0, 0, %A_ScreenWidth%, %A_ScreenHeight%, *%shade_variation% %xp_minimap_button%
    if (ErrorLevel = 2)
    {
        Tooltip, Could not conduct the search`rsearch area: 0x0 and %A_ScreenWidth%x%A_ScreenHeight%`rimage = %xp_minimap_button%, 100, 500, 20
        return false
    }
    else if (ErrorLevel = 1)
    {
        Tooltip, Could not find in the search area: 0x0 and %A_ScreenWidth%x%A_ScreenHeight%`rimage = %xp_minimap_button%, 100, 500, 20
        return false
    }
    else
    {
        Random, x_offset, 30, 60
        Random, y_offset, -23, 0
        x_offset += found_x
        y_offset += found_y
        Click, left, %x_offset%, %y_offset%
        return
    }
}

;returns true if menu is open, false otherwise
menu_is_open()
{
    closed_runelite_menu := "image_library\closed_runelite_menu.bmp"
    ImageSearch, dummy_x, dummy_y, 0, 0, %A_ScreenWidth%, %A_ScreenHeight%, %closed_runelite_menu%
    if (ErrorLevel = 2)
    {
        ToolTip, Error: In menu_is_open() -- Could not conduct the search., 100, 400, 20
        return false
    }
    else if (ErrorLevel = 1)
    {
        ; menu was open
        MsgBox, Please close the RuneLite menu.
        return true
    }
    else
    {
        ;menu is closed
        return false
    }
}

; ---------------------- Utilities --------------------------------------------
;Search for an image and click on it. If screen area is omitted, then coordinates must be provided. Offset should
;   be "option" if you are clicking on a '"right"-click "option"' and "item" if you are clicking around an "item" image.
;   If click_type = "right", "right" click, "left" = "left" click, "mouseover" will move the mouse but doesn't click,
;   "doubleclick" clicks twice, "in_place" to click in place.
image_search_and_click(image_url, scan_area:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0)
{
    search_counter = 5
    menu_width = 140
    shade_variation = 0
    
    switch scan_area
    {
        case "top_left":
            x1 := 0
            y1 := 22
            x2 := 190
            y2 := 75
            menu_width := 0
            
        case "bag":
            x1 = 1645
            y1 = 700
            x2 = 1855
            y2 = 1000
            menu_width += 100
            
        case "chat":
            x1 := 0
            y1 := 975
            x2 := 510
            y2 := 1015
            menu_width := 0

        case "middle":
            x1 := 0
            y1 := 200
            x2 := 1650
            y2 := 970
            
        case "bank":
            x1 := 575
            y1 := 50
            x2 := 1060
            y2 := 850
            
        case "under_mouse":
            MouseGetPos, x, y
            x1 := x - 130
            y1 := y
            x2 := x + 120
            y2 := y + 255
            menu_width := 0
    
        case "whole_screen":
            x1 := 0
            y1 := 0
            x2 := %A_ScreenWidth%
            y2 := %A_ScreenHeight%
            menu_width := 0
    }   ;default case is to use the parameters 4 through 7
    
    if (menu_is_open())
    {
        x1 -= menu_width
        x2 -= menu_width
    }
RetryImageSearch:
    IfWinActive, %runelite_window%
    {
        ; delays should be randomized often
        set_random_delays()
        
        ImageSearch, found_x, found_y, %x1%, %y1%, %x2%, %y2%, *%shade_variation% %image_url%
        ;ToolTip, Inside: image_search_and_click() @ImageSearch `r%image_url% was found at %found_x%x%found_y%`r%x1%x%y1% and %x2%x%y2% was the search area, 100, 200, 19
        if (ErrorLevel = 2)     ;if the search wasn't able to start
        {
            MsgBox, Could not conduct the search using: %x1%x%y1% | %x2%x%y2% | %image_url%
            Reload
        }

        else if (ErrorLevel = 1)    ;if we can't find the image
        {
            if (search_counter >= 0)
            {   
                shade_variation += 10
                search_counter--
                Goto, RetryImageSearch
            }
            else
            {
                Tooltip, Retried too many times- bot failed to find: `r%image_url%`rCoords:%x1%x%y1%  |  %x2%x%y2% `rn=%shade_variation% `rIt must be off screen or blocked., 100, 100, 20
                Tooltip, Retried too many times- bot failed to find: `r%image_url%`rCoords:%x1%x%y1%  |  %x2%x%y2% `rn=%shade_variation% `rIt must be off screen or blocked., 100, 100, 20
                return false
            }
        }
        else
        {
            ;depending on what type of image, the offset will be different
            switch offset
            {
                ;"option" refers to when you "right" click in-game, the top "left" of the image is 0,0
                case "option":
                    ;we want to move mouse to the "right" 52 to 92 pixels to click more in the center of the image
                    Random, offset_horizontal, 52, 92
                    ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                    Random, offset_vertical, 2, 11

                ;"item" refers to an "item" in the "bag", also works for fishing spot indicators
                case "item":
                    ;"item" pictures are cut so that the"middle" of the image is the starting point
                    Random, offset_horizontal, -2, 2
                    Random, offset_vertical, -2, 2

                ;default is no offset, can be used when searching but not clicking on an image
                default:
                    offset_horizontal = 0
                    offset_vertical = 0
            }
            
            ;Tooltip, Found: `r%image_url%`rCoords Searched:%x1%x%y1%  |  %x2%x%y2% `r Found at %found_x%x%found_y%, 100, 100, 5
            offset_x := found_x + offset_horizontal
            offset_y := found_y + offset_vertical
            switch click_type
            {
                case "right":
                    Click, right, %offset_x%, %offset_y%
                    
                case "left":
                    Click, %offset_x%, %offset_y%
                    
                case "mouseover":
                    Click, %offset_x%, %offset_y%, 0
                    
                case "doubleclick":
                    Click, %offset_x%, %offset_y%, 2
                    
                case "in_place":
                    Click, 0, 0, 0, Rel
            }
            ;otherwise we do not click and simply return
            return true
        }
    }
    return false
}

;Set the color of a tile in game and use that as the pixel color. if modifier = "right", "right" click,
;    "mouseover" will move the mouse but doesn't click, otherwise "left" click.
pixel_search_and_click(x1, y1, x2, y2, pixel_color, modifier:=0, offset:=0)
{
    IfWinActive, %runelite_window%
    {
        Random, delaySpeed, 60, 110
        SetMouseDelay, %delaySpeed%

        PixelSearch, found_x, found_y, x1, y1, x2, y2, pixel_color, 0, RGB fast ;search region for color
        if ErrorLevel
        {
            ;ToolTip, The color %pixel_color% was not found in %x1%x%y1% %x2%x%y2%, 100, 400, 17
            return false
        }
        else
        {
            ;ToolTip, The color %pixel_color% was found at %found_x%x%found_y% `rmodifier= %modifier%, 100, 300, 18
            
            ;these magic numbers are about the size of the tile to be clicked into, they might need to be adjusted
            ;         depending on how small the object inside of the tile is.
            
            switch offset
            {
                case "mining":
                    Random, offset_x, -50, -10
                    Random, offset_y, 0, 50
                default:
                    Random, offset_x, -5, 10
                    Random, offset_y, 0, 15
            }

            offset_x += found_x
            offset_y += found_y
            
            switch modifier
            {
                case "right":
                    Click, right, %offset_x%, %offset_y%
            
                case "mouseover":
                    Click, %offset_x%, %offset_y%, 0
            
                case "left":
                    Click, %offset_x%, %offset_y%
            }
            ;otherwise do nothing, but return 'true' meaning the color was found
            return true
        }
    }
    return false
}

set_random_delays()
{   
    ;set the dalay of your mouse movement between 20ms and 40ms
    Random, delaySpeed, 60, 80
    SetMouseDelay, %delaySpeed%
    
    Random, key_delay_speed, 10, 12
    Random, press_duration, 10, 12
    SetKeyDelay, %key_delay_speed%, %press_duration%
    
}
sleep_random( sleep_time_low, sleep_time_high )
{
    Random, sleep_time, sleep_time_low, sleep_time_high
    Sleep, %sleep_time%
    
    return
}

;Move the mouse randomly, offset from the current location
mouse_move_random_offset(lower_x:=-100, upper_x:=100, lower_y:=-90, upper_y:=90)
{
    Random, rand_x, lower_x, upper_x
    Random, rand_y, lower_y, upper_y
    MouseMove, rand_x, rand_y,, R
}