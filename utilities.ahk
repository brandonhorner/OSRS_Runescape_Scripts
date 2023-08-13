/*
    Utilites for OSRS bots
*/
setup()
{
     If WinActive("ahk_group active_windows")
    {
        ;zoom all the way out
        zoom("out")
        sleep_random(100, 200)
        
        ;Face North (click compass)
        click_compass()
        sleep_random(100, 200)
        
        ;move camera angle to above character
        Send, {up down}
        sleep_random(1300, 3000)
        Send, {up up}
        return
    }
}

restart_runelite_client()
{
    close_runelite()
    open_runelite()
    return
}

close_runelite()
{
    if (WinExist(runelite_window))
    {
        WinKill, %runelite_window%
        WinWaitClose, %runelite_window%
    }
    if (WinExist("RuneLite"))
    {
        WinKill, "RuneLite"
        WinWaitClose, "RuneLite"
    }
}

open_runelite()
{
    Run, "F:\Users\brand\AppData\Local\RuneLite\RuneLite.exe"
    ToolTip, waiting for RuneLite to start (20-30sec), XTOOLTIP, YTOOLTIP, 1
    sleep_random(20000, 30000)
}

disconnect_check()
{
    disconnect_ok_image := "image_library\utilities\disconnected.png"
    ;if we see the disconnect image, then click okay
    
    if (image_search_and_click(disconnect_ok_image, "middle", "left"))
        return true
    return false
}

login()
{
    set_random_delays()
    welcome_page := "image_library\utilities\welcome_page.png"
    existing_user := "image_library\utilities\existing_user.png"
    change_server := "image_library\utilities\change_server.png"
    error_loading := "image_library\utilities\error_loading.png"
    login_page := "image_library\utilities\login_page.png"
    click_here_to_play := "image_library\utilities\click_here_to_play.png"
    
    wait_attempts = 0
    ;if (image_search_and_click(xp_minimap_button, "m"))
    ; if we are passed the log in page already
    if (image_search_and_click(click_here_to_play, "main_menu", "left"))
    {
        ; we have clicked the play button
        return true
    }
    
    ; or if we are on the welcome page
    ToolTip, searching for welcome page, XTOOLTIP, YTOOLTIP, 1
    if (image_search_and_click(welcome_page, "main_menu", "mouseover"))
    {
        ; move to the login page
        image_search_and_click(existing_user, "main_menu", "left")
    }
    
    ; or if we are already on the log in page
    ToolTip, searching for log in page, XTOOLTIP, YTOOLTIP, 1
    if (image_search_and_click(login_page, "main_menu", "left"))
    {
        sleep_random(800, 1200)
        Send, 2vwftwi527t
        sleep_random(200, 600)
        Send, {Enter}
        
        while (!image_search_and_click(click_here_to_play, "main_menu", "left"))
        {
            ; if we have waited for over 2 minutes, things likely haven't gone well...
            if (wait_attempts > 120)
            {
                ;rerun the script
                return main()
            }
            if (image_search_and_click(change_server, "main_menu") 
                or image_search_and_click(error_loading, "main_menu"))
                restart_runelite_client()
            
            ToolTip, %wait_attempts%. waiting for click here to play button, XTOOLTIP, YTOOLTIP, 1
            sleep_random(1000, 1500)
            wait_attempts++
        }
        return true
    }
    return false
}

check_logged_in()
{
    ToolTip, checking if disconnected..., XTOOLTIP, YTOOLTIP, 1
    if (disconnect_check())
    ToolTip, trying to log in..., XTOOLTIP, YTOOLTIP, 1
    if (login())
        return
}

;after each iteration, move the mouse, this can fix what went wrong during the loop, as sometimes the mouse gets in the way.
move_mouse_center()
{
    Random, offset_x, -300, 300
    Random, offset_y, -300, 300
    
    new_x_pos := A_ScreenWidth/2 + offset_x
    new_y_pos := A_ScreenHeight/2 + offset_y
    
    MouseMove, %new_x_pos%, %new_y_pos%
}

;zooms the camera out to max by default
zoom(zoom_direction, zoom_level:=30)
{
    move_mouse_center()
    
    if (zoom_direction = "out")
    {
        Loop, %zoom_level%
        {
            Send, {Wheeldown}
            sleep_random(45, 65)
        }
    }
    else ;zooming in
    {
        Loop, %zoom_level%
        {
            Send {Wheelup}
            sleep_random(35, 55)
        }
    }
    return
}


click_compass()
{
    xp_minimap_button := "image_library\utilities\xp_minimap_button.bmp"
    shade_variation := 50
    ImageSearch, found_x, found_y, 1670, 450, 1700, 70, *%shade_variation% %xp_minimap_button%
    if (ErrorLevel = 2)
    {
        Tooltip, Could not conduct the search`rsearch area: 1670x45 and 1700x70`rimage = %xp_minimap_button%, 100, 500, 20
        return false
    }
    else if (ErrorLevel = 1)
    {
        ;Tooltip, Could not find in the search area: 1670x45 and 1700x70`rimage = %xp_minimap_button%, 100, 500, 20
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
    closed_runelite_menu := "image_library\utilities\closed_runelite_menu.bmp"
    ImageSearch, dummy_x, dummy_y, 0, 0, %A_ScreenWidth%, %A_ScreenHeight%, %closed_runelite_menu%
    if (ErrorLevel = 2)
    {
        ToolTip, Error: In menu_is_open() -- Could not conduct the search., 100, 400, 20
        return false
    }
    else if (ErrorLevel = 1)
    {
        ; menu was open
        TrayTip,, Please close the RuneLite menu.
        return true
    }
    else
    {
        ;menu is closed
        return false
    }
}

click_closest(image_url)
{
     If WinActive("ahk_group active_windows")
    {
        ;how many pixels to expand the search area each iteration
        expansion_x = 40
        expansion_y = 22
        ;center of screen, only character is enclosed
        x1 := 925
        y1 := 515
        x2 := 950
        y2 := 540
        
        while (x2 < A_ScreenWidth and y2 < A_ScreenHeight)
        {
            ;click the image within the current area
            if (image_search_and_click(image_url, "new_area", "left", "item", x1, y1, x2, y2))
            {
                ;mouse_move_random_offset()
                return true
            }
            else    ;grow search area
            {
                x1 -= %expansion_x%
                y1 -= %expansion_y%
                x2 += %expansion_x%
                y2 += %expansion_y%
            }
        }
    }
    ;TrayTip,, returning false (click_closest())
    return false
}

; Check the center of screen before expanding search to a larger section (until the full
;    screen is being searched). Can help with clicking the closest pixel to the character.
; Parameters - 
;   pixel_color - 
click_closest_pixel(pixel_color, click_type:="left", offset_x:=0, offset_y:=0)
{
     If WinActive("ahk_group active_windows")
    {
        ;how many pixels to expand the search area each iteration
        expansion_x = 80
        expansion_y = 44
        ;center of screen, only character is enclosed
        x1 := 925
        y1 := 515
        x2 := 950
        y2 := 540
        
        while (x2 < A_ScreenWidth and y2 < A_ScreenHeight)
        {
            ;ToolTip, %pixel_color% was not found %x1%x%y1% and %x2%x%y2%, 300, 300, 17
            if (pixel_search_and_click(x1, y1, x2, y2, pixel_color, click_type, offset_x, offset_y))
            {
                ;mouse_move_random_offset()
                ;ToolTip, %pixel_color% was found at %x1%x%y1% and %x2%x%y2%, 700, 700, 16
                return true
            }
            else    ;grow search area
            {
                x1 -= %expansion_x%
                y1 -= %expansion_y%
                x2 += %expansion_x%
                y2 += %expansion_y%
            }
            sleep_random(200, 300)

        }
    }
    return false
}

;Search for an image and click on it. If screen area is omitted, then coordinates must be provided. Offset should
;   be "option" if you are clicking on a '"right"-click "option"' and "item" if you are clicking around an "item" image.
;   If click_type = "right", "right" click, "left" = "left" click, "mouseover" will move the mouse but doesn't click,
;   "doubleclick" clicks twice, "in_place" to click in place.
image_search_and_click(image_url, scan_area:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0)
{
    attempts = 5
    menu_width = 140
    shade_variation = 15
    
    switch scan_area
    {
        case "main_menu":
            x1 := 760, y1 := 200
            x2 := 1109, y2 := 385
            
        case "top_left":
            x1 := 0, y1 := 22
            x2 := 190, y2 := 75
            menu_width := 0
            
        case "bag":
            x1 = 1645, y1 = 700
            x2 = 1855, y2 = 1000
            menu_width += 100
            
        case "chat":
            x1 := 0, y1 := 975
            x2 := 510, y2 := 1015
            menu_width := 0

        case "middle":
            x1 := 0, y1 := 200
            x2 := 1650, y2 := 970
            
        case "bank":
            x1 := 575, y1 := 50
            x2 := 1060, y2 := 850
            
        case "under_mouse":
            MouseGetPos, x, y
            x1 := x - 130, y1 := y
            x2 := x + 120, y2 := y + 255
            menu_width := 0
    
        case "whole_screen":
            x1 := 0, y1 := 0
            x2 := %A_ScreenWidth%, y2 := %A_ScreenHeight%
            menu_width := 0
    }   ;default case is to use the parameters 4 through 7
    
    if (menu_is_open())
    {
        x1 -= menu_width
        x2 -= menu_width
    }
RetryImageSearch:
    if (WinActive("ahk_group active_windows"))
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
            if (attempts >= 0)
            {   
                shade_variation += 15
                attempts--
                Goto, RetryImageSearch
            }
            else
            {
                ;Tooltip, Retried too many times- bot failed to find: `r%image_url%`rCoords:%x1%x%y1%  |  %x2%x%y2% `rn=%shade_variation% `rIt must be off screen or blocked., 100, 100, 20
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
pixel_search_and_click(x1, y1, x2, y2, pixel_color, modifier:=0, offset_x:=0, offset_y:=0)
{
    if (WinActive("ahk_group active_windows"))
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
            ;these offsets should be determined on a case by case basis
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
    Random, delaySpeed, 20, 40
    SetMouseDelay, %delaySpeed%
    
    Random, key_delay_speed, 30, 130
    Random, press_duration, 50, 300
    SetKeyDelay, %key_delay_speed%, %press_duration%
    return
}


sleep_random(min_time, max_time)
{
    Random, sleep_time, min_time, max_time
    Sleep, %sleep_time%
    return
}


;Move the mouse randomly, offset from the current location
mouse_move_random_offset(lower_x:=-100, upper_x:=100, lower_y:=-90, upper_y:=90)
{
    Random, rand_x, lower_x, upper_x
    Random, rand_y, lower_y, upper_y
    MouseMove, rand_x, rand_y,, R
    return
}