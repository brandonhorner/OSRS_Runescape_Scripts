;THIS SCRIPT DOES NOT CURRENTLY WORK
;REQUIRED:
; Runelite client
; Change your name in the window names in the code below.
; This was made on a 1920 x 1080 screen size (In Windows) so use the same resolution for now.
; You should have your inventory set up the same as 3_tick_setup.bmp provided if using 3 tick. 
; You should have fishing icons on. (Fishing in Runelite)

#SingleInstance

CoordMode, Pixel, Screen    ; Starts pixel search at top left of ACTUAL SCREEN, delete if you want to search from top left of WINDOW
CoordMode, Mouse, Screen

global bag_x1 = 1385
global bag_y1 = 700
global bag_x2 = 1855
global bag_y2 = 1000

global last_bagslot_menu_x1 := 1565
global last_bagslot_x1 := 1805
global last_bagslot_y1 := 965

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

global pink_tile := 0xFF00FF

global fishing_spot := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\fishing_spot.bmp"
global fishing_text := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\fishing_text.bmp"
global fishing := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\fishing.bmp"
global herb := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\herb.bmp"
global swamp_tar := "C:\Users\Tuco\Documents\AutoHotkey_Scripts\Runescape\barbarian_fishing\swamp_tar.bmp"


^F1:: ;three tick fishing
IfWinActive, RuneLite - BinaryBilly
{
    click_fishing_spot()
    sleep_random(600, 650)
;TODO: If fishing spot not near me, don't start clicking herb!!
    click_herb()
    click_swamp_tar()
    shift_click_fish()
    Goto, Start
    return
} 
return


click_fishing_spot()
{
    Fish:
    IfWinActive, RuneLite - BinaryBilly
    {
        image_search_and_click("middle", fishing_spot, "left", "item")        
        return false
    }
}

click_herb()
{
    if (exists("bag", herb))
    {
        image_search_and_click("bag", herb, "left", "item")
        return true
    }
    return false
}

click_swamp_tar()
{
    if (exists("bag", swamp_tar))
    {
        image_search_and_click("bag", swamp_tar, "left", "item")
        return true
    }
    return false
}

;Drop the fish to the left of the swamp tar. Assumes correct inventory layout.
shift_click_fish()
{
    Random, x, -50, -40
    Random, y, -10, 10
    Send, {shift down}
    Click, %x%, %y%, Rel
    Send, {shift up}
}