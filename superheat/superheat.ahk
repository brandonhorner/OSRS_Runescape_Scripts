﻿;Created by Brandon Horner aKa BinaryBilly
;   testing as of 12/13/2020
;   
;REQUIREMENTS CHECKLIST:
;
; 0. Must be using RuneLite client.
;
; 1. Change your name in the window names in the code below.
global runelite_window := "RuneLite - BinaryBilly"
;                                      ^  ^  ^ replace this with your character's name
;
; 2. This was made on a 1920 x 1080 screen. Use the same resolution for now.
;
; 3. In the Mining addon in RuneLite, check 'Show Session Stats'.
;
; 4. Keep an empty slot in the bottom "right" of "bag" (the very corner slot). 
;
; 5. Ardougne Easy Diary cloak must be equipped
;
; 6. Equip a Fire Battlestaff (bot will not pick up fire runes currently).
;
; 7. In your bank, have nature runes and your pickaxe of choice in the first screen.
;
; 8. In the filter on your spellbook menu, turn off "Show spells you lack the runes for".

; Optional: Go to 'Entities' app and turn off entities (for more reliability).
; 

; This script will superheat your ore of choice, until your inventory is empty of that ore.


#SingleInstance
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%\..  ; Ensures a consistent starting directory.

global iron_ore := "image_library\iron_ore.bmp"
global mithril_ore := "image_library\mithril_ore.bmp"
global silver_ore := "image_library\silver_ore.bmp"

;currently we must change iron_ore to whatever ore is desired.
global current_ore := iron_ore

global report_messages := true


^H::
    run_count := 0
    run_limit := 30
                                                            if (report_messages) 
                                                                ToolTip, Setting up character, 500, 500, 1
    ;setup character
    setup()
Start:
    run_count++
    run_limit--
    if (run_limit <= 0)
        return
                                                        if (report_messages) 
                                                            ToolTip, Teleporting to monastery, 500, 500, 1
    ;teleport with ardougne cloak
    teleport_with_cloak()
    sleep_random(5000, 6000)
                                                        if (report_messages) 
                                                            ToolTip, Clicking north iron node--Preparing for mining, 500, 500, 1
    ;start mining
    mine_north_iron_node()
    zoom_in()
    sleep_random(8000, 9500)
                                                         if (report_messages) 
                                                            ToolTip, Beginning mining, 500, 500, 1
    ;Mine until full
    mine_until_full()
    zoom_out()
                                                         if (report_messages) 
                                                            ToolTip, Mining done--taking ore count, 500, 500, 1
    ;count ore in inventory
    num_of_ore := get_ore_count(current_ore)
                                                         if (report_messages) 
                                                            ToolTip, Going to cyan, 500, 500, 1
    ;Go to cyan
    go_to_cyan()
    num_of_ore -= 8
                                                         if (report_messages) 
                                                            ToolTip, Superheating 8 ore, 500, 500, 1
    superheat_ore(current_ore, 8)   
                                                         if (report_messages) 
                                                            ToolTip, Going to green, 500, 500, 1
    ;Go to green
    go_to_green()
    num_of_ore -= 9
                                                         if (report_messages) 
                                                            ToolTip, Superheating 9 ore, 500, 500, 1
    superheat_ore(current_ore, 9)
                                                         if (report_messages) 
                                                            ToolTip, Going to pink, 500, 500, 1
    ;Go to pink
    go_to_pink()
                                                        if (report_messages) 
                                                            ToolTip, Superheating remaining ore, 500, 500, 1
    ;Superheat remaining ore
    superheat_ore(current_ore, num_of_ore)
    zoom_in()
                                                        if (report_messages) 
                                                           ToolTip, Remaking inventory and restarting, 300, 500, 1
    click_bank()
    sleep_random(2000, 3000)
    
    ;deposit smelted ore
    remake_inventory()
    zoom_out()
                                                        if (report_messages) 
                                                           ToolTip, Times run = %run_count%, 300, 400, 2 
    Goto, Start
    return


^G::Reload

^F3::ExitApp

;use for testing
^t::
    click_superheat()
    return
^r::
    ore_count := get_ore_count(current_ore)
    MsgBox, ore count = %ore_count% 
    superheat_ore(current_ore, ore_count)
    return
    
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
zoom_in()
{
    Send, {Wheelup 35}
    return
}

zoom_out()
{
    Send, {Wheeldown 35}
    return
}

click_compass()
{   
    xp_minimap_button := "image_library\xp_minimap_button.bmp"
    
    ImageSearch, found_x, found_y, 0, 0, %A_ScreenWidth%, %A_ScreenHeight%, %xp_minimap_button%
    if (ErrorLevel = 2)
    {
        Tooltip, Could not conduct the search`rsearch area: 0x0 and %A_ScreenWidth%x%A_ScreenHeight%`rimage = %xp_minimap_button%, 100, 500, 20
        return false
    }
    else if (ErrorLevel = 1)
        return false
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

teleport_with_cloak()
{
    ardougne_cloak := "image_library\ardougne_cloak.bmp"
    
    open_equipment()
    ;"right" click ardougne cloak
    image_search_and_click(ardougne_cloak, "bag", "right", "item")
    
    ;"left" click kandarin monastery
    click_kandarin_monastery_menu_option()
    return
}

mine_north_iron_node()
{
    green = 0x00FF4D
    mining_text := "image_library\mining_text.bmp"
    loop_count := 5
    while(loop_count > 0)
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
    return
}

mine_until_full()
{   
    green = 0x00FF4D
    yellow = 0xFFFF00
    
    ;top iron ore search area
    top_x1 := 660 
    top_y1 := 250 
    top_x2 := 1220
    top_y2 := 660 

    ;bottom iron ore search area
    bottom_x1 := 660
    bottom_y1 := 625
    bottom_x2 := 1224
    bottom_y2 := 1020
    
    Random, offset_x, -50, -10
    Random, offset_y, 0, 50
    while(bag_is_full() == false)
    {
        IfWinActive, %runelite_window%
        {
            if (!pixel_search_and_click(top_x1, top_y1, top_x2, top_y2, yellow))
            {
                pixel_search_and_click(top_x1, top_y1, top_x2, top_y2, green, "left", offset_x, offset_y)
                if (report_messages)
                        ToolTip, Mining north iron node, 500, 500, 1
                sleep_random(1000, 1500)
                while (is_mining())
                {
                    sleep_random(100,200)
                }
            }
            if (!pixel_search_and_click(bottom_x1, bottom_y1, bottom_x2, bottom_y2, yellow))
            {
                pixel_search_and_click(bottom_x1, bottom_y1, bottom_x2, bottom_y2, green, "left", offset_x, offset_y)
                if (report_messages) 
                        ToolTip, Mining south iron node, 500, 500, 1
                sleep_random(1000, 1500)
                while (is_mining())
                {
                    sleep_random(100,200)
                }
            }
        }
    }
    if (report_messages)
        ToolTip, Bag is full, 500, 500, 1
}

is_mining()
{
    is_mining := "image_library\is_mining.bmp"
    if (image_search_and_click(is_mining, "top_left"))
        return true
    return false
}

bag_is_full()
{
    last_bag_slot_x1 := 1804
    last_bag_slot_y1 := 960
    last_bag_slot_x2 := 1844
    last_bag_slot_y2 := 995
    
    open_bag()
    if(image_search_and_click(current_ore, 0, 0, 0, last_bag_slot_x1, last_bag_slot_y1, last_bag_slot_x2, last_bag_slot_y2))
        return true
    else
        return false
}

go_to_cyan()
{
    cyan = 0x377372
    pixel_search_and_click(424, 35, 1628, 866, cyan, "left")
    return
}

go_to_green()
{
    green = 0x00FF00
    pixel_search_and_click(424, 35, 1628, 866, green, "left")
    return
}

go_to_pink()
{
    pink = 0xFF00FF
    pixel_search_and_click(424, 35, 1628, 866, pink, "left")
    return
}

click_bank()
{
    teal = 0x00FFFF
    bank_text := "image_library\bank_text.bmp"
    
ClickBank:
    if (pixel_search_and_click(424, 35, 1628, 866, teal, "mouseover"))
    {
        if(image_search_and_click(bank_text, "top_left"))
            Click
        else
            Goto, ClickBank
    }
    return
}

superheat_ore(ore, count)
{
    IfWinActive, %runelite_window%
    {
        open_spellbook()
        while (count > 0)
        {
            click_superheat()

            click_ore(ore)

            count--
        }
    }
    ;if (report_messages) 
    ;   ToolTip, finished superheating, 500, 500, 1
    return
}


click_kandarin_monastery_menu_option()
{
    kandarin_monastery_menu_option := "image_library\kandarin_monastery_menu_option.bmp"
    search_limit = 30
    while(search_limit > 0)
    {
        if(image_search_and_click(kandarin_monastery_menu_option, "under_mouse", "left", "option"))
        {
            ;if (report_messages)
            ;    ToolTip, Clicking Kandarin Monastery "option", 500, 500, 1
            return true
        }
        else
        {
            sleep_random(10,20)
            search_limit --
        }
    }
    return false    
}

click_ore(ore)
{
    search_limit = 30
    while(search_limit > 0)
    {
        if(image_search_and_click(ore, "bag", "left", "item"))
        {
            ;if (report_messages)
            ;    ToolTip, Clicking ore, 500, 500, 1
            return true
        }
        else
        {
            sleep_random(10,20)
            open_bag()
            search_limit --
            mouse_move_random_offset(2, 10, 2, 10)
            mouse_move_random_offset(0, 10, -10, 10)
        }

        if(report_messages) 
            ToolTip, No ore was found, 500, 500, 1
    }
    return false    
}


click_superheat()
{
    superheat := "image_library\superheat.bmp"
    search_limit = 30
    while(search_limit > 0)
    {
        if(image_search_and_click(superheat, "bag", "left", "item"))
        {
            ;if (report_messages)
            ;    ToolTip, Clicking Superheat, 500, 500, 1
            return true
        }
        else
        {
            sleep_random(20,200)
            search_limit --
            mouse_move_random_offset(2, 10, 2, 10)
        }
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


;check to see if "bag" is open, if not then open it
open_bag()
{
    open_bag := "image_library\open_bag.bmp"
    ;if (report_messages)
    ;    ToolTip, Opening bag, 500, 500, 1
    if (!image_search_and_click(open_bag, "bag"))
        SendInput, {F3}
    return
}


;check to see if equipment is open, if not then open it
open_equipment()
{
    open_equipment := "image_library\open_equipment.bmp"
    ;if (report_messages)
        ;ToolTip, Opening equipment, 500, 500, 1
    if (!image_search_and_click(open_equipment, "bag"))
        SendInput, {F4}
    return
}


;check to see if spellbook is open, if not then open it
open_spellbook()
{
    open_spellbook := "image_library\open_spellbook.bmp"
    ;if (report_messages)
        ;ToolTip, Opening spellbook, 500, 500, 1
    if (!image_search_and_click(open_spellbook, "bag"))
        SendInput, {F6}
    return
}


;counts the number of ore in your inventory
get_ore_count(ore)
{
    IfWinActive, %runelite_window%
    {
        open_bag()
        count = 0
        bag_rows = 7
        bag_columns = 4
        offset_because_menu = 242
        current_bag_slot_x1 = 1684
        current_bag_slot_y1 = 750
        current_bag_slot_x2 = 1724
        current_bag_slot_y2 = 785
        
        if (menu_is_open())
        {
            current_bag_slot_x1 -= %offset_because_menu%
            current_bag_slot_x2 -= %offset_because_menu%
        }
        
        ;if (report_messages)
        ;    ToolTip, Getting count of ore, 500, 500, 1
            
        Loop, %bag_rows%     ;loop over the 7 rows of "bag" slots
        {
            Loop, %bag_columns% ;loop over the 4 columns of "bag" slots
            {
                IfWinActive, %runelite_window%
                {
                    if(image_search_and_click(ore,,,, current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2))
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

remake_inventory()
{
    deposit_all_items := "image_library\bank_deposit_all_items.bmp"
    image_search_and_click(deposit_all_items, "bank", "left", "item")
    
    nature_runes := "image_library\nature_runes.bmp"
    adamant_pickaxe := "image_library\adamant_pickaxe.bmp"
    rune_pickaxe := "image_library\rune_pickaxe.bmp"

    ;withdraw necessary items, you can add to this list after adding an image to the directory
    image_search_and_click(nature_runes, "bank", "right", "item")
    click_withdraw_all()
    ;image_search_and_click(rune_pickaxe, "bank", "left", "item")
    
    close_bank := "image_library\exit_bank_button.bmp"
    image_search_and_click(close_bank, "bank", "left", "item")
    return
}

click_withdraw_all()
{
    withdraw_all := "image_library\withdraw_all_menu_option.bmp"
    search_limit = 30
    while(search_limit > 0)
    {
        if(image_search_and_click(withdraw_all, "under_mouse", "left", "option"))
        {
            ;if (report_messages)
            ;    ToolTip, Clicking Withdraw All "option", 500, 500, 1
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

;click_run()
;{
;    xp_minimap_button := "image_library\xp_minimap_button.bmp"
;
;    ImageSearch, found_x, found_y, 0, 0, %A_ScreenWidth%, %A_ScreenHeight%, %xp_minimap_button%
;    Random, x_offset, 11, 55
;    Random, y_offset, 92, 106
;    x_offset += found_x
;    y_offset += found_y
;
;    if (ErrorLevel = 2)
;    {
;        Tooltip, Could not conduct the search`rsearch area: 0x0 and %A_ScreenWidth%x%A_ScreenHeight%`rimage = %xp_minimap_button%, 100, 500, 20
;        return false
;    }
;    else if (ErrorLevel = 1)
;    {
;        Tooltip, Could not find xp minimap button `rsearch area: 0x0 and %A_ScreenWidth%x%A_ScreenHeight%`rimage = %xp_minimap_button%, 100, 500, 20
;        return false
;    }
;    else
;    {
;
;        Click, left, %x_offset%, %y_offset%
;    }
;}

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