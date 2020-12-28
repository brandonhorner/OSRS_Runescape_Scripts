;Created by Brandon Horner aKa BinaryBilly
;   testing as of 11/29/2020
;   
;REQUIREMENTS CHECKLIST:
;
; 0. Must be using RuneLite client.
;
; 1. Change your name in the window names in the code below.
global runelite_window := "RuneLite - BinaryBilly"
;                                      ^  ^  ^ replace this with your character's name

; 2. This was made on a 1920 x 1080 screen. Use the same resolution for now.
;
; 3. You should have fishing icons on.
;   - Click wrench at top "right" of RuneLite. Go to 'Fishing' app settings.
;
; 4. Zoom all the way out so you can see all of the spawns and face north (click compass).  
;
; 5. Go to the top spawns (only spot I tested).
;
; 6. Keep an empty slot in the bottom "right" of "bag" (the very corner slot). 
;
; 7. You should have a barbarian fishing harpoon and some bait (10k feathers will easily last overnight).
;
; 8. Go to 'Entities' app and turn off entities. (I have seen a fishing pole cover the spawn image before).
; Optional: Go to the 'Camera' app in RuneLite and enable 'Vertical camera'.
;
; 

#SingleInstance
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

CoordMode, Pixel, Screen    ; Starts pixel search at top left of ACTUAL SCREEN, delete if you want to search from top left of WINDOW
CoordMode, Mouse, Screen

;TODO: finish support for menu being open

global salmon := "images\salmon.bmp"
global trout := "images\trout.bmp"
global sturgeon := "images\sturgeon.bmp"
global report_errors := 0

^H::
{
    main_tooltip_x1 = 700
    main_tooltip_y1 = 500
    run_count := 0

CheckFishing:
    IfWinActive, %runelite_window%
    {
        while (is_fishing())
        {
            ToolTip, %run_count%. We be fishin'..., %main_tooltip_x1%, %main_tooltip_y1%, 1
            sleep_random(3000, 10000)
            value := Mod(run_count, 10)
            if( value = 0 )
            {
                ToolTip, pause 1-1.5 minutes, %main_tooltip_x1%, %main_tooltip_y1%, 1
                sleep_random(60000, 90000)
                ToolTip, %run_count%. Waiting extra time (3-10 sec), %main_tooltip_x1%, %main_tooltip_y1%
                sleep_random(3000, 10000)
            }
        }
        ToolTip, We aren't fishing. `rChecking if "bag" is full..., %main_tooltip_x1%, %main_tooltip_y1%, 1
        ;if not fishing, check last "bag" slot to see if full
        if (bag_is_full(trout) or bag_is_full(salmon) or bag_is_full(sturgeon))
        {
            run_count++
            ToolTip, Bag was filled %run_count% time(s).`r...Dropping fish, %main_tooltip_x1%, %main_tooltip_y1%, 1
            drop_fish()
            if (run_count >= 140)
                return
        }
        ;scan for fish to catch
        ToolTip, Clicking new fishing spot..., %main_tooltip_x1%, %main_tooltip_y1%, 1
        click_closest(sturgeon)
        sleep_random(4000, 5500)

        Goto, CheckFishing
    }
    
return
}


^G::Reload

^F3::ExitApp


drop_fish()
{
    IfWinActive, %runelite_window%
    {
        bag_rows = 7
        bag_columns = 4
        offset_because_menu = 240
        current_bag_slot_x1 = 1684
        current_bag_slot_y1 = 750
        current_bag_slot_x2 = 1724
        current_bag_slot_y2 = 785
        
;        if (menu_is_open())
;        {
;            current_bag_slot_x1 -= %offset_because_menu%
;            current_bag_slot_x2 -= %offset_because_menu%
;        }

        Loop, %bag_rows%     ;loop over 7 rows of "bag" slots
        {
            Loop, %bag_columns% ;loop over 4 columns of "bag" slots
            {
                IfWinActive, %runelite_window%
                {
                    Send, {Shift Down}
                    image_search_and_click(trout,, "left", "item", current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2)
                    image_search_and_click(salmon,, "left", "item", current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2)
                    image_search_and_click(sturgeon,, "left", "item", current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2)
                    current_bag_slot_x1 += 40
                    current_bag_slot_x2 += 40
                }
            }
            current_bag_slot_x1 -= 160
            current_bag_slot_x2 -= 160
            current_bag_slot_y1 += 35
            current_bag_slot_y2 += 35
        }
    }
    Send {Shift Up}
    
    return true
}

is_fishing()
{
    is_fishing := "images\is_fishing.bmp"
    IfWinActive, %runelite_window%
    {
        if (image_search_and_click(is_fishing, "top_left"))
            return true
    }
    return false
}

bag_is_full(item)
{
    IfWinActive, %runelite_window%
    {
        last_bagslot_x1 = 1805
        last_bagslot_y1 = 965
        bag_x2 = 1855
        bag_y2 = 1000
        
        if (bag_is_open() = false)
        {
            ;open the "bag"
            SendInput, {F3}
        }
        sleep_random(200, 600)

        if(image_search_and_click(item, "new_area", 0, "item", last_bagslot_x1, last_bagslot_y1, bag_x2, bag_y2))
        {
            ;TrayTip,, %last_bagslot_x1%x%last_bagslot_y1% | %bag_x2%x%bag_y2% | %item%
            return true
        }
    }
    return false 
}

bag_is_open()
{
    bag_is_open := "images\open_bag.bmp"
    IfWinActive, %runelite_window%
    {
        if  (image_search_and_click(bag_is_open, "bag"))
            return true
        return false
    }
    return false
}

;searches in a square area around the player and expands the search area until an image is found or we are off screen.
click_closest(image_url)
{
    IfWinActive, %runelite_window%
    {
        ;how many pixels to expand the search area each iteration
        expansion_integer = 40
        ;center of screen, only character is enclosed
        x1 = 925
        y1 = 515
        x2 = 950
        y2 = 540
        
        while (x2 < A_ScreenWidth and y2 < A_ScreenHeight)
        {
            if (image_search_and_click(image_url, "new_area", "left", "item", x1, y1, x2, y2, "slow"))
            {
                mouse_move_random_offset()
                return true
            }
            else    ;grow search area
            {
                x1 -= %expansion_integer%
                y1 -= %expansion_integer%
                x2 += %expansion_integer%
                y2 += %expansion_integer%
            }
        }
    }
    ;TrayTip,, returning false (click_closest())
    return false
}



;Search for an image and click on it. If screen area is omitted, then coordinates must be provided. Offset should
;   be option if you are clicking on a '"right"-click option', item if you are clicking around an item image.
;   If click_type = "right", "right" click, "left" = left click, "mouseover" will move the mouse but doesn't click,
;   in_place to click in place. Function will search 
image_search_and_click(image_url, scan_area:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0, delay:="fast")
{
    menu_width = 140
    search_counter = 3
    shade_variation = 0

    switch scan_area
    {
        case "top_left":
            x1 = 0
            y1 = 22
            x2 = 190
            y2 = 120
            
        case "bag":
            x1 = 1645
            y1 = 700
            x2 = 1855
            y2 = 1000
            
        case "chat":
            x1 = 0
            y1 = 975
            x2 = 510
            y2 = 1015

        case "middle":
            x1 = 0
            y1 = 200
            x2 = 1650
            y2 = 970
    }
    if(menu_is_open())
    {
        x1 -= %menu_width%
        x2 -= %menu_width%
    }
    
RetryImageSearch:
    IfWinActive, %runelite_window%
    {
        ; delays should be randomized often
        if (delay = "slow")
        {
            set_random_delays(45, 85)
        }
        else
        {
            set_random_delays(15, 30)
        }
        ImageSearch, found_x, found_y, %x1%, %y1%, %x2%, %y2%, *%shade_variation% %image_url%

        if (ErrorLevel = 2)     ;if the search wasn't able to start
        {
            MsgBox, Could not conduct the search using: %x1%x%y1% | %x2%x%y2% | %image_url%
            Reload
        }

        else if (ErrorLevel = 1)    ;if we can't find the image
        {
            search_counter--
            if (search_counter > 0)
            {
                shade_variation += 40
                Goto, RetryImageSearch
            }
            else
            {
                if (report_errors)
                    Tooltip, Retried too many times- bot failed to find: `r%image_url%`rCoords:%x1%x%y1%  |  %x2%x%y2% `rn=%shade_variation% `rIt must be off screen or blocked., 100, 200, 4
                return false
            }
        }
        else
        {
            ;depending on what type of image, the offset will be different
            switch offset
            {
                ;option refers to when you "right" click in-game, the top left of the image is 0,0
                case "option":
                {
                    ;we want to move mouse to the "right" 52 to 92 pixels to click more in the center of the image
                    Random, offset_horizontal, 52, 92
                    ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                    Random, offset_vertical, 2, 11
                }
                ;item refers to an item in the "bag", also works for fishing spot indicators
                case "item":
                {
                    ;item pictures are cut so that the"middle" of the image is the starting point
                    Random, offset_horizontal, -10, 10
                    Random, offset_vertical, -10, 10
                }
                default:
                {
                    offset_horizontal = 0
                    offset_vertical = 0
                }
            }
            
            if (report_errors)
                    Tooltip, Found: `r%image_url%`rCoords Searched:%x1%x%y1%  |  %x2%x%y2% `r Found at %found_x%x%found_y%, 100, 100, 5
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

menu_is_open()
{
    closed_runelite_menu := "images\closed_runelite_menu.bmp"
    ImageSearch, dummy_x, dummy_y, 0, 0, %A_ScreenWidth%, %A_ScreenHeight%, %closed_runelite_menu%
    if (ErrorLevel = 2)
    {
        ToolTip, Error: In menu_is_open() -- Could not conduct the search., 100, 400, 20
        return false
    }
    else if (ErrorLevel = 1)
    {
        ; menu was not found to be closed
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
set_random_delays(mouse_delay_low :=15, mouse_delay_high:=35, key_delay_low:=20, key_delay_high:=45, press_duration_low:=20, press_duration_high := 45)
{   
    ;set the delay of your mouse movement in microseconds
    Random, delaySpeed, %mouse_delay_low%, %mouse_delay_high%
    SetMouseDelay, %delaySpeed%
    
    Random, key_delay_speed, %key_delay_low%, %key_delay_high%
    Random, press_duration, %press_duration_low%, %press_duration_high%
    SetKeyDelay, %key_delay_speed%, %press_duration%
    
}
sleep_random( sleep_time_low, sleep_time_high )
{
    Random, sleep_time, sleep_time_low, sleep_time_high
    Sleep, %sleep_time%
    
    return
}

;Move the mouse randomly, offset from the current location
mouse_move_random_offset()
{
    set_random_delays(45, 85)
    Random, rand_x, 30, 100
    Random, rand_y, -90, 90
    MouseMove, rand_x, rand_y,, R
}