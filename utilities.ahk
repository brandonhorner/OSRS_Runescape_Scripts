; This file is for testing purposes and should remain convenient to open
global XTOOLTIP := 600
global YTOOLTIP := 550

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")

SetWorkingDir "C:\Git\OSRS_Runescape_Scripts"

; these are image files used for image searching
global images := {
    menaphite_hovering_text : A_WorkingDir "\image_library\blackjacking\menaphite_hovering_text.png",
    lobster_cooked : A_WorkingDir "\image_library\lobster_cooked.png",
    lobster_cooked_noted : A_WorkingDir "\image_library\blackjacking\lobster_cooked_noted.png",
    knockout_option : A_WorkingDir "\image_library\blackjacking\knockout_option.bmp",
    knockout_success : A_WorkingDir "\image_library\blackjacking\knockout_success.bmp",
    knockout_failure : A_WorkingDir "\image_library\blackjacking\knockout_failure.bmp",
    pickpocket_option : A_WorkingDir "\image_library\blackjacking\pickpocket_option.bmp",
    pickpocket_attempt : A_WorkingDir "\image_library\blackjacking\pickpocket_attempt.bmp",
    pickpocket_success : A_WorkingDir "\image_library\blackjacking\pickpocket_success.bmp",
    pickpocket_failure : A_WorkingDir "\image_library\blackjacking\pickpocket_failure.bmp",
    cant_pickpocket_combat : A_WorkingDir "\image_library\blackjacking\cant_pickpocket_combat.png",
    right_click_options : A_WorkingDir "\image_library\blackjacking\right_click_options.png",
    cannot_knockout : A_WorkingDir "\image_library\blackjacking\cannot_do_that.bmp",
    healthbar : A_WorkingDir "\image_library\blackjacking\healthbar.bmp",
    stunned : A_WorkingDir "\image_library\blackjacking\stunned.bmp",
    imstunned : A_WorkingDir "\image_library\blackjacking\imstunned.png",
    missed_right_click : A_WorkingDir "\image_library\blackjacking\missed_right_click.bmp",
    combat : A_WorkingDir "\image_library\blackjacking\combat.bmp",
    money_bag : A_WorkingDir "\image_library\blackjacking\money_bag.png",
    money_bag_full : A_WorkingDir "\image_library\blackjacking\money_bag_full.png",
    minimap_bank_icon : A_WorkingDir "\image_library\minimap_bank_icon.png",
    open_bag : A_WorkingDir "\image_library\open_bag.bmp",
    minimap_cake_stall_icon : A_WorkingDir "\image_library\minimap_cake_stall_icon.png",
    deposit_inventory : A_WorkingDir "\image_library\deposit_inventory.png",
    open_curtain_option : A_WorkingDir "\image_library\blackjacking\open_curtain.png",
    close_curtain_option : A_WorkingDir "\image_library\blackjacking\close_curtain.png",
    select_an_option : A_WorkingDir "\image_library\blackjacking\select_an_option.png",
    stunned : A_WorkingDir "\image_library\been_stunned.bmp",
    xp_minimap_button : A_WorkingDir "\image_library\xp_minimap_button.png"
}

; some tooltip coords
global X_TOOLTIP := {
    1: 0,   ; <-| main functions
    2: 0,   ; <-|
    3: 0,   ; <-|
    4: 980, ; <-|
    
    5: 0,  ; <-| image search / support functions
    6: 0,  ; <-|
    7: 0,  ; <-|
    8: 0,  ; <-|
    9: 0   ; <-|
}

global Y_TOOLTIP := {
    1: 100, ; <-| main functions
    2: 125, ; <-|
    3: 150, ; <-|
    4: 205, ; <-|

    5: 205, ; <-| image search / support functions
    6: 230, ; <-|
    7: 285, ; <-|
    8: 325, ; <-|
    9: 375  ; <-|
}


gameWindowWidth := A_ScreenWidth - 20
; object that holds all of the screen area coordinates
global coord := {
    chat_all:       { x1: 3, y1: 872, x2: 494, y2: 986 },
    chat_bottom:    { x1: 3, y1: 969, x2: 494, y2: 986 },
    chat_bottom_2:  { x1: 3, y1: 958, x2: 494, y2: 986 },
    bag:        { x1:1385, y1:700, x2:1855, y2:1000 },
    top_left:   { x1:0, y1:22, x2:200, y2:128 },
    middle:     { x1:0, y1:200, x2:1650, y2:970 },
    health:     { x1:1400, y1:820, x2:1700, y2:850 },
    
    ; Screen below is split up like this:
    ;                ;                ;               ;
    ;       p1       ;       p2       ;       p3      ;
    ;________________;________________;_______________;
    ;                ;                ;               ;
    ;       p4       ;       p5       ;       p6      ;
    ;                ;                ;               ;
    p1 : { x1:0, y1:20, x2:gameWindowWidth / 3, y2:A_ScreenHeight / 2 },
    p2 : { x1:gameWindowWidth / 3, y1:20, x2:gameWindowWidth * 2 / 3, y2:A_ScreenHeight / 2 },
    p3 : { x1:gameWindowWidth * 2 / 3, y1:20, x2:gameWindowWidth, y2:A_ScreenHeight / 2 },
    p4 : { x1:0, y1:A_ScreenHeight / 2, x2:gameWindowWidth / 3, y2:A_ScreenHeight},
    p5 : { x1:gameWindowWidth / 3, y1:A_ScreenHeight / 2, x2:gameWindowWidth * 2 / 3, y2:A_ScreenHeight},
    p6 : { x1:gameWindowWidth * 2 / 3, y1:A_ScreenHeight / 2, x2:gameWindowWidth, y2:A_ScreenHeight}
}

/**
 * coords to ensure an NPC's orientation
 * add more vertices to these :o
 */
global target_coord := {
    laying_left:    { x:745, y:330 },
    laying_middle:  { x:890, y:225 },
    laying_right:   { x:1030,y:380 },
    laying_bottom:  { x:805, y:600 },
    laying_left_2:    { x:824, y:330 },
    laying_middle_2:  { x:965, y:225 },
    laying_right_2:   { x:1105,y:375 },
    laying_bottom_2:  { x:890, y:600 },
    standing_top_left:      { x:805, y:240 },
    standing_top_right:     { x:975, y:245 },
    standing_bottom_left:   { x:805, y:600 },
    standing_bottom_right:  { x:940, y:535 },
    standing_top_left_2:        { x:885, y:245 },
    standing_top_right_2:       { x:1055,y:245 },
    standing_bottom_left_2:     { x:890, y:600 },
    standing_bottom_right_2:    { x:1030,y:530 }
}

; these are the colors of outlines around NPCs and the tick on the compass
global pixel_color := {
    tile_teal : 0x00FAFF,
    tile_purple : 0x6655FF,
    tile_pink : 0xD769E8,
    object_green: 0xAAFF00,
    bag_background: 0x3E3529,
    npc : 0xA4FF00,
    npc_dark : 0x84CD00,
    tick : 0x00908D,
    tick_2 : 0x1580AD,
    tick_3 : 0x01E0E11
}

; put this back after you look up how to override these
; setup_in()
; {
;     if WinActive(runelite_window)
;     {
;         ;zoom all the way out
;         zoom("in")
;         sleep_random(100, 200)
        
;         ;Face North (click compass)
;         ClickCompass()
;         sleep_random(100, 200)
;     }
; }

InventoryIsFull()
{
<<<<<<< HEAD
    ; if the bag background color is in the last space, then the bag is assumed not full.. 
    ;  probs should make this more robust later
    if PixelSearchAndClick(pixel_color.bag_background,,,, 1821, 967, 1829, 976)
=======
    SendKey(1)
    ; if the bag background color is in the last space, then the bag is assumed not full.. 
    ;  probs should make this more robust later (count 28 non-blank slots)
    if PixelSearchAndClick(pixel_color.bag_background,,,, 1821, 967, 1829, 976, 30)
>>>>>>> c09d5f2b244d69719fe48c1eafc9ff1c49a98648
        return false
    return true
}

setup_out()
{
    if WinActive(runelite_window)
    {
        ;zoom all the way out
        zoom("out")
        sleep_random(100, 200)
        
        ;Face North (click compass)
        ClickCompass()
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

ClickCompass()
{
    shade_variation := 50
    options := "*" shade_variation " " images.xp_minimap_button
    
    if ImageSearch(&foundX, &foundY, 0, 0, A_ScreenWidth, A_ScreenHeight, options)
    {
        x_offset := Random(30, 60)
        y_offset := Random(-23, 0)
        x_offset += foundX
        y_offset += foundY
        Click("left, " x_offset ", " y_offset)
        return true
    }
    else
    {
        ToolTip("Could not conduct the search`rsearch area: 0x0 and " A_ScreenWidth "x" A_ScreenHeight "`rimage = " images.xp_minimap_button, 100, 500, 20)
        return false

    }
}

;check to see if "bag" is open
open_bag()
{
    open_bag_pic := A_WorkingDir "\image_library\open_bag.bmp"
    if WinActive(runelite_window)
    {
        ;Tooltip("Searching: " A_WorkingDir . open_bag_pic, 100, 100, 1)
        ; if open_bag isn't on screen
        if !ImageExists(open_bag_pic, coord.bag.x1, coord.bag.y1, coord.bag.x2, coord.bag.y2)
        {
            ; open bag was not found, open the bag with F3 by default (I changed it to 1)
            SendInput(1)
        } 
        return true
    }
    return false
}

; if menu is open, create a msg box to close the menu, false otherwise
menu_is_open()
{
    menu_bg_color := 0x282828

    if(pixel_search_and_click(1867, 450, 1874, 600, menu_bg_color,,,,0))
    {
        MsgBox("Please close the RuneLite menu.")
        menu_is_open()
    }
    ; menu was not open (pixel color of menu background was not found)
    return false
}

click_closest(ImageURL)
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
            if (image_search_and_click(ImageURL, "new_area", "left", "item", x1, y1, x2, y2))
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
image_search_and_click(ImageURL, scan_area:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0)
{
    attempts := 5
    menu_width := 140
    shade_variation := 15
    
    switch scan_area
    {
        case "top_left":
            x1 := 0
            y1 := 22
            x2 := 190
            y2 := 75
            menu_width := 0
            
        case "bag":
            x1 := 1645
            y1 := 700
            x2 := 1855
            y2 := 1000
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
            x2 := A_ScreenWidth
            y2 := A_ScreenHeight
            menu_width := 0
    }   ;default case is to use the parameters 4 through 7
    
    if (MenuIsOpen())
    {
        x1 -= menu_width
        x2 -= menu_width
    }
    RetryImageSearch:
    if WinActive(runelite_window)
    {
        ; delays should be randomized often
        set_random_delays()
        
        if ImageSearch(&foundX, &foundY, x1, y1, x2, y2, "*50 *TransBlack " ImageURL)
        {
            ;depending on what type of image, the offset will be different
            switch offset
            {
                ;"option" refers to when you right click in-game, the top left of the image is 0,0
                case "option":
                    ;we want to move mouse to the right 52 to 92 pixels to click more in the center of the image
                    offset_horizontal := Random(52, 92)
                    ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                    offset_vertical := Random(2, 11)

                ;"item" refers to an "item" in the "bag", also works for fishing spot indicators
                case "item":
                    ;"item" pictures are cut so that the"middle" of the image is the starting point
                    offset_horizontal := Random(-2, 2)
                    offset_vertical := Random(-2, 2)

                ; This should be used when an item is searched at it's top left corner
                case "item2":
                    offset_horizontal := Random(1, 25)
                    offset_vertical := Random(1, 25)

                ;default is no offset, can be used when searching but not clicking on an image
                default:
                    offset_horizontal := 0
                    offset_vertical := 0
            }
            
            ;Tooltip, Found: `r%ImageURL%`rCoords Searched:%x1%x%y1%  |  %x2%x%y2% `r Found at %foundX%x%foundY%, 100, 100, 5
            offset_x := foundX + offset_horizontal
            offset_y := foundY + offset_vertical

            switch click_type
            {
                case "right":
                    Click("right", offset_x, offset_y)
                    
                case "left":
                    Click(offset_x, offset_y)
                    
                case "mouseover":
                    Click(offset_x, offset_y, 0)
                    
                case "doubleclick":
                    Click(offset_x, offset_y, 2)
                    
                case "in_place":
                    Click()
            }
            ;otherwise we do not click and simply return
            return true
        }
        ;ToolTip, Inside: image_search_and_click() @ImageSearch `r%ImageURL% was found at %foundX%x%foundY%`r%x1%x%y1% and %x2%x%y2% was the search area, 100, 200, 19
    }
    return false
}


;Set the color of a tile in game and use that as the pixel color. if modifier = "right", "right" click,
;   "mouseover" will move the mouse but doesn't click, otherwise "left" click. Optionally can input
;   an offset x and y to offset where the function will click (in case you are searching for an image
;   but want to click something in an area nearby it.
pixel_search_and_click(x1, y1, x2, y2, pixel_color, modifier:=0, offset_x:=0, offset_y:=0, shade_variance := 50)
{
    ;MsgBox("pixel_search_and_click: " x1 " " y1 " " x2 " " y2 " " pixel_color " " modifier " " offset_x " " offset_y " " shade_variance)
    if WinActive(runelite_window)
    {
        ;delaySpeed := Random(20, 80)
        ;SetMouseDelay(delaySpeed)

        if PixelSearch(&foundX, &foundY, x1, y1, x2, y2, pixel_color, shade_variance) ;search region for color
        {
            ;ToolTip, The color %pixel_color% was found at %foundX%x%foundY% `rmodifier= %modifier%, 100, 300, 18
            ;these offsets should be determined on a case by case basis
            offset_x += foundX
            offset_y += foundY
            
            switch modifier
            {
                case "right":   
                    Click("right", offset_x, offset_y)
            
                case "mouseover":
                    Click(offset_x, offset_y, 0)
            
                case "left":
                    Click(offset_x,  offset_y)
            }
            ;otherwise do nothing, but return 'true' meaning the color was found
            return true
        }
        ;ToolTip, The color %pixel_color% was not found in %x1%x%y1% %x2%x%y2%, 100, 400, 17
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
    ToolTip "", XTOOLTIP+70, YTOOLTIP-25, 2
    Return
}

; Function to display tooltip and send a key
SendKey(key, presses := 1){
    ToolTip "Key: " key "`nPresses: "  presses " times ", X_TOOLTIP.3, Y_TOOLTIP.3, 3
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

; WAS set_random_delays(mouse_delay_low := 40, mouse_delay_high := 43, key_delay_low := 80, key_delay_high := 190, press_duration_low := 40, press_duration_high := 75) {
set_random_delays(mouse_delay_low := 20, mouse_delay_high := 23, key_delay_low := 30, key_delay_high := 50, press_duration_low := 20, press_duration_high := 30) {
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
    Sleep sleep_time
    
    return sleep_time
}

AdjustWindow() {
  ; Maximize the Pokemmo window
  WinMaximize "a"
  Sleep 1000 ; Wait for a second (adjust the delay if necessary)

  ; Restore the Pokemmo window to its previous size and position
  WinRestore "PokeMMO"
  Sleep 1000
}

exists(image_area, ImageURL)
{
    ;options in the top left are good for verification before an action.  
    switch image_area
    {
        case "top_left":
            return image_search_and_click_v2(coord.top_left.x1, coord.top_left.y1, coord.top_left.x2, coord.top_left.y2, ImageURL, 0, 0)

        case "chat":    ; use coordinates relative to chat window area
            return image_search_and_click_v2(coord.bag.x1, coord.bag.y1, coord.bag.x2, coord.bag.y2, ImageURL, 0, 0)
        
        default:    ; default to "middle" of screen coordinates 
            return image_search_and_click_v2(coord.middle.x1, coord.middle.y1, coord.middle.x2, coord.middle.y2, ImageURL, 0, 0)
    }
    
    return image_search_and_click_v2(0, 0, A_ScreenWidth, A_ScreenHeight, ImageURL, 0, 0)

}

;Search for an image and click on it. If modifier = "right", "right" click,
;    "mouseover" will move the mouse but doesn't click, otherwise left click.
image_search_and_click_v2(x1, y1, x2, y2, ImageURL, modifier, offset)
{
    abort_counter := 5
    n := 1

Retry:
    if WinActive(runelite_window){
        ; delays should be randomized often
        set_random_delays()

        ; search for the image                         *40 means 40 shades away from the picture's color
        ErrorLevel := !ImageSearch(&foundX, &foundY, x1, y1, x2, y2, "*50 *TransBlack " ImageURL)
        if (ErrorLevel = 2){
            ToolTip("Could not conduct the search using: " x1 "x" y1 " | " x2 "x" y2 " | " ImageURL, 0, 100, 6)
            return false
        }
        else if (ErrorLevel = 1){
            ;mouse_move_random_offset()
            abort_counter--
            if (abort_counter > 0){
                n += 20
                Goto("Retry")
            }
            else{
                ;ToolTip("Retried 5 times- bot failed to find: `r" ImageURL "`rCoords:" x1 "x" y1 "  |  " x2 "x" y2 " `rn=" n " `rIt must be off screen or blocked.", 0, 100, 6)
                return false
            }
        }
        else{
            ;option refer to when you "right" click in-game, the top left of the image is 0,0
            if (offset = "option"){
                ;we want to move mouse to the "right" 52 to 92 pixels to click more in the center of the image
                offset_horizontal := Random(72, 98)
                ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                offset_vertical := Random(3, 10)
            }
            else if (offset = "item"){
                offset_horizontal := Random(0, 20)
                offset_vertical := Random(0, 20)
            }
            else{
                offset_horizontal := Random(0, 0)
                offset_vertical := Random(-0, 0)
            }
            ;TrayTip,, Found: `r%ImageURL%`rCoords Searched:%x1%x%y1%  |  %x2%x%y2% `r Found at %foundX%x%foundY%
            offset_x := foundX + offset_horizontal
            offset_y := foundY + offset_vertical
            if (modifier = "right")
                Click(offset_x, offset_y, "Right")
            if (modifier = "mouseover")
                MouseMove(offset_x, offset_y)
            if (modifier = "doubleclick")
                Click(offset_x, offset_y, 2)
            if (modifier = "left")
                Click(offset_x, offset_y)
            ;otherwise we do not click and simply return
            return true
        }
    }
    return false
}

; weird things happen when you pass a hexadecimal color two times, so maybe don't use this function lol
WaitForPixel(color, x1, y1, x2, y2)
{
    ; MsgBox("WaitForPixel: " color " " x1 " " y1 " " x2 " " y2)  
    ; try 10k times lol (3.6GHz baby)!
    while (A_Index < 10000) {
        if (pixel_search_and_click(x1, y1, x2, y2, color)){
            return true
        }
                                                                                ToolTip("5. WaitForPixel: " A_Index " tries. Can't find the color...", X_TOOLTIP.5, Y_TOOLTIP.5, 5)
    }
    ;ToolTip(A_Index ": Found color...", 900, 300, 6)
    return true
}

WaitForTick()
{
    while (A_Index < 10000 )
    {   ;1700, 119, 1704, 123
        if (pixel_search_and_click(1700, 119, 1706, 123, pixel_color.tick)) {
            return true
        }
                                                                                ToolTip("5. WaitForTick(): " A_Index " tries. Can't find the color...", X_TOOLTIP.5, Y_TOOLTIP.5, 5)
    }
    return false
}

; Check to see if the mini map button is in the normal position
MenuIsOpen()
{
    StartTime := A_TickCount
    ; Keep checking until timeout have passed
    while (A_TickCount - StartTime) < 50 {
        if(ImageExists(images.xp_minimap_button, 1665, 56, 1695, 81))
            return false
    }
    return true
}

; click the first available lobster in your inventory
EatLobster()
{
                                                                            ToolTip "Eating lobster...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    open_bag()
    sleep_random(500, 1500)
    if ImageSearchAndClick(images.lobster_cooked, "bag", "mouseover", "item") {
        sleep_random(500, 1500)
        Click("Left")
        sleep_random(500, 1500)
        return true
    }
                                                                            ToolTip "...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return false
}


HealthIsLow()
{
    if ImageExists(images.healthbar, 1400, 820, 1700, 850)
    {
        return false
    }
                                                                            ToolTip "Health is low...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return true
}

CheckIfStunned()
{
                                                                            ToolTip "Stunned. Waiting...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    if ImageSearchAndClick(images.imstunned, "top_left",,,,,,,5)
    {
        sleep_random(100, 100)
        return true
    }
                                                                            ToolTip "", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return false
}

CheckIfFullOnMoneyBags()
{
    SendKey("1")
    if ImageSearchAndClick(images.money_bag_full, "bag", "mouseover", "item") {
                                                                            ToolTip "Clicking the FULL money bag :')...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
        sleep_random(400, 900)
        Click("Left")
        sleep_random(500, 900)
        return true
    }
    return false
}

; 1 in 4 chance to click the money bag in your inventory
ClickMoneyBag()
{
    lucky_number := Random(1,5)
    if !(lucky_number = 4)
        return false    
    
    SendKey(1)
    if ImageExists(images.open_bag) {                                       ;ensure bag is open
        sleep_random(10, 100)
        if ImageSearchAndClick(images.money_bag, "bag", "mouseover", "item")
                                                                            ToolTip "Clicking the money bag...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
            sleep_random(500, 1500)
            Click("Left")
            sleep_random(500, 1500)
            return true
    }
                                                                            ToolTip "", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return false
}

; target is outlined with a solid line, this function checks for a pixel at 4 points around the outline
;   if 3 out of 4 points are found, we are going to return true, there is only one cardinal
;   direction that can produce these 3 points, so we know they standing up facing us
TargetIsStandingUpFacingMe()
{
    offset := 30
    count := 0
    ; search for the top left, and the top left + offset for light and dark color
    if pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + offset, target_coord.standing_top_left.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + offset, target_coord.standing_top_left.y + offset, pixel_color.npc_dark) ||
        pixel_search_and_click(target_coord.standing_top_left_2.x, target_coord.standing_top_left_2.y, target_coord.standing_top_left_2.x + offset, target_coord.standing_top_left_2.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_top_left_2.x, target_coord.standing_top_left_2.y, target_coord.standing_top_left_2.x + offset, target_coord.standing_top_left_2.y + offset, pixel_color.npc_dark)
        count += 1

    if pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + offset, target_coord.standing_top_right.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + offset, target_coord.standing_top_right.y + offset, pixel_color.npc_dark) ||
        pixel_search_and_click(target_coord.standing_top_right_2.x, target_coord.standing_top_right_2.y, target_coord.standing_top_right_2.x + offset, target_coord.standing_top_right_2.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_top_right_2.x, target_coord.standing_top_right_2.y, target_coord.standing_top_right_2.x + offset, target_coord.standing_top_right_2.y + offset, pixel_color.npc_dark)
        count += 1
        
    if pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + offset, target_coord.standing_bottom_left.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + offset, target_coord.standing_bottom_left.y + offset, pixel_color.npc_dark) ||
        pixel_search_and_click(target_coord.standing_bottom_left_2.x, target_coord.standing_bottom_left_2.y, target_coord.standing_bottom_left_2.x + offset, target_coord.standing_bottom_left_2.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_bottom_left_2.x, target_coord.standing_bottom_left_2.y, target_coord.standing_bottom_left_2.x + offset, target_coord.standing_bottom_left_2.y + offset, pixel_color.npc_dark)
        count += 1
        
    if pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + offset, target_coord.standing_bottom_right.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + offset, target_coord.standing_bottom_right.y + offset, pixel_color.npc_dark) ||
        pixel_search_and_click(target_coord.standing_bottom_right_2.x, target_coord.standing_bottom_right_2.y, target_coord.standing_bottom_right_2.x + offset, target_coord.standing_bottom_right_2.y + offset, pixel_color.npc) ||
        pixel_search_and_click(target_coord.standing_bottom_right_2.x, target_coord.standing_bottom_right_2.y, target_coord.standing_bottom_right_2.x + offset, target_coord.standing_bottom_right_2.y + offset, pixel_color.npc_dark)
        count += 1
    
    if (count >= 3)
        return true
    ; Otherwise the target is not standing up or is in another area of the screen
    return false
}

; target is outlined with a solid line, this function checks for a pixel at 4 points around the outline, one point
;   out of 4 points should NOT be there, and 3 should be found. Although if 3 points meet conditions, we're going to
;   return true, there is only one cardinal direction that can produce these 3 points, so we know they laying down facing us
TargetIsLayingDownFacingMe()
{
    count := 0
    ; If the bottom 4 searches result in true, true, true, false
    if pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, pixel_color.npc) ||
        pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, pixel_color.npc_dark) ||
        pixel_search_and_click(target_coord.laying_left_2.x, target_coord.laying_left_2.y, target_coord.laying_left_2.x + 30, target_coord.laying_left_2.y + 30, pixel_color.npc) ||
        pixel_search_and_click(target_coord.laying_left_2.x, target_coord.laying_left_2.y, target_coord.laying_left_2.x + 30, target_coord.laying_left_2.y + 30, pixel_color.npc_dark)
    count += 1
    
    if pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, pixel_color.npc) ||
        pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, pixel_color.npc_dark) ||
        pixel_search_and_click(target_coord.laying_middle_2.x, target_coord.laying_middle_2.y, target_coord.laying_middle_2.x + 30, target_coord.laying_middle_2.y + 30, pixel_color.npc) ||
        pixel_search_and_click(target_coord.laying_middle_2.x, target_coord.laying_middle_2.y, target_coord.laying_middle_2.x + 30, target_coord.laying_middle_2.y + 30, pixel_color.npc_dark)
        count += 1

    if pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, pixel_color.npc) ||
        pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, pixel_color.npc_dark) ||
        pixel_search_and_click(target_coord.laying_right_2.x, target_coord.laying_right_2.y, target_coord.laying_right_2.x + 30, target_coord.laying_right_2.y + 30, pixel_color.npc) ||
        pixel_search_and_click(target_coord.laying_right_2.x, target_coord.laying_right_2.y, target_coord.laying_right_2.x + 30, target_coord.laying_right_2.y + 30, pixel_color.npc_dark)
        count += 1

    if !pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, pixel_color.npc) ||
        !pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, pixel_color.npc_dark) ||
        !pixel_search_and_click(target_coord.laying_bottom_2.x, target_coord.laying_bottom_2.y, target_coord.laying_bottom_2.x + 30, target_coord.laying_bottom_2.y + 30, pixel_color.npc) ||
        !pixel_search_and_click(target_coord.laying_bottom_2.x, target_coord.laying_bottom_2.y, target_coord.laying_bottom_2.x + 30, target_coord.laying_bottom_2.y + 30, pixel_color.npc_dark)
        count += 1
    
    if (count >= 3)
        return true
        
    ; Otherwise the target is not laying down or is in another area of the screen
    return false
}

; finds the target NPC and designates a coordinate to click on
GetTargetClickArea()
{
    target_area := {
        x:(A_ScreenWidth / 2) , y:(A_ScreenHeight / 2)
    }

    if (TargetIsLayingDownFacingMe())
    {
        target_area.x := 900
        target_area.y := 300
    }
    else if (TargetIsStandingUpFacingMe())
    {
        target_area.x := 900
        target_area.y := 340
    }
    return target_area
}

; Get the offsets from the current mouse position.
;     This is specifically for the right click menu items.
GetMousePosOffsets()
{
    MouseGetPos(&x, &y)
    offset := {
        x1 : x - 130,
        y1 : y,
        x2 : x + 120,
        y2 : y + 200
    }
    return offset
}

; This function waits for an image, and an optional timeout (default is 10s)
WaitForImage(ImageURL, Timeout := 3000, coord_group := "None", shade_variance:=20) {
    SplitPath ImageURL, &ImageName
    if coord_group = "None" {
        x1:= 0
        y1:= 0
        x2:= A_ScreenWidth
        y2:= A_ScreenHeight
    }
    else {
        x1:= coord_group.x1
        y1:= coord_group.y1
        x2:= coord_group.x2
        y2:= coord_group.y2
    }
    
    ; Store the current tick count
    StartTime := A_TickCount
                                                                                                ToolTip "6. WaitForImage: waiting on:`n" ImageName, X_TOOLTIP.6, Y_TOOLTIP.6, 6
    ; Keep checking until timeout has passed
    while (A_TickCount - StartTime) < Timeout {
        ; Check for the image
        if ImageExists(ImageURL, x1, y1, x2, y2, shade_variance) {
            return true
        }
        ; Sleep for a short period to not hog the CPU
        Sleep 10
    }
                                                                                                ToolTip "6. WaitForImage: Didn't find:`n" ImageName, X_TOOLTIP.6, Y_TOOLTIP.6, 6
    ; If we've reached here, timeout has hit without detecting the image 
    return false
}

; This function waits for an array of images, and an optional timeout (default is 3s)
WaitForAnyImages(ImageURLs, Timeout := 3000, coord_group := "None") {
    if coord_group = "None" {
        x1:= 0
        y1:= 0
        x2:= A_ScreenWidth
        y2:= A_ScreenHeight
    }
    else {
        x1:= coord_group.x1
        y1:= coord_group.y1
        x2:= coord_group.x2
        y2:= coord_group.y2
    }

    ; Store the current tick count
    StartTime := A_TickCount

    ; Concatenate image names for tooltip
    imageNames := ""
    for index, imageURL in ImageURLs {
        SplitPath imageURL, &ImageName
        imageNames .= ImageName "`n"
    }
                                                                ToolTip "6. WaitForAnyImages: waiting on:`n" imageNames, X_TOOLTIP.6, Y_TOOLTIP.6, 6

    ; Keep checking until timeout has passed
    while (A_TickCount - StartTime) < Timeout {
        ; Check for the images
        for index, imageURL in ImageURLs {
            if ImageExists(imageURL, x1, y1, x2, y2) {
                return true
            }
        }

        ; Sleep for a short period to not hog the CPU
        Sleep 10
    }

                                                                ToolTip "6. WaitForAnyImages: Didn't find:`n" imageNames, X_TOOLTIP.6, Y_TOOLTIP.6, 6

    ; If we've reached here, timeout has hit without detecting any of the images
    return false
}

; This function waits for an array of images, and an optional timeout (default is 3s)
WaitForAllImages(ImageURLs, Timeout := 3000, coord_group := "None") {
    if coord_group = "None" {
        x1:= 0
        y1:= 0
        x2:= A_ScreenWidth
        y2:= A_ScreenHeight
    }
    else {
        x1:= coord_group.x1
        y1:= coord_group.y1
        x2:= coord_group.x2
        y2:= coord_group.y2
    }

    ; Store the current tick count
    StartTime := A_TickCount

    ; Keep checking until timeout has passed
    while (A_TickCount - StartTime) < Timeout {
        allImagesFound := true ; Assume all images are found

        ; Concatenate image names for tooltip
        imageNames := ""
        ; Check for the images
        for index, imageURL in ImageURLs {
            SplitPath imageURL, &ImageName
            imageNames .= ImageName "`n"
            if !ImageExists(imageURL, x1, y1, x2, y2) {
                allImagesFound := false ; If any image is not found, set flag to false
                break ; No need to check further images
            }
        }

        if allImagesFound {
            ToolTip "6. WaitForAllImages: Found all:`n" imageNames, X_TOOLTIP.6, Y_TOOLTIP.6, 6
            return true ; If all images are found, return true
        }

        ; Sleep for a short period to not hog the CPU
        Sleep 10
    }

    ToolTip "6. WaitForAllImages: Didn't find all:`n" imageNames, X_TOOLTIP.6, Y_TOOLTIP.6, 6

    ; If we've reached here, timeout has hit without detecting all of the images
    return false
}


; Function to check if the ImageURL is present in the window
ImageExists(ImageURL, x1:=0,y1:=0, x2:=A_ScreenWidth,y2:=A_ScreenHeight, shade_variance:=20) {
    CoordMode "ToolTip", "Screen"
    CoordMode "Pixel"
    shade_variation := 90

    SplitPath ImageURL, &ImageName
    
    try {
        ; Search for the image on the entire screen with variation tolerance of shade_variance
        if ImageSearch(&FoundX, &FoundY, x1, y1, x2, y2, "*" shade_variance " *TransBlack " ImageURL) { 
                                                                                                                    ToolTip "7. ImageExists: checking for: `n" ImageName " WAS found! @" FoundX " & " FoundY , X_TOOLTIP.7, Y_TOOLTIP.7, 7
            return true
        } else {
                                                                                                                    ToolTip "7. ImageExists: checking for: `n" ImageName " was NOT found!", X_TOOLTIP.7, Y_TOOLTIP.7, 7
        }
    } catch as exc {
                                                                                                                    ToolTip "7. ImageExists: Could not conduct the search due to the following error:`n" exc.Message " > " ImageURL, X_TOOLTIP.7, Y_TOOLTIP.7, 7
    }

    return false
}


PixelSearchAndClick(PixelColor, scanAreaInput:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0, shade_variance:=0)
{
    menu_width := 140
    
    if scanAreaInput != 0
    {
        scanArea := GetScanArea(scanAreaInput)
    }
    else
    {
        scanArea := {
            x1: x1, y1: y1, 
            x2: x2, y2: y2
        }
    }

    if WinActive(runelite_window)
    {
        ; delays should be randomized often
        set_random_delays()
        
        if PixelSearch(&foundX, &foundY,
                        scanArea.x1, scanArea.y1,
                        scanArea.x2, scanArea.y2, 
                        PixelColor, shade_variance ) {
                                                                                          ToolTip "8. PixelSearchAndClick: " PixelColor " was found at: (" foundX ", " foundY ")", X_TOOLTIP.8, Y_TOOLTIP.8, 8
            ;depending on what area we are clicking, the offset will be different
            offsetObj := GetOffset(offset) ;TODO separate this into GetPixelOffset / GetImageOffset?
            
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            
            ClickOffset(click_type, offsetX, offsetY)
            return true
        }
    }
    return false
}

ImageSearchAndClick(ImageURL, scanAreaInput:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0, shade_variance:=50)
{
    menu_width := 140
    
    if scanAreaInput != 0
    {
        scanArea := GetScanArea(scanAreaInput)
    }
    else
    {
        scanArea := {
            x1: x1, y1: y1, 
            x2: x2, y2: y2
        }
    }
    
    SplitPath ImageURL, &ImageName
    
    if WinActive(runelite_window)
    {
        ; delays should be randomized often
        set_random_delays()
        
        if (ImageSearch(&foundX, &foundY,
                        scanArea.x1, scanArea.y1,
                        scanArea.x2, scanArea.y2, 
                        "*" shade_variance " *TransBlack " ImageURL)
        or ImageSearch(&foundX, &foundY,
                        scanArea.x1, scanArea.y1,
                        scanArea.x2, scanArea.y2, 
                        "*" shade_variance " " ImageURL))
        {
                                                                                          ToolTip "8. ImageSearchAndClick: Looking for:`n" ImageName " was found at: (" foundX ", " foundY ")", X_TOOLTIP.8, Y_TOOLTIP.8, 8
            ;depending on what type of image, the offset will be different
            offsetObj := GetOffset(offset)
            
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            
            ClickOffset(click_type, offsetX, offsetY)
            return true
        }
    }
    return false
}

GetScanArea(scan_area := 0)
{
    menu_width := 0
    ; adjusted window width to not include menu.. clashes with the menu width adjustment though :\
    gameWindowWidth := A_ScreenWidth - 20
    switch scan_area
    {
        case "top_left":
            scan_area_obj := {
                x1: 0, y1: 22,
                x2: 190, y2: 75
            }
            menu_width := 0
            
        case "bag":
            scan_area_obj := {
                x1: 1645, y1: 700,
                x2: 1855, y2: 1000
            }
            menu_width += 100
            
        case "chat_all":
            scan_area_obj := {
                x1: 3, y1: 872,
                x2: 494, y2: 986
            }
            menu_width := 0

        case "chat_bottom":
            scan_area_obj := {
                x1: 3, y1: 969,
                x2: 494, y2: 986
            }
            menu_width := 0

        case "chat_bottom_2":
            scan_area_obj := {
                x1: 3, y1: 958,
                x2: 510, y2: 1015
            }
            menu_width := 0
            
        case "middle":
            scan_area_obj := {
                x1: 0, y1: 200,
                x2: 1650, y2: 970
            }
            menu_width := 0

        case "center":
            scan_area_obj := {
                x1: A_ScreenWidth / 4, y1: A_ScreenHeight /4,
                x2: A_ScreenWidth * 3 / 4, y2: A_ScreenHeight * 3 / 4
            }
            menu_width := 0
            
        case "bank":
            scan_area_obj := {
                x1: 575, y1: 50, 
                x2: 1060, y2: 850
            }

        case "under_mouse":
            MouseGetPos(&x, &y)
            scan_area_obj := {
                x1: x - 130, y1: y - 10,
                x2: x + 120, y2: y + 255
            } 
            menu_width := 0
        
        case "p1":
            scan_area_obj := {
                x1:0, y1:20, 
                x2:A_ScreenWidth / 3, y2:A_ScreenHeight / 2
            } 
            menu_width := 0
        case "p2":
            scan_area_obj := {
                x1:A_ScreenWidth / 3, y1:20,
                x2:A_ScreenWidth * 2 / 3, y2:A_ScreenHeight / 2
            } 
            menu_width := 0
        case "p3":
            scan_area_obj := {
                x1:A_ScreenWidth * 2 / 3, y1:20,
                x2:A_ScreenWidth - 20, y2:A_ScreenHeight / 2
            } 
            menu_width := 0
        case "p4":
            scan_area_obj := {
                x1:0, y1:A_ScreenHeight / 2,
                x2:A_ScreenWidth / 3, y2:A_ScreenHeight - 50
            } 
            menu_width := 0
        case "p5":
            scan_area_obj := {
                x1:A_ScreenWidth / 3, y1:A_ScreenHeight / 2,
                x2:A_ScreenWidth * 2 / 3, y2:A_ScreenHeight - 50
            } 
            menu_width := 0

        case "p6":
            scan_area_obj := {
                x1:A_ScreenWidth * 2 / 3, y1:A_ScreenHeight / 2,
                x2:A_ScreenWidth - 20, y2:A_ScreenHeight - 50
            } 
            menu_width := 0

        default:
            scan_area_obj := {
                x1: 0, y1: 20, 
                x2: A_ScreenWidth-20, y2: A_ScreenHeight-50
            }
            menu_width := 0
    }
    if menu_is_open()
    {
        scan_area_obj.x1 -= menu_width
        scan_area_obj.x2 -= menu_width
    }
    return scan_area_obj
}

GetOffset(offset_item)
{
    switch offset_item {
        ;"option" refers to when you "right" click in-game, the top "left" of the image is 0,0
        case "option":
            ;we want to move mouse to the right 52 to 92 pixels to click more in the center of the image
            horizontal := Random(0, 200)
            ;we want to move mouse down 2 to 11 pixels to click randomly within the image
            vertical := Random(1, 10)

        ;"option_short" refers to when the right click menu is half sized from the usual
        case "option_short":
            ;we want to move mouse horizontally to click more in the center of the image
            horizontal := Random(-1, 100) ;30
            ;we want to move mouse down vertical pixels to click randomly within the image
            vertical := Random(-2, 5)

        ;"item" refers to an item in the bag, also works for fishing spot indicators
        case "item":
            ;item pictures are cut so that the"middle" of the image is the starting point
            horizontal := Random(5, 15)
            vertical := Random(5, 15)
        
        case "tile":
            horizontal := Random(-50, 50)
            vertical := Random(-50, 50)

        case "tile_sw":
            horizontal := Random(-50, 0)
            vertical := Random(0, 50)

        case "tile_se":
            horizontal := Random(20, 100)
            vertical := Random(20, 100)

        case "tile_se_reduced":
            horizontal := Random(15, 40)
            vertical := Random(15, 40)

        case "south":
            horizontal := Random(0, 0)
            vertical := Random(10, 30)

        case "southish":
            horizontal := Random(-15, 15)
            vertical := Random(20, 80)

        case "minimap_icon":
            horizontal := Random(0,5)
            vertical := Random(0,5)
            
        ;default is no offset, can be used when searching but not clicking on an image
        default:
            horizontal := 0
            vertical := 0
    }

    offset := {
        x : horizontal, 
        y : vertical
    }

    return offset
}

ClickOffset(click_type, offset_x := 0, offset_y := 0)
{
    switch click_type
    {
        case "right":
            Click("right", offset_x, offset_y)
            
        case "left":
            Click(offset_x, offset_y)
            
        case "mouseover":
            Click(offset_x, offset_y, 0)
            
        case "doubleclick":
            Click(offset_x, offset_y, 2)
            
        case "in_place":
            Click()

        ; otherwise we don't do anything
    }
}
