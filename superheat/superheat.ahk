;Created by Brandon Horner 12/10/2020
;REQUIRED
; Runelite client, change your name in the window names in the code below.
; This script will superheat your ore of choice, until your inventory is empty of that ore.
; This was made on a 1920 x 1080 screen size. (In Windows).
; Have a lobster pot in the first screen of your bank (turn on Always set placeholders)



#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

global bag_x1 := 1645
global bag_y1 := 700
global bag_x2 := 1855
global bag_y2 := 1000

global iron_ore := "images\iron_ore.bmp"
global mithril_ore := "images\mithril_ore.bmp"
global silver_ore := "images\silver_ore.bmp"

;currently we must change iron_ore to whatever ore is desired.

global runelite_window := "RuneLite - BinaryBilly"

global report_messages := true


^`::
    superheat_ore(iron_ore)
return

superheat_ore(current_ore)
{
    count = get_ore_count(current_ore)
    if( count > 0 )
    {
        IfWinActive, %runelite_window%
        {

            open_bag()
            sleep_random(100,200)
            
            ;if there are ore in your bag
            if (exists(current_ore))
            {
                open_spellbook()
                
            DoWhile:
                click_superheat()
                
                click_ore(current_ore)
                
                mouse_move_random_offset(-250, -150, -500, 50)  ;move mouse out of inventory to avoid blocking ImageSearch
                                                                if(report_messages)ToolTip, Restarting in .5-1 seconds, 500, 500, 1
                sleep_random(500,1000)
                count--
                if ( count > 0 )
                    Goto, DoWhile
            }
        }
    }
    return
}

+`::Reload

^F3::ExitApp

^r::

return


get_ore_count()
{
    IfWinActive, %runelite_window%
    {
        count = 0
        bag_rows = 7
        bag_columns = 4
        offset_because_menu = 240
        current_bag_slot_x1 = 1684
        current_bag_slot_y1 = 750
        current_bag_slot_x2 = 1724
        current_bag_slot_y2 = 785
        
        if (menu_is_open())
        {
            current_bag_slot_x1 -= %offset_because_menu%
            current_bag_slot_x2 -= %offset_because_menu%
        }

        Loop, %bag_rows%     ;loop over the 7 rows of bag slots
        {
            Loop, %bag_columns% ;loop over the 4 columns of bag slots
            {
                IfWinActive, %runelite_window%
                {
                    if(image_search_and_click(current_ore,,, "item", current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2))
                        count ++
                    current_bag_slot_x1 += 40
                    current_bag_slot_x2 += 40
                }
            }
            current_bag_slot_x1 -= 160
            current_bag_slot_x2 -= 160
            current_bag_slot_y1 += 35
            current_bag_slot_y2 += 35
        }
        return count
    }
    return 
}

click_superheat()
{
    superheat := "images\superheat.bmp"
    loop_count = 30
    while(loop_count > 0)
    {
        if(image_search_and_click(superheat, bag, "left", "item"))
        {
            if (report_messages)
                ToolTip, Clicking Superheat, 500, 500, 1
            return true
        }
        else
        {
            sleep_random(10,20)
            loop_max_count --
        }
    }
    return false    
}


click_ore(ore)
{
    loop_count = 30
    while(loop_count > 0)
    {
        if(image_search_and_click(ore, "bag", "left", "item"))
        {
            if (report_messages)
                ToolTip, Clicking %ore%, 500, 500, 1
            return true
        }
        else
        {
            sleep_random(10,20)
            loop_max_count --
        }
        if(report_messages) 
            ToolTip, No %ore% was found, 500, 500, 1
    }
    return false    
}


exists(image_url)
{
    if (image_search_and_click(image_url, "bag", 0, "item"))
    {
        ;ToolTip, exists() was true | %image_url%, 500, 500, 2
        return true
    }
    return false
}


;Search for an image and click on it. If screen area is omitted, then coordinates must be provided. Offset should
;   be "option" if you are clicking on a 'right-click option', "item" if you are clicking around an item image.
;   If click_type = "right", right click, "left" = left click, "mouseover" will move the mouse but doesn't click,
;   "in-place" to click in place. Function will search 
image_search_and_click(image_url, scan_area:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0)
{
    search_counter = 2
    menu_width = 140
    shade_variation = 0
    
    switch scan_area
    {
        case "top_left":
            x1 = 0
            y1 = 22
            x2 = 190
            y2 = 75
            menu_width = 0
            
        case "bag":
            x1 = 1645
            y1 = 700
            x2 = 1855
            y2 = 1000
            menu_width += 100
            
        case "chat":
            x1 = 0
            y1 = 975
            x2 = 510
            y2 = 1015
            menu_width = 0

        case "middle":
            x1 = 0
            y1 = 200
            x2 = 1650
            y2 = 970
            
        default:
            x1 = 0
            y1 = 0
            x2 = %A_ScreenWidth%
            y2 = %A_ScreenHeight%
    }
    
RetryImageSearch:
    IfWinActive, %runelite_window%
    {
        ; delays should be randomized often
        set_random_delays()
        
        ImageSearch, found_x, found_y, %x1%, %y1%, %x2%, %y2%, *%shade_variation% %image_url%
        ;ToolTip, Inside: image_search_and_click() @ImageSearch `r%image_url% was found at %found_x%x%found_y%`r%x1%x%y1% and %x2%x%y2% was the search area, 500, 600, 3
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
                ;Tooltip, Retried %search_counter% times- bot failed to find: `r%image_url%`rCoords:%x1%x%y1%  |  %x2%x%y2% `rn=%shade_variation% `rIt must be off screen or blocked., 100, 100, 1
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
                    ;we want to move mouse to the right 52 to 92 pixels to click more in the center of the image
                    Random, offset_horizontal, 52, 92
                    ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                    Random, offset_vertical, 2, 11

                ;item refers to an item in the bag, also works for fishing spot indicators
                case "item":
                    ;item pictures are cut so that the middle of the image is the starting point
                    Random, offset_horizontal, -8, 8
                    Random, offset_vertical, -8, 8

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
                    
                case "in-place":
                    Click, 0, 0, 0, Rel
            }
            ;otherwise we do not click and simply return
            return true
        }
    }
    return false
}



;check to see if bag is open, if not then open it
open_bag()
{
    open_bag := "images\open_bag.bmp"
    if (report_messages)
        ToolTip, Opening bag, 500, 500, 1
    if (!image_search_and_click(open_bag, "bag"))
        SendInput, {F3}
    return
}

;check to see if bag is open, if not then open it
open_spellbook()
{
    open_spellbook := "images\open_spellbook.bmp"
    if (report_messages)
        ToolTip, Opening spellbook, 500, 500, 1
    if (!image_search_and_click(open_spellbook, "bag"))
        SendInput, {F6}
    return
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
        return true
    }
    else
    {
        ;menu is closed
        return false
    }
}


; ---------------------- Utilities --------------------------------------------
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