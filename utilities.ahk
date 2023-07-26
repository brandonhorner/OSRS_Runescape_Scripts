global XTOOLTIP := 600
global YTOOLTIP := 550

setup()
{
    if WinActive(runelite_window)
    {
        ;zoom all the way out
        zoom("out")
        sleep_random(100, 200)
        
        ;Face North (click compass)
        click_compass()
        sleep_random(100, 200)
        
        ;move camera angle to above character
        Send("{up down}")
        sleep_random(1300, 5000)
        Send("{up up}")
        return
    }
}

;after each iteration, move the mouse, this can fix what went wrong during the loop, as sometimes the mouse gets in the way.
move_mouse_center()
{
    offset_x := Random(-300, 300)
    offset_y := Random(-300, 300)
    
    new_x_pos := A_ScreenWidth/2 + offset_x
    new_y_pos := A_ScreenHeight/2 + offset_y
    
    MouseMove(new_x_pos, new_y_pos)
}

;zooms the camera out to max by default
zoom(zoom_direction, zoom_level:=30)
{
    move_mouse_center()
    
    if (zoom_direction = "out")
    {
        Loop zoom_level
        {
            Send("{Wheeldown}")
            sleep_random(45, 65)
        }
    }
    else ;zooming in
    {
        Loop zoom_level
        {
            Send("{Wheelup}")
            sleep_random(35, 55)
        }
    }
    return
}

click_compass()
{   
    xp_minimap_button := A_WorkingDir "\image_library\xp_minimap_button.bmp"
    shade_variation := 50
    ErrorLevel := !ImageSearch(&found_x, &found_y, 0, 0, A_ScreenWidth, A_ScreenHeight, "*" shade_variation " " xp_minimap_button)
    if (ErrorLevel = 2)
    {
        ToolTip("Could not conduct the search`rsearch area: 0x0 and " A_ScreenWidth "x" A_ScreenHeight "`rimage = " xp_minimap_button, 100, 500, 20)
        return false
    }
    else if (ErrorLevel = 1)
    {
        ToolTip("Could not find in the search area: 0x0 and " A_ScreenWidth "x" A_ScreenHeight "`rimage = " xp_minimap_button, 100, 500, 20)
        return false
    }
    else
    {
        x_offset := Random(30, 60)
        y_offset := Random(-23, 0)
        x_offset += found_x
        y_offset += found_y
        Click("left, " x_offset ", " y_offset)
        return
    }
}

;check to see if "bag" is open
open_bag(x1,y1,x2,y2)
{
    open_bag_pic := A_WorkingDir "\image_library\open_bag.bmp"
    if WinActive(runelite_window)
    {
        Tooltip("Searching: " A_WorkingDir . open_bag_pic, 100, 100, 1)
        ErrorLevel := ImageSearch(&found_x, &found_y, x1, y1, x2, y2, open_bag_pic)

        if (ErrorLevel = 2)
        {
            ToolTip("Error: In open_bag() -- Could not conduct the search.", 100, 400, 20)
            return false
        }
        else
        {
            ; open "bag" was not found, open the "bag" with F3 by default
            SendInput(1)
            return true
        }
    }
    return false
}

; returns true if menu is open, false otherwise
menu_is_open()
{
    menu_bg_color := 0x282828
    ErrorLevel := !PixelSearch(&found_x, &found_y, 1867, 849, 1874, 867, menu_bg_color, "RGB fast")
    ErrorLevel := !PixelSearch(&found_x2, &found_y2, 1641, 472, 1650, 530, menu_bg_color, "RGB fast")
    
       ;deprecated: closed_runelite_menu := A_WorkingDir "\image_library\closed_runelite_menu.bmp"
    ; if either variable is populated then the pixel color was found
    if (found_x or found_x2)
    {
        ; menu is open so return true
        MsgBox("Please close the RuneLite menu.")
        return true
    }
    ; menu was not open (pixel color of menu background was not found)
    return false
}

click_closest(image_url)
{
    if WinActive(runelite_window)
    {
        ;how many pixels to expand the search area each iteration
        expansion_x := "40"
        expansion_y := "22"
        
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

click_closest_pixel(pixel_color, click_type:="left", offset_x:=0, offset_y:=0)
{
    if WinActive(runelite_window)
    {
        ;how many pixels to expand the search area each iteration
        expansion_x := "80"
        expansion_y := "44"
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

;Search for an image (and maybe click on it). 
;   If screen_area is omitted, then coordinates must be provided. Offset should
;   be "option" if you are clicking on a 'right-click option' and "item" if you are clicking an items image. These are
;   preset areas the size of the image and the size of the options (when you right click in game).
;   If click_type = "right", right-click, "left" = left-click, "mouseover" will move the mouse but doesn't click,
;   "doubleclick" clicks twice, "in_place" to click in place. If you omit click_type, then it will not click but still
;   returns true
image_search_and_click(image_url, scan_area:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0)
{
    attempts := "5"
    menu_width := "140"
    shade_variation := "15"
    
    switch scan_area
    {
        case "top_left":
            x1 := 0
            y1 := 22
            x2 := 190
            y2 := 75
            menu_width := 0
            
        case "bag":
            x1 := "1645"
            y1 := "700"
            x2 := "1855"
            y2 := "1000"
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
            MouseGetPos(&x, &y)
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
    if WinActive(runelite_window)
    {
        ; delays should be randomized often
        set_random_delays()
        
        ErrorLevel := !ImageSearch(&found_x, &found_y, x1, y1, x2, y2, "*" shade_variation " " image_url)
        ;ToolTip, Inside: image_search_and_click() @ImageSearch `r%image_url% was found at %found_x%x%found_y%`r%x1%x%y1% and %x2%x%y2% was the search area, 100, 200, 19
        if (ErrorLevel = 2)     ;if the search wasn't able to start
        {
            MsgBox("Could not conduct the search using: " x1 "x" y1 " | " x2 "x" y2 " | " image_url)
            Reload()
        }

        else if (ErrorLevel = 1)    ;if we can't find the image
        {
            if (attempts >= 0)
            {   
                shade_variation += 15
                attempts--
                Goto RetryImageSearch
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
                    offset_horizontal := Random(52, 92)
                    ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                    offset_vertical := Random(2, 11)

                ;"item" refers to an "item" in the "bag", also works for fishing spot indicators
                case "item":
                    ;"item" pictures are cut so that the"middle" of the image is the starting point
                    offset_horizontal := Random(-2, 2)
                    offset_vertical := Random(-2, 2)

                ;default is no offset, can be used when searching but not clicking on an image
                default:
                    offset_horizontal := "0"
                    offset_vertical := "0"
            }
            
            ;Tooltip, Found: `r%image_url%`rCoords Searched:%x1%x%y1%  |  %x2%x%y2% `r Found at %found_x%x%found_y%, 100, 100, 5
            offset_x := found_x + offset_horizontal
            offset_y := found_y + offset_vertical
            switch click_type
            {
                case "right":
                    Click("right, " offset_x ", " offset_y)
                    
                case "left":
                    Click(offset_x ", " offset_y)
                    
                case "mouseover":
                    Click(offset_x ", " offset_y ", 0")
                    
                case "doubleclick":
                    Click(offset_x ", " offset_y ", 2")
                    
                case "in_place":
                    Click("0, 0, 0, Rel")
            }
            ;otherwise we do not click and simply return
            return true
        }
    }
    return false
}


;Set the color of a tile in game and use that as the pixel color. if modifier = "right", "right" click,
;   "mouseover" will move the mouse but doesn't click, otherwise "left" click. Optionally can input
;   an offset x and y to offset where the function will click (in case you are searching for an image
;   but want to click something in an area nearby it.
pixel_search_and_click(x1, y1, x2, y2, pixel_color, modifier:=0, offset_x:=0, offset_y:=0)
{
    if WinActive(runelite_window)
    {
        delaySpeed := Random(20, 80)
        SetMouseDelay(delaySpeed)

        ErrorLevel := !PixelSearch(&found_x, &found_y, x1, y1, x2, y2, pixel_color, 10) ;search region for color
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
                    Click("right, " offset_x ", " offset_y)
            
                case "mouseover":
                    Click(offset_x ", " offset_y ", 0")
            
                case "left":
                    Click(offset_x ", " offset_y)
            }
            ;otherwise do nothing, but return 'true' meaning the color was found
            return true
        }
    }
    return false
}

;Move the mouse randomly, offset from the current location
mouse_move_random_offset(lower_x:=-100, upper_x:=100, lower_y:=-90, upper_y:=90)
{
    rand_x := Random(lower_x, upper_x)
    rand_y := Random(lower_y, upper_y)
    MouseMove(rand_x, rand_y, , "R")
    return
}

; Function to check if the image_url is present in the window
ImageExists(image_url, x1:=0,y1:=0, x2:=A_ScreenWidth,y2:=A_ScreenHeight) {
    CoordMode "ToolTip", "Screen"
    CoordMode "Pixel"

    shade_variation := 90
    found_image := false

    ;Sleep RandomSeconds(.2 , 1.5)
    try {
        ; Search for the image on the entire screen with variation tolerance of 50
        if ImageSearch(&FoundX, &FoundY, x1, y1, x2, y2, "*50 *TransBlack " image_url) {
            ;ToolTip image_url " WAS found!", XTOOLTIP+70, YTOOLTIP+100, 1
            found_image := true
            return found_image
        } else {
            ;ToolTip image_url " was NOT found!", XTOOLTIP+70, YTOOLTIP+100, 1
        }
    } catch as exc {
        ToolTip "Could not conduct the search due to the following error:`n" exc.Message, XTOOLTIP+80, YTOOLTIP+90, 9
        Sleep 5000
    }

    return found_image
}

; this function waits for a
WaitForImage(image_url) {
    while (!ImageExists(image_url)) {
        if (A_Index > 10){
            return false
        }
        Sleep RandomSeconds(.5, 1)
    }
    return true
}

; Function to simulate pressing and holding a key and display a tooltip
PressAndHoldKey(key, duration, times := 1) {

    Loop times
    { 
        ToolTip key " for " duration "ms (" times " time(s))", XTOOLTIP+70, YTOOLTIP-25, 2
        Send "{" key " down}"
        Sleep duration
        Send "{" key " up}"
    
        ; if duration is over 1 second, we can risk subtracting
        if (duration > 1000) {
            duration := duration + RandomSeconds(-.2, .2)
        }
        ; otherwise still change it up but be safer
        else {
            duration := duration + RandomSeconds(0, .05)
        }
    }
    Return
}

; Function to display tooltip and send a key
SendKey(key, presses := 1){
    ToolTip key presses, XTOOLTIP+70, YTOOLTIP-25, 2
    set_random_delays(45, 85)

    if (presses <= 1){
        Send "{" key "}"
        return
    }
    if (presses > 1){
        Send "{" key "}"
        SendKey(key, presses - 1)
        Return
    }
}

set_random_delays(mouse_delay_low := 40, mouse_delay_high := 43, key_delay_low := 80, key_delay_high := 190, press_duration_low := 40, press_duration_high := 75) {
    ; Set the delay of your mouse movement in microseconds
    delaySpeed := Random(mouse_delay_low, mouse_delay_high)
    SetMouseDelay(delaySpeed)
    
    key_delay_speed := Random(key_delay_low, key_delay_high)
    press_duration := Random(press_duration_low, press_duration_high)
    SetKeyDelay(key_delay_speed, press_duration)
}

; Function to sleep for a random time between low and high values in seconds
RandomSeconds(low, high) {
    waitTime := Random(low * 1000, high * 1000)
    return waitTime
}

sleep_random(sleep_time_low, sleep_time_high)
{
    sleep_time := Random(sleep_time_low, sleep_time_high)
    Sleep(sleep_time)
    
    return
}

AdjustWindow() {
  ; Maximize the Pokemmo window
  WinMaximize "a"
  Sleep 1000 ; Wait for a second (adjust the delay if necessary)

  ; Restore the Pokemmo window to its previous size and position
  WinRestore "PokeMMO"
  Sleep 1000
}