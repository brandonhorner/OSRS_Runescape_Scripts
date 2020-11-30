;REQUIREMENTS:
; Runelite client
; Change your name in the window names in the code below.
; This was made on a 1920 x 1080 screen size (In Windows) so use the same resolution for now.
; You should have your inventory set up the same as 3_tick_setup.bmp provided if using 3 tick. 
;        Otherwise just keep an empty slot in bottom right corner of your bag.
; You should have fishing icons on. (Fishing in Runelite)
; Zoom all the way out and face north.
; optional: Go to the Camera option in Runelite and enable 'Vertical camera'.
; requires an empty slot in the bottom right of bag


#SingleInstance

CoordMode, Pixel, Screen    ; Starts pixel search at top left of ACTUAL SCREEN, delete if you want to search from top left of WINDOW
CoordMode, Mouse, Screen


; ATTENTION all recorded coordinates should assume there is no menu, image_search_and_click will adjust for the runelite menu being up
global bag_x1 = 1640
global bag_y1 = 700
global bag_x2 = 1855
global bag_y2 = 1000

global last_bagslot_x1 = 1805
global last_bagslot_y1 = 965

global chat_x1 = 0
global chat_y1 = 975
global chat_x2 = 515
global chat_y2 = 1015

global top_left_x1 = 0
global top_left_y1 = 22
global top_left_x2 = 190
global top_left_y2 = 75

global middle_x1 = 0
global middle_y1 = 200
global middle_x2 = 1650
global middle_y2 = 970

global MENU_WIDTH = 140
global MAX_INT = 92233
global NUM_TRIES = 3


global pink_tile := 0xFF00FF

global fishing_spot := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\fishing_spot.bmp"
global fishing_text := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\fishing_text.bmp"
global fishing := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\fishing.bmp"
global herb := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\herb.bmp"
global swamp_tar := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\swamp_tar.bmp"
global salmon := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\salmon.bmp"
global trout := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\trout.bmp"
global bag_is_open := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\bag_is_open.bmp"

^`::
{
    IfWinActive, RuneLite - BinaryBilly
    {
    CheckFishing:
        count := 0
        while (is_fishing())
        {
            ToolTip, we be fishing, 500, 500, 1
            sleep_random(3000, 7000)
            count++
            value := Mod(count, 20)
            if( value = 0 )
            {
                click_closest(fishing_spot)
                ToolTip, 20th iteration of loop, 500, 500, 1
            }
        }
        ToolTip, we aint fishing -- checking if bag is full, 500, 500, 1
        ;if not fishing, check last bag slot
        if (bag_is_full(trout) or bag_is_full(salmon))
        {
            ToolTip, bag was full! dropping fish!, 500, 500, 1
            drop_fish()
        }
        ;back to scan for lobsters to catch
    SearchSpots:
        ToolTip, clicking new fishing spot, 500, 500, 1
        click_closest(fishing_spot)
        sleep_random(4000, 5500)

        Goto, CheckFishing
    }
return
}


^r::
    
return

+`::Reload

^F3::ExitApp


drop_fish()
{
    bag_rows = 7
    bag_columns = 4
    offset_because_menu = 240
    current_bag_slot_x1 = 1684
    current_bag_slot_y1 = 750
    current_bag_slot_x2 = 1720
    current_bag_slot_y2 = 785
    if (menu_is_open())
    {
        Tooltip, menu was open, 0,300
        current_bag_slot_x1 -= %offset_because_menu%
        current_bag_slot_x2 -= %offset_because_menu%
    }

    row = 0
    Loop, %bag_rows%     ;loop over 7 rows of bag
    {
        column = 0
        Loop, %bag_columns% ;loop over 4 columns of bag
        {
            IfWinActive, RuneLite - BinaryBilly
            {
                Send, {Shift Down}
                if(image_search_and_click(trout, "new_area", "left", "item", current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2) = false and image_search_and_click(salmon, "new_area", "left", "item", current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2) = false)
                    ;Tooltip, NOT FOUND: %row%x%column% @ %current_bag_slot_x1%x%current_bag_slot_y1% and %current_bag_slot_x2%x%current_bag_slot_y2%, 0, 300, 2
                ;else
                    ;Tooltip, FOUND: %row%x%column% @ %current_bag_slot_x1%x%current_bag_slot_y1% and %current_bag_slot_x2%x%current_bag_slot_y2%, 0, 500, 3

                current_bag_slot_x1 += 40
                current_bag_slot_x2 += 40
            }
            column ++
        }
        current_bag_slot_x1 -= 160
        current_bag_slot_x2 -= 160
        current_bag_slot_y1 += 35
        current_bag_slot_y2 += 35
        row ++
    }
    Send {Shift Up}
    return true
}

is_fishing()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        if (image_search_and_click(fishing, "top_left"))
            return true
    }
    return false
}

bag_is_full(item)
{
    if (bag_is_open() = false)
    {
        ;open the bag
        SendInput, {F3}
    }
    sleep_random(200, 600)
        
    if(image_search_and_click(item, "new_area", "none", "item", last_bagslot_x1, last_bagslot_y1, bag_x2, bag_y2))
    {
        ;TrayTip,, %last_bagslot_x1%x%last_bagslot_y1% | %bag_x2%x%bag_y2% | %item%
        return true
    }
    return false
    
}

bag_is_open()
{
    IfWinActive, Runelite - BinaryBilly
    {
        image_search_and_click(bag_is_open, top_of_bag_x1, top_of_bag_y1, top_of_bag_x2, top_of_bag_y2, bag_is_open)
        return true
    }
    return false
}

;searches in a square area around the player and expands the search area until an image is found or we are off screen.
click_closest(image_url)
{
    ;how many pixels to expand the search area each iteration
    expansion_integer = 40
    
    ;center of screen, only character is enclosed
    x1 = 925
    y1 = 515
    x2 = 950
    y2 = 540
    
    if(menu_is_open())
    {
        x1 -= %menu_width%
        x2 -= %menu_width%
    }
    count = 0
    while (x2 < A_ScreenWidth and y2 < A_ScreenHeight)
    {
        
        count++

        ;TrayTip,, in while %count%: `r%x1%x%y1%'r       %x2%x%y2% `rIMAGE:%image_url%
        if (image_search_and_click(image_url, "new_area", "left", "item", x1, y1, x2, y2))
        {
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
    ;TrayTip,, returning false (click_closest())
    return false
}




;Search for an image and click on it. If screen area is omitted, then coordinates must be provided. Offset should
;   be "option" if you are clicking on a 'right-click option', "item" if you are clicking around an item image.
;   If click_type = "right", right click, "left" = left click, "mouseover" will move the mouse but doesn't click,
;   "in-place" to click in place.
image_search_and_click(image_url, scan_area:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0)
{
    abort_counter = %NUM_TRIES%
    shade_variation = 0

    switch scan_area
    {
        case "top_left":
            x1 = %top_left_x1%
            y1 = %top_left_y1%
            x2 = %top_left_x2%
            y2 = %top_left_y2%

        case "chat":
            x1 = %chat_x1%
            y1 = %chat_y1%
            x2 = %chat_x2%
            y2 = %chat_y2%

        case "bag":
            x1 = %bag_x1%
            y1 = %bag_y1%
            x2 = %bag_x2%
            y2 = %bag_y2%

        case "middle":
            x1 = %middle_x1%
            y1 = %middle_y1%
            x2 = %middle_x2%
            y2 = %middle_y2%
    }
    if(menu_is_open())
    {
        x1 -= %MENU_WIDTH%
        x2 -= %MENU_WIDTH%
    }
    
RetryImageSearch:
    IfWinActive, RuneLite - BinaryBilly
    {
        ; delays should be randomized often
        set_random_delays()
        
        ImageSearch, found_x, found_y, %x1%, %y1%, %x2%, %y2%, *%shade_variation% %image_url%

        if (ErrorLevel = 2)     ;if the search wasn't able to start
        {
            MsgBox, Could not conduct the search using: %x1%x%y1% | %x2%x%y2% | %image_url%
            Reload
        }

        else if (ErrorLevel = 1)    ;if we can't find the image
        {
            abort_counter--
            if (abort_counter > 0)
            {
                shade_variation += 40
                Goto, RetryImageSearch
            }
            else
            {
                ;Tooltip, Retried %NUM_TRIES% times- bot failed to find: `r%image_url%`rCoords:%x1%x%y1%  |  %x2%x%y2% `rn=%shade_variation% `rIt must be off screen or blocked., 100, 100, 1
                return false
            }
        }
        else
        {
            ;depending on what type of image, the offset will be different
            switch offset
            {
                ;option refers to when you right click in-game, the top left of the image is 0,0
                case "option":
                {
                    ;we want to move mouse to the right 52 to 92 pixels to click more in the center of the image
                    Random, offset_horizontal, 52, 92
                    ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                    Random, offset_vertical, 2, 11
                }
                ;item refers to an item in the bag, also works for fishing spot indicators
                case "item":
                {
                    ;item pictures are cut so that the middle of the image is the starting point
                    Random, offset_horizontal, -10, 10
                    Random, offset_vertical, -10, 10
                }
                default:
                {
                    offset_horizontal = 0
                    offset_vertical = 0
                }
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
                    
                case "in-place":
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
    runelite_menu_test_pixel_x := 1643 
    runelite_menu_test_pixel_y := 25
    runelite_menu_color := 0x282828
    
    IfWinActive, RuneLite - BinaryBilly
    {
        PixelGetColor, color, %runelite_menu_test_pixel_x%, %runelite_menu_test_pixel_y%
        if (color = runelite_menu_color)  ;runelite window is open
            return true
        else
            return false
    }
}

;UNUSED -- TODO: Delete this
exists(image_url, screen_area:=0)
{ 
    switch screen_area
    {
        case "top_left":
        {
            if (image_search_and_click(image_url, "top_left"))
                return true
        }
        case "chat":
        {
            if (image_search_and_click(image_url, "chat"))
                return true
        }
        case "bag":
        {
            if (image_search_and_click(image_url, "bag"))
                return true
        }   
        default:
        {
            if (image_search_and_click(image_url, "middle"))
                return true
        }
    }
    
    return false
}  
; ---------------------- Utilities --------------------------------------------
set_random_delays()
{   
    ;set the dalay of your mouse movement between 20ms and 40ms
    Random, delaySpeed, 30, 55
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
mouse_move_random_offset()
{
    Random, rand_x, -100, 100
    Random, rand_y, -90, 90
    MouseMove, rand_x, rand_y,, R
}