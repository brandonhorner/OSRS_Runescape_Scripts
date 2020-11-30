;REQUIRED:
; Runelite client, change your name in the window names in the code below.
; Starts at Wintertodt bank chest, doesn't matter what your inventory looks like.
; This was made on a 1920 x 1080 screen size. (In Windows)
; Have a lobster pot in your 2nd bank inventory space, turn on "Always set placeholders"
;OPTIONAL:
; Have your chat turned to "Game" Chat
#SingleInstance

CoordMode, Pixel, Screen    ; Starts pixel search at top left of ACTUAL SCREEN, delete if you want to search from top left of WINDOW
CoordMode, Mouse, Screen

SetMouseDelay, 80

global bag_x1 = 1385
global bag_y1 = 700
global last_bagslot_menu_x1 = 1565
global last_bagslot_x1 = 1805
global last_bagslot_y1 = 965
global bag_x2 = 1855
global bag_y2 = 1000

global top_of_bag_x1 = 1400
global top_of_bag_y1 = 700
global top_of_bag_x2 = 1880
global top_of_bag_y2 = 740

global top_left_x1 = 0
global top_left_y1 = 22
global top_left_x2 = 190
global top_left_y2 = 75

global bank_inventory_x1 = 450
global bank_inventory_y1 = 50
global bank_inventory_x2 = 1060
global bank_inventory_y2 = 850

global middle_x1 = 0
global middle_y1 = 200
global middle_x2 = 1650
global middle_y2 = 970

global chat_x1 = 0
global chat_y1 = 875
global chat_x2 = 515
global chat_y2 = 1015

global screen_size_x = 1920
global screen_size_y = 1080

global red_tile := 0xFF0000
global green_tile := 0x08C300
global blue_tile := 0x0013FF
global message_color := 0x0000FF

global raw_lobster := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\raw_lobster.bmp"
global bank_deposit_all_items := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\bank_deposit_all_items.bmp"
global exit_bank_button := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\exit_bank_button.bmp"
global open_bag := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\open_bag.bmp"
global cooking_message := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\cooking_message.bmp"
global bonfire_text := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\bonfire_text.bmp"
global cooking := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\cooking.bmp"
global bank_chest := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\bank_chest.bmp"


^+`::
{
    IfWinActive, RuneLite - BinaryBilly
    {
        loop_count = 11
        
    Start:
        Random, divisor, 6, 14
        if (loop_count > divisor)
        {
            remainder := Mod(loop_count, divisor)
            if(remainder = 0)
            {
                TrayTip,, 10-30second pause now
                sleep_random(10000, 30000)
            }
        }
        ;0. Check if skip to cooking.
        if (is_cooking())
        {
            Goto, Cooking
        }
        ;if we aren't done with cooking and we aren't cooking, CookLobster
        if (cooking_is_done() = false)
        {
            Goto, CookLobster
        }

        if (!loop_count = 0)
        {
            TrayTip,, %loop_count% times left to run.
            loop_count--
        }
        else
        {
            MsgBox, Done running!
            return
        }
            
    Bank:        
        ;1. Open Bank
        pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2, red_tile, "mouseover")
        ;if we can't verify and click on the bank, try again
        if(!verify_and_click_bank())
        {
            sleep_random(300, 1200)
            Goto, Bank
        }
        while (bank_is_open() = false)
        {

            sleep_random(300, 500)
        }
        
        ;2. Deposit all
        image_search_and_click(bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, bank_deposit_all_items, 0)

        ;3. Withdraw all raw lobbies
        if (bank_is_out_of_raw_lobsters())
        {
            MsgBox, Error: Couldn't find lobsters!
            return
        }
        image_search_and_click(bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, raw_lobster, "right")
        click_withdraw_all()
        sleep_random(700, 1200)
        ;mouse_move_random_offset()
        
        ;close bank
        image_search_and_click(bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, exit_bank_button, 0)
        sleep_random(700,1200)
        
    CookLobster:
        ;4. Click raw lobbies
        if(image_search_and_click(bag_x1, bag_y1, bag_x2, bag_y2, raw_lobster, 0) = false)
        {
            Goto, Start
        }
        sleep_random(300, 600)

    ClickBonfire:
        ;5. Mouse over bonfire
        pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2,  blue_tile, "mouseover")
        sleep_random(450 ,500)

        if (verify_and_click_bonfire())
        {
            sleep_random(550, 950)
            
            ;6. Wait for cooking screen
            while (!cooking_screen_is_showing())
            {
                sleep_random(350, 550)   
            }
        }
        else
        {
            pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2,  green_tile, "doubleclick")
            Sleep_random(2000, 3400)
            Goto, CookLobster
        }

        sleep_random(500, 1000)
        
        ;7. Press spacebar to start cooking
        Send, {space}
        sleep_random(500,1000)
        pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2,  red_tile, "mouseover")
        
        
        ;8. wait while cooking is not done
        while (!is_cooking())
        {
            sleep_random(1000, 2000)
        }
        
    Cooking:
        while (is_cooking())
        {
            sleep_random(3000, 7000)
        }
        if (cooking_is_done())
        {
            ;TrayTip,, cooking is done - starting over
            Goto, Start
        }
        else
        {
            Goto, CookLobster
        }
    }
    return
}


Numpad1::
    if(is_cooking())
    {
        TrayTip,, we cookin
    }
    else
    {
        TrayTip,, we not cookin
    }
;------------------------------------------FUNCTIONS--------------------------------------------------------
;check to see if bag is open
open_bag()
{
    IfWinActive, RuneLite - BinaryBilly
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

;check to see if the chat box shows the food item of choice
cooking_screen_is_showing()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, chat_x1, chat_y1, chat_x2, chat_y2, %cooking_message%
        if (ErrorLevel = 2)
        {
            ;MsgBox Error: In cooking_screen_is_showing() -- Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            ; cooking message was not found
            return false
        }
        else
        {
            ; cooking message found
            return true
        }
    }
    return false
}


;If this isn't working, try to increase the *n in ImageSearch to a higher value (up to 255)
is_cooking()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, top_left_x1, top_left_y1, top_left_x2, top_left_y2, *50 %cooking%
        if (ErrorLevel = 2)
        {
            MsgBox, is_cooking() - Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            ;TrayTip,, is_cooking() - Icon could not be found on the screen.
            return false
        }   
        else
        {
            return true
        }
    }
    return false
}

verify_and_click_bank()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, top_left_x1, top_left_y1, top_left_x2, top_left_y2, *50 %bank_chest%
        if (ErrorLevel = 2)
        {
            TrayTip,, verify_and_click_bank() - Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            ;TrayTip,, verify_and_click_bank() - Icon could not be found on the screen.
            return false
        }   
        else
        {
            Click, found_x, found_y
            return true
        }
    }
    return false
}

bank_is_open()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, %bank_deposit_all_items%
        if (ErrorLevel = 2)
        {
            MsgBox, is_cooking() - Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            ;TrayTip,, is_cooking() - Icon could not be found on the screen.
            return false
        }   
        else
        {
            return true
        }
    }
    return false
}
;Checks to see if there are any raw lobsters in bag, if so return false
cooking_is_done()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        if(open_bag() = false)
        {
            ;open the bag
            SendInput, {F3}
        }
        sleep_random(200, 600)
        ImageSearch, found_x, found_y, bag_x1, bag_y1, bag_x2, bag_y2, %raw_lobster%
        if (ErrorLevel = 2)
            MsgBox Error: In cooking_is_done() -- Could not conduct the search.
        else if (ErrorLevel = 1)
        {
            ; raw lobster could not be found on the screen: cooking is done
            return true
        }
        else
        {
            ; otherwise raw lobster was found, meaning cooking is not done
            return false
        }
    }
    return false
}


verify_and_click_bonfire()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ;TrayTip,, %top_left_x1%x%top_left_y1% | %top_left_x2%x%top_left_y2% | %bonfire_text%
        ImageSearch, found_x, found_y, top_left_x1, top_left_y1, top_left_x2, top_left_y2, *100 %bonfire_text%
        if (ErrorLevel = 2)
        {
            TrayTip,, verify_and_click_bonfire() - Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            ;TrayTip,, verify_and_click_bonfire() - Icon could not be found on the screen.
            return false
        }   
        else
        {
            Click, found_x, found_y
            return true
        }
    }
}


bank_is_out_of_raw_lobsters()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, %raw_lobster%
        if (ErrorLevel = 2)
            MsgBox Error: In cooking_is_done() -- Could not conduct the search.

        else if (ErrorLevel = 1)
        {
            ;raw lobster was NOT found in bank, meaning bank is out of lobsters to cook
            return true
        }
        else
        {
            ;otherwise raw lobster in bank, meaning bank is not out of lobsters to cook
            return false
        }
    }
}


;Checks to see if level up message happened
level_up_message_exists()
{   
    IfWinActive, RuneLite - BinaryBilly
    {
        PixelSearch, found_x, found_y, chat_x1, chat_y1, chat_x2, chat_y2, %message_color%, 0, RGB Fast
        if ErrorLevel
           ;if the message was not found
            return false
        
        ;if the message was found
        return true
    }
}


;Search for an image and click on it. If modifier = "right", right click,
;    "mouseover" will move the mouse but doesn't click, otherwise left click.
image_search_and_click(x1, y1, x2, y2, image_url, modifier)
{
    Random, offset_horizontal, -10, 10
    Random, offset_vertical, -10, 10
    abort_counter = 3
Retry:
    IfWinActive, RuneLite - BinaryBilly
    {
        ; delays should be randomized often
        set_random_delays()
        
        ; search for the image
        ImageSearch, found_x, found_y, x1, y1, x2, y2, %image_url%
        if (ErrorLevel = 2)
        {
            TrayTip,, Could not conduct the search using: %x1%- %y1%- %x2%- %y2%- %image_url%
            return
        }

        else if (ErrorLevel = 1)
        {
            mouse_move_random_offset()
            sleep_random(1000, 1200)
            abort_counter--
            if (abort_counter > 0)
            {
                Goto, Retry
            } 
            else
            {
                TrayTip,, Retried 3 times- bot failed to find image. `rIt must be off screen or blocked.
                return
            }
        }
        else
        {
            offset_x := found_x + offset_horizontal
            offset_y := found_y + offset_vertical
            if (modifier = "right")
                Click, right, %offset_x%, %offset_y%
            else if (modifier = "mouseover")
                MouseMove, %offset_x%, %offset_y%
            else if (modifier = "doubleclick")
            {
                Click, %offset_x%, %offset_y%
                Click, %offset_x%, %offset_y% 
            }
            else
                Click, %offset_x%, %offset_y%
            return
        }
    }
    return
}

;Set the color of a tile in game and use that as the pixel color. if modifier = "right", right click,
;    "mouseover" will move the mouse but doesn't click, "doubleclick" clicks twice in the same spot.
;     Otherwise left click.
pixel_search_and_click_world_tile(x1, y1, x2, y2, pixel_color, modifier)
{
    IfWinActive, RuneLite - BinaryBilly
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
            Random, offset_tile_x, -15, -5
            Random, offset_tile_y, 5, 15
            offset_x := found_x + offset_tile_x
            offset_y := found_y + offset_tile_y
            
            if (modifier = "right")
                Click, right, %offset_x%, %offset_y%
            else if (modifier = "mouseover")
                MouseMove, %offset_x%, %offset_y%
            else if (modifier = "doubleclick")
            {
                Click, %offset_x%, %offset_y%
                Click, %offset_x%, %offset_y%
            }
            else
                Click, %offset_x%, %offset_y%
        }
    }
}

;Move mouse down to withdraw all option.
click_withdraw_all()
{
    Random, offset_horizontal, -40, 40
    Random, offset_vertical, 95, 105
    Click, %offset_horizontal%, %offset_vertical%, Rel
}



; ---------------------- Utilities --------------------------------------------
set_random_delays()
{   
    Random, delaySpeed, 60, 110
    SetMouseDelay, %delaySpeed%
    
    Random, key_delay_speed, 100, 300
    Random, press_duration, 100, 300
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

+`::Reload

^`::ExitApp