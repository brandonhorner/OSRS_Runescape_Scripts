;REQUIRED:
; Runelite client, change your name in the window names in the code below.
; This was made on a 1920 x 1080 screen size. (In Windows)
; You must set the bot up each time:
;   - your inventory depletes of lobsters.
;   - the target disappears through a wall
; You must have 'Status Bars' in RuneLite on so that your health bar is shown on the left of your bag.
; You must have 'NPC Indicators' highlight color the same as in the script (0xA4FF00).
;OPTIONAL:
; Have your chat turned to "Game" Chat, this would help because we search for phrases in chat box.
#SingleInstance

CoordMode, Pixel, Screen    ; Starts pixel search at top left of ACTUAL SCREEN, delete if you want to search from top left of WINDOW
CoordMode, Mouse, Screen

SetMouseDelay, 80

global bag_x1 = 1385
global bag_y1 = 700
global bag_x2 = 1855
global bag_y2 = 1000

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

global num_of_tries = 5

global enemy_color := 0xA4FF00  ;some green color

global attack := "images\attack_top_left.bmp"
global failed_pickpocket := "images\failed_pickpocket.bmp"
global glancing_blow := "images\glancing_blow.bmp"
global knockout_option := "images\knockout_option.bmp"
global pickpocket_option := "images\pickpocket_option.bmp"
global cooked_lobster := "images\cooked_lobster.bmp"
global open_bag := "images\open_bag.bmp"
global unconscious := "images\unconscious.bmp"
global cannot_knockout := "images\cannot_do_that.bmp"
global healthbar := "images\healthbar.bmp"
global stunned := "images\stunned.bmp"
global missed_right_click := "images\missed_right_click.bmp"
global combat := "images\combat.bmp"
global money_bag := "images\money_bag.bmp"

global runelite_window := "RuneLite - BinaryBilly"


^`::
    tooltip_x = 600
    tooltip_y = 550
Start:
IfWinActive, %runelite_window%
{
    if (health_is_okay() = false)
    {
        ToolTip, Health is not okay...!, 600, 500, 1
        if (eat_lobster())
        {
            ToolTip, Eating lobster..., %tooltip_x%, %tooltip_y%, 2
            click_money_bag()
            ToolTip, eat_lobster() was true... `rGoing back to start, %tooltip_x%, 600, 3
            Goto, Start
        }
        else
        {
            MsgBox, Reload your inventory with lobsters!
            return
        }
    }
    ToolTip, Health is okay!, 600, 500, 1
Knockout:

    ToolTip, Right clicking on bandit(1)..., %tooltip_x%, %tooltip_y%, 2
    right_click_bandit()
    ToolTip, Clicking knockout..., %tooltip_x%, %tooltip_y%, 2
    click_knockout()
    if (exists("chat", stunned))
    {
        sleep_random(1900, 2300)
        ToolTip, We are stunned...`r...waiting 2 seconds., %tooltip_x%, %tooltip_y%, 2
        Goto, Start
    }
    ;if (exists("chat", cannot_knockout)) 
    ;{
    ;    ToolTip, Cannot knockout bandit right now...`r...waiting 2 seconds., %tooltip_x%, %tooltip_y%, 2 
    ;    sleep_random(1800, 2000)
    ;    ToolTip, cannot_knockout() exists `rGoing back to start, %tooltip_x%, 600, 3
    ;    Goto, Start
    ;}
    
    ToolTip, Right clicking bandit (2)..., %tooltip_x%, %tooltip_y%, 2    
    right_click_bandit()
    sleep_random(80,120)
    ToolTip, Clicking pickpocket(1)..., %tooltip_x%, %tooltip_y%, 2
    click_pickpocket()
    
PostPickpocket:
    ;if we glancing blow
    if (exists("chat", glancing_blow))
    {   
        ToolTip, Glancing blow...`rWaiting 4.8-6sec, %tooltip_x%, %tooltip_y%, 2
        sleep_random(4800,6800)
    }
    else if (exists("chat", unconscious))
    {
        sleep_random(100,130)
        ;second pickpocket
        ToolTip, Right clicking bandit (3)..., %tooltip_x%, %tooltip_y%, 2   
        right_click_bandit()
        ToolTip, Clicking pickpocket (2)..., %tooltip_x%, %tooltip_y%, 2
        click_pickpocket()
    }
    ToolTip, else of PostKnockout`rGoing back to start, %tooltip_x%, 600, 3
    Goto, Start
}    
return
^r::

return

+`::Reload

^F1::ExitApp

;TODO: NOT TESTED WITH MENU OPEN
click_money_bag()
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
        
        ;if (menu_is_open())
        ;{
        ;    current_bag_slot_x1 -= %offset_because_menu%
        ;    current_bag_slot_x2 -= %offset_because_menu%
        ;}

        row = 0
        Loop, %bag_rows%     ;loop over 7 rows of bag slots
        {
            column = 0
            Loop, %bag_columns% ;loop over 4 columns of bag slots
            {
                IfWinActive, %runelite_window%
                {
                    image_search_and_click(current_bag_slot_x1, current_bag_slot_y1, current_bag_slot_x2, current_bag_slot_y2, money_bag, "left", "item")
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
    }
    return true
}

eat_lobster()
{        
    open_bag()
    if (image_search_and_click(bag_x1, bag_y1, bag_x2, bag_y2, cooked_lobster, "left", "item"))
       ;TrayTip,, returning true to eat lobster
       return true
    
    ;TrayTip,, returning false to eat lobster
    return false
}

health_is_okay()
{
    ImageSearch, x, y, 1400, 820, 1850, 850, %healthbar%
    if (ErrorLevel = 2)
    {
        MsgBox Could not conduct the search.
        return false
    }
    else if (ErrorLevel = 1)
        return false
    else
        return true
}

click_knockout()
{    
    counter = %num_of_tries%
    while (counter > 0)
    {
        if (!exists("middle", knockout_option))
        {
            sleep_random(10, 20)
        }
        else
        {
            ;TrayTip,, clicking knockout
            image_search_and_click(middle_x1, middle_y1, middle_x2, middle_y2, knockout_option, "left", "option")
            return true
        }
        counter --
    }
    return false
}

click_pickpocket()
{    
    counter = 2
    while (counter > 0)
    {
        if (!exists("middle", pickpocket_option))
        {   
            sleep_random(10, 20)
        }
        else
        {
            ;TrayTip,, clicking pickpocket
            image_search_and_click(middle_x1, middle_y1, middle_y2, middle_x2, pickpocket_option, "left", "option")
            return true
        }
        counter --
    }
    return false
}

;searches in a square area around the player and expands the search area until an image is found or we are off screen.
right_click_bandit()
{
    IfWinActive, %runelite_window%
    {
        ;how many pixels to expand the search area each iteration
        expansion_integer = 100
        menu_offset = 140
        Random, offset_x, 200, 700
        Random, offset_y, 200, 700
        ;center of screen, only character is enclosed
        x1 = 925
        y1 = 515
        x2 = 950
        y2 = 540
        
        while (x2 < A_ScreenWidth and y2 < A_ScreenHeight)
        {
        TryAgain:
            ;TrayTip,, in while %count%: `r%x1%x%y1%'r%x2%x%y2% `rIMAGE:%image_url%
            if (pixel_search_and_click(x1, y1, x2, y2, enemy_color, "right"))
                sleep_random(100, 200)
                if (!exists("middle", pickpocket_option))
                {
                    SetMouseDelay, 20
                    MouseMove, %offset_x%, %offset_y%
                    Goto, TryAgain
                }
            else    ;grow search area
            {
                x1 -= %expansion_integer%
                y1 -= %expansion_integer%
                x2 += %expansion_integer%
                y2 += %expansion_integer%
            }
            return true
        }
    }
    return false
}

  
exists(image_area, image_url)
{
    ;options in the top left are good for verification before an action.  
    switch image_area
    {
        ;change coordiantes to chat top left area
        case "top_left":
        {
            x1 = %top_left_x1%
            y1 = %top_left_y1%
            x2 = %top_left_x2%
            y2 = %top_left_y2%
        }
        ;change coordiantes to chat window area
        case "chat":
        {
            x1 = %chat_x1%
            y1 = %chat_y1%
            x2 = %chat_x2%
            y2 = %chat_y2%
        }
        ;default to middle of screen coordiantes
        default:
        {
            x1 = %middle_x1%
            y1 = %middle_y1%
            x2 = %middle_x2%
            y2 = %middle_y2%
        }
    }
    
    if (image_search_and_click(x1, y1, x2, y2, image_url, 0, 0))
        return true
    return false
}  
    


;Search for an image and click on it. If modifier = "right", right click,
;    "mouseover" will move the mouse but doesn't click, otherwise left click.
image_search_and_click(x1, y1, x2, y2, image_url, modifier, offset)
{
    abort_counter = 5
    n = 0

Retry:
    IfWinActive, %runelite_window%
    {
        ; delays should be randomized often
        set_random_delays()

        ; search for the image                         *40 means 40 shades away from the picture's color
        ImageSearch, found_x, found_y, x1, y1, x2, y2, *%n% %image_url%
        if (ErrorLevel = 2)
        {
            ToolTip, Could not conduct the search using: %x1%x%y1% | %x2%x%y2% | %image_url%, 0, 100, 6
            return false
        }

        else if (ErrorLevel = 1)
        {
            ;mouse_move_random_offset()
            abort_counter--
            if (abort_counter > 0)
            {
                n += 20
                Goto, Retry
            }
            else
            {
                ;ToolTip, Retried 5 times- bot failed to find: `r%image_url%`rCoords:%x1%x%y1%  |  %x2%x%y2% `rn=%n% `rIt must be off screen or blocked., 0, 100, 6
                return false
            }
        }
        else
        {
            ;option refer to when you right click in-game, the top left of the image is 0,0
            if (offset = "option")
            {
                ;we want to move mouse to the right 52 to 92 pixels to click more in the center of the image
                Random, offset_horizontal, 72, 98
                ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                Random, offset_vertical, 2, 11
            }
            else if (offset = "item")
            {
                Random, offset_horizontal, -10, 10
                Random, offset_vertical, -10, 10
            }
            else
            {
                Random, offset_horizontal, 0, 0
                Random, offset_vertical, -0, 0
            }
            ;TrayTip,, Found: `r%image_url%`rCoords Searched:%x1%x%y1%  |  %x2%x%y2% `r Found at %found_x%x%found_y%
            offset_x := found_x + offset_horizontal
            offset_y := found_y + offset_vertical
            if (modifier = "right")
                Click, right, %offset_x%, %offset_y%
            if (modifier = "mouseover")
                MouseMove, %offset_x%, %offset_y%
            if (modifier = "doubleclick")
                Click, %offset_x%, %offset_y%, 2
            if (modifier = "left")
                Click, %offset_x%, %offset_y%
            ;otherwise we do not click and simply return
            return true
        }
    }
    return false
}

;Set the color of a tile in game and use that as the pixel color. if modifier = "right", right click,
;    "mouseover" will move the mouse but doesn't click, "doubleclick" clicks twice in the same spot.
;     Otherwise left click.
pixel_search_and_click(x1, y1, x2, y2, pixel_color, modifier)
{
    IfWinActive, %runelite_window%
    {     
        ;delays should be randomized frequently
        set_random_delays()
        
        PixelSearch, found_x, found_y, x1, y1, x2, y2, pixel_color, 0, RGB fast ;search region for color
        if ErrorLevel
        {
            ;TrayTip,, The color %pixel_color% was not found in region.,1 
            return
        }
        else
        {
            ;TrayTip,, The color %pixel_color% was found at x%found_x% and y%found_y%
            
            ;these magic numbers are about the size of the tile to be clicked into, they might need to be adjusted
            ;  depending on how small the object inside of the tile is.
            Random, offset_tile_x, 0, 5
            Random, offset_tile_y, -10, -20 
            offset_x := found_x + offset_tile_x
            offset_y := found_y + offset_tile_y
            
            if (modifier = "right")
                Click, right, %offset_x%, %offset_y%
            else if (modifier = "mouseover")
                MouseMove, %offset_x%, %offset_y%
            else if (modifier = "doubleclick")
            {
                Click, %offset_x%, %offset_y%, 2
            }
            if (modifier = "left")
                Click, %offset_x%, %offset_y%
            ;otherwise we do not click and simply return
            return true
        }
    }
    return false
}


;check to see if bag is open
open_bag()
{
    IfWinActive, %runelite_window%
    {
        ImageSearch, found_x, found_y,  top_of_bag_x1, top_of_bag_y1, top_of_bag_x2, top_of_bag_y2, %open_bag%
        if (ErrorLevel = 2)
            MsgBox Error: In open_bag() -- Could not conduct the search.
        else if (ErrorLevel = 1)
        {
            ; open bag was not found
            SendInput, {F3} 
            return true
        }
        else
        {
            ; open bag found
            return true
        }
    }
    return false
}

; ---------------------- Utilities --------------------------------------------
set_random_delays()
{   
    ;set the dalay of your mouse movement between 20ms and 40ms
    Random, delaySpeed, 40, 43
    SetMouseDelay, %delaySpeed%
    
    Random, key_delay_speed, 80, 190
    Random, press_duration, 40, 75
    SetKeyDelay, %key_delay_speed%, %press_duration%
    
}

sleep_random( sleep_time_low, sleep_time_high )
{
    Random, sleep_time, sleep_time_low, sleep_time_high
    Sleep, %sleep_time%
    
    return
}