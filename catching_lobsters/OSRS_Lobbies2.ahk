;REQUIRED:
; Runelite client, change your name in the window names in the code below.
; Starts at bank in catherby or on the beach by lobsters, doesn't matter what
; your inventory looks like.
; This was made on a 1920 x 1080 screen size. (In Windows).
; Have a lobster pot in the first screen of your bank (turn on "Always set placeholders")
 
#SingleInstance

CoordMode, Pixel, Screen    ; Starts pixel search at top left of ACTUAL SCREEN, delete if you want to search from top left of WINDOW
CoordMode, Mouse, Screen

SetMouseDelay, 80
;TODO: Change all integer variables to = and take away %%
global bag_x1 := 1385
global bag_y1 := 700
global last_bagslot_menu_x1 := 1565
global last_bagslot_x1 := 1805
global last_bagslot_y1 := 965
global bag_x2 := 1855
global bag_y2 := 1000

global below_character_menu_x1 := 808
global below_character_no_menu_x1 := 931
global below_character_y1 := 550
global below_character_menu_x2 := 839
global below_character_no_menu_x2 := 960
global below_character_y2 := 583

global runelite_menu_x := 1880 
global runelite_menu_y := 355   

global top_of_bag_x1 := 1400
global top_of_bag_y1 := 700
global top_of_bag_x2 := 1880
global top_of_bag_y2 := 740

global bank_inventory_x1 := 450
global bank_inventory_y1 := 50
global bank_inventory_x2 := 1060
global bank_inventory_y2 := 850

global top_left_x1 := 0
global top_left_y1 := 24
global top_left_x2 := 190
global top_left_y2 := 75

global middle_x1 := 0
global middle_y1 := 200
global middle_area_no_bag_x2 := 1400
global middle_area_no_bag_y2 := 850
global middle_x2 := 1650
global middle_y2 := 970

global chat_x1 := 0
global chat_y1 := 875
global chat_x2 := 515
global chat_y2 := 1015

global black_tile := 0x000000
global blue_tile := 0x000FFF
global green_tile := 0x00FF00
global pink_tile := 0xFF00FF
global runelite_menu_color := 0x282828
global red_tile := 0xFF0000
global teal_tile := 0x377372
global yellow_tile := 0xFFFF00

global bag_is_open := "images\bag_is_open.bmp"
global bank := "images\bank.bmp"
global bank_deposit_all_items := "images\bank_deposit_all_items.bmp"
global fishing := "images\fishing.bmp"
global fishing_text := "images\fishing_text.bmp"
global lobster_pot := "images\lobster_pot.bmp"
global raw_lobster := "images\raw_lobster.bmp"


^+`::
{
    IfWinActive, RuneLite - BinaryBilly
    {
    ;TODO
    ; Check where you with search_screen_portion
    Goto, CheckFishing
    Bank:
        loop_count := 50
        if (loop_count <= 0)
        {
            return
        }
        loop_count--
        ;Clicking the bank stall (teal tile AND bank.bmp is showing)
        pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2, teal_tile, "mouseover")
        verify_and_click_bank()
        sleep_random(9000, 12000)
        
        ;Deposit all items
        image_search_and_click(bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, bank_deposit_all_items, 0)
        sleep_random(700, 1200)
        
        ;Take out lobster pot
        image_search_and_click(bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, lobster_pot, 0)

    LeaveBank:
        ;Leave the bank, clicking pink tile
        pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2, pink_tile, 0)
        sleep_random(9000, 12000)
    
    CheckFishing:
        count := 0
        while (is_fishing())
        {
            ;TrayTip,, we be fishing
            sleep_random(3000, 7000)
            count++
            value := Mod(count, 15)
            if( value = 0 )
            {
                click_lobsters_in_front()
                ;TrayTip,, 10th iteration of watchspawn(), 1
            }
        }
        ;if not fishing, check last bag slot
        if (bag_is_full())
        {
            TrayTip,, bag was full! returning to pink area
            ;walk back to bank
            pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2, pink_tile, 0)
            sleep_random(8000, 9000)
            Goto, Bank
        }
        ;back to scan for lobsters to catch

        
        
    SearchSpots:
        if (!click_lobsters_in_front()) ; if we can't click lobsters in front of us, scan
        {
            ;TrayTip,, couldn't find lobsters in front
            ;sleep_random(1000,2000)
            if (!scan_for_lobsters()) ;if we can't find lobsters in scan, reposition
            {
                ;TrayTip,, couldn't find lobsters in scan - moving to green
                pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2, green_tile, 0)
                sleep_random(4500,5500)
                Goto SearchSpots
            }
        }
        sleep_random(4000, 5500)
        

        Goto, CheckFishing
    }
return
}

Numpad1::
        pixel_search_and_click_world_tile(middle_x1, middle_y1, middle_x2, middle_y2, pink_tile, 0)


is_fishing()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, %top_left_x1%, %top_left_y1%, %top_left_x2%, %top_left_y2%, *50 %fishing%
        if (ErrorLevel = 2)
        {
            TrayTip,, is_fishing() - Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            ;TrayTip,, is_fishing() - Icon could not be found on the screen.
            return false
        }   
        else
        {
            return true
        }
    }
    return false
}

;check to see if bag is open
bag_is_open()
{
    IfWinActive, Runelite - BinaryBilly
    {
        ImageSearch, found_x, found_y,  %top_of_bag_x1%, %top_of_bag_y1%, %top_of_bag_x2%, %top_of_bag_y2%, %bag_is_open%
        if (ErrorLevel = 2)
            MsgBox Error: In bag_is_open() -- Could not conduct the search.
        else if (ErrorLevel = 1)
        {
            ; open bag was not found
            return false
        }
        else
        {
            ; open bag found
            return true
        }
    }
    return false
}

verify_and_click_bank()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, %top_left_x1%, %top_left_y1%, %top_left_x2%, %top_left_y2%, *50 %bank%
        if (ErrorLevel = 2)
        {
            TrayTip,, verify_and_click_bank() - Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            TrayTip,, verify_and_click_bank() - Icon could not be found on the screen.
            return false
        }   
        else
        {
            Click, found_x, found_y
            return true
        }
    }
}

verify_and_click_lobsters()
{
    IfWinActive, RuneLite - BinaryBilly
    {
        ImageSearch, found_x, found_y, %top_left_x1%, %top_left_y1%, %top_left_x2%, %top_left_y2%, *50 %fishing_text%
        if (ErrorLevel = 2)
        {
            TrayTip,, verify_and_click_lobsters() - Could not conduct the search.
            return false
        }
        else if (ErrorLevel = 1)
        {
            ;TrayTip,, verify_and_click_lobsters() - Icon could not be found on the screen.
            return false
        }   
        if (found_x)
        {
            Click, found_x, found_y
            return true
        }
    }
}

bag_is_full()
{
    if (bag_is_open() = false)
    {
        ;open the bag
        SendInput, {F3}
    }
    sleep_random(200, 600)
    if (menu_is_open())  ;runelite menu is open
        x1 := last_bagslot_menu_x1
    else
        x1 := last_bagslot_x1
    ;TrayTip,, %x1%x%last_bagslot_y1% | %bag_x2%x%bag_y2% | %raw_lobster%
    ImageSearch, found_x, found_y, %x1%, %last_bagslot_y1%, %bag_x2%, %bag_y2%, %raw_lobster%
    if (ErrorLevel = 2)
    {
        MsgBox, ;_full(): Could not conduct the search.
        Reload
    }
    else if (ErrorLevel = 1)
    {
        ;TrayTip,, bag_is_full() - Icon could not be found on the screen.
        return false
    }
    ;if we found a raw lobster, bag is full
    else
    {
        return true
    }
}

click_lobsters_in_front()
{
    abort_counter = 3
RetrySearch:
    if (menu_is_open())  ;runelite window is open
    {
        x1 := below_character_menu_x1
        x2 := below_character_menu_x2
    }
    else
    {
        x1 := below_character_no_menu_x1
        x2 := below_character_no_menu_x2
    }
    if (image_search_and_click(x1, below_character_y1, x2, below_character_y2, raw_lobster, "mouseover"))
    {
        if( verify_and_click_lobsters())
            return true
        else
        {
            if( abort_counter > 0 )
            {
                abort_counter--
                Goto, RetrySearch
            }
            return false
        }
    }
    return false
}

scan_for_lobsters()
{
    if(image_search_and_click(middle_x1, middle_y1, middle_area_no_bag_x2, middle_area_no_bag_x2, raw_lobster, "mouseover"))
    {
        if( verify_and_click_lobsters())
            return true
        return false
    }
    return false
}

menu_is_open()
{
    IfWinActive, RuneLite - BinaryBilly
    {
    
        PixelGetColor, color, %runelite_menu_x%, %runelite_menu_y%
        if (color = runelite_menu_color)  ;runelite window is open
        {
            ;TrayTip,, returning true
            return true
        }
        else
        {
            ;TrayTip,, returning false
            return false
        }
    }
}

; modifier should be pixel or image
search_screen_portion(position_on_screen, image_url_or_pixel, modifier)
{
;TODO fill
    ;if (position_on_screen = "middle")
    ;{
      
    ;}
    ;else if (position_on_screen = "bag" )
    ;{
        
    ;}
    Random, offset_horizontal, -10, 10
    Random, offset_vertical, -10, 10
    abort_counter = 3

    IfWinActive, RuneLite - BinaryBilly
    {
        ; how fast the mouse moves should be randomized
        Random, delaySpeed, 60, 110
        SetMouseDelay, %delaySpeed%
        
        ;if(
        ; search for the image
        ImageSearch, found_x, found_y, %x1%, %y1%, %x2%, %y2%, %image_url%
        if (ErrorLevel = 2)
        {
            TrayTip,, Could not conduct the search using: %x1%- %y1%- %x2%- %y2%- %image_url%
            return false
        }

        else if (ErrorLevel = 1)
        {
            ;mouse_move_random_offset()
            sleep_random(100, 200)
            abort_counter--
            if (abort_counter > 0)
            {
;Goto, Retry
            } 
            else
            {
                ;TrayTip,, Retried 3 times- bot failed to find image. `rIt must be off screen or blocked.
                ;TrayTip,, %x1%x%y1% | %x2%x%y2% | %image_url%
                return false
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
            else
                Click, %offset_x%, %offset_y%
            return true
        }
    }
    return false
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
        ; how fast the mouse moves should be randomized
        Random, delaySpeed, 60, 110
        SetMouseDelay, %delaySpeed%

        ; search for the image
        ImageSearch, found_x, found_y, %x1%, %y1%, %x2%, %y2%, %image_url%
        if (ErrorLevel = 2)
        {
            TrayTip,, Could not conduct the search using: %x1%- %y1%- %x2%- %y2%- %image_url%
            return false
        }

        else if (ErrorLevel = 1)
        {
            ;mouse_move_random_offset()
            sleep_random(100, 200)
            abort_counter--
            if (abort_counter > 0)
            {
                Goto, Retry
            } 
            else
            {
                ;TrayTip,, Retried 3 times- bot failed to find image. `rIt must be off screen or blocked.
                ;TrayTip,, %x1%x%y1% | %x2%x%y2% | %image_url%
                return false
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
            else
                Click, %offset_x%, %offset_y%
            return true
        }
    }
    return false
}

;Set the color of a tile in game and use that as the pixel color. if modifier = "right", right click,
;    "mouseover" will move the mouse but doesn't click, otherwise left click.
pixel_search_and_click_world_tile(x1, y1, x2, y2, pixel_color, modifier)
{
    IfWinActive, RuneLite - BinaryBilly
    {
        
        Random, delaySpeed, 60, 110
        SetMouseDelay, %delaySpeed%

        PixelSearch, found_x, found_y, x1, y1, x2, y2, pixel_color, 0, RGB fast ;search region for color
        if ErrorLevel
        {
            ;TrayTip,, The color %pixel_color% was not found in %x1%x%y1% %x2%x%y2%.,1 
            return false
        }
        else
        {
            ;TrayTip,, The color %pixel_color% was found at x%found_x% and y%found_y% modifier= %modifier%
            
            ;these magic numbers are about the size of the tile to be clicked into, they might need to be adjusted
            ;         depending on how small the object inside of the tile is.
            Random, offset_tile_x, -15, -5
            Random, offset_tile_y, 5, 15
            offset_x := found_x + offset_tile_x
            offset_y := found_y + offset_tile_y
            
            if (modifier = "right")
                Click, right, %offset_x%, %offset_y%
            else if (modifier = "mouseover")
            {
                MouseMove, %offset_x%, %offset_y%
            }
            else
                Click, %offset_x%, %offset_y%
        }
    }
}


;Move the mouse randomly, offset from the current location
mouse_move_random_offset()
{
    Random, rand_x, -100, 100
    Random, rand_y, -90, 90
    MouseMove, rand_x, rand_y,, R
}

; ---------------------- Utilities --------------------------------------------

sleep_random( sleep_time_low, sleep_time_high )
{
    Random, sleep_time, sleep_time_low, sleep_time_high
    Sleep, %sleep_time%
    
    return
}

+`::Reload

^`::ExitApp