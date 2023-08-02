;REQUIRED:
; Runelite client, change your name in the window names in the code below.
; This was made on a 1920 x 1080 screen size. (In Windows)
; You must set the bot up each time:
;   - your inventory depletes of lobsters.
;   - the target disappears through a wall
; You must have 'Status Bars' in RuneLite on so that your health bar is shown on the left of your "bag".
; You must have 'NPC Indicators' highlight color the same as in the script (0xA4FF00).
;OPTIONAL:
; Have your chat turned to "Game" Chat, this would help because we search for phrases in the chat box.

#SingleInstance
#Include ..\utilities.ahk

SetWorkingDir A_MyDocuments "\AutoHotkey_Scripts\runescape"

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")

; these are image files used for image searching
global images := {
    attack_menaphite_hovering_text : A_WorkingDir "\image_library\attack_menaphite_hovering_text.png",
    lobster_cooked : A_WorkingDir "\image_library\lobster_cooked.png",
    attack : A_WorkingDir "\image_library\attack_top_left.bmp",
    failed_pickpocket : A_WorkingDir "\image_library\failed_pickpocket.bmp",
    glancing_blow : A_WorkingDir "\image_library\glancing_blow.bmp",
    knockout_option : A_WorkingDir "\image_library\knockout_option.bmp",
    pickpocket_option : A_WorkingDir "\image_library\pickpocket_option.bmp",
    ; not used right_click_options : A_WorkingDir "\image_library\right_click_options.png",
    unconscious : A_WorkingDir "\image_library\unconscious.png",
    cannot_knockout : A_WorkingDir "\image_library\cannot_do_that.bmp",
    healthbar : A_WorkingDir "\image_library\healthbar.bmp",
    stunned : A_WorkingDir "\image_library\stunned.bmp",
    imstunned : A_WorkingDir "\image_library\imstunned.png",
    missed_right_click : A_WorkingDir "\image_library\missed_right_click.bmp",
    combat : A_WorkingDir "\image_library\combat.bmp",
    money_bag : A_WorkingDir "\image_library\money_bag.png",
    open_bag : A_WorkingDir "\image_library\open_bag.bmp"
}

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"

; some tooltip coords
global tooltip_x := 600
global tooltip_y := 550

; object that holds all of the screen area coordinates
global coord := {
    chat:       { x1: 7, y1: 965, x2: 515, y2: 1015 },
    bag:        { x1:1385, y1:700, x2:1855, y2:1000 },
    top_left:   { x1:0, y1:22, x2:190, y2:75 },
    middle:     { x1:0, y1:200, x2:1650, y2:970 }
}

; coords to ensure an NPC's orientation
; add more vertices to these :o
global target_coord := {
    laying_left:    { x:745, y:330 },
    laying_middle:  { x:890, y:225 },
    laying_right:   { x:1030, y:380 },
    laying_bottom:  { x:805, y:600 },
    laying_left_2:    { x:824, y:330 },
    laying_middle_2:  { x:965, y:225 },
    laying_right_2:   { x:1105, y:375 },
    laying_bottom_2:  { x:890, y:600 },
    standing_top_left:      { x:805, y:240 },
    standing_top_right:     { x:975, y:245 },
    standing_bottom_left:   { x:805, y:600 },
    standing_bottom_right:  { x:940, y:535 },
    standing_top_left_2:        { x:885, y:245 },
    standing_top_right_2:       { x:1055, y:245 },
    standing_bottom_left_2:     { x:890, y:600 },
    standing_bottom_right_2:    { x:1030, y:530 }
}

; these are the colors of outlines around enemy NPCs
global enemy_color := 0xA4FF00
global enemy_color_dark := 0x84CD00
global tick_color := 0x00DFDF
global tick_color2 := 0x1580AD
global tick_color3 := 0x01E0E1

F1::Main()

+F1::Reload()

^F2::ExitApp()


Main()
{
    ;if ImageExists(images.money_bag)
    ;     ClickMoneyBag()

    tick_time := 600

    short_sleep_min := 300
    short_sleep_max := 450
    successful_runs := 0
    ;setup_in()

    state := "check_health"
    WaitForTick()
    
    SetTimer Tick, 600
    return

    Tick()
    {
        if state == "check_health" 
        {
            ; check health
            if HealthIsOkay()
                state := "right_click"
             else 
                state := "eat_lobster"
        } 
        else if state == "eat_lobster" 
        {
            ; eat lobster
            if EatLobster() 
                state := "check_health"
            else
                state := "pause"
        } 
        else if state == "pause" 
        {
            MsgBox ("Refill lobsters...`rYou filthy mongrel..!`r (Then press OK)")
            
        } else if state == "knockout" {
            RightClickNPC()
            sleep_random(short_sleep_min, short_sleep_max)
            ClickKnockout()
            state := "wait_tick"

        } else if state == "wait_tick" {
            RightClickNPC()
            state := "pickpocket"

        } else if state == "pickpocket" {
            ClickPickpocket()
            state := "wait_tick2"

        } else if state == "wait_tick2" {
            state := "wait_tick3"

        } else if state == "wait_tick3" {
            state := "pickpocket_dos"

        } else if state == "pickpocket_dos" {
            RightClickNPC()
            sleep_random(short_sleep_min, short_sleep_max)
            ClickPickpocket()
            state := "check_health"

        return
        }
    }
}

IAmStunned()
{
    if ImageExists(images.imstunned)
        return true
    return false
}

WaitForTick()
{
    if WaitForPixel(1697, 117, 1701, 123, tick_color)
        return true
    return false
}

; the right click menu in the game is open, now we left click the knockout option
ClickKnockout()
{
    MouseGetPos(&x, &y)
    search_x1 := x - 130
    search_y1 := y
    search_x2 := x + 120
    search_y2 := y + 255

    if image_search_and_click(images.knockout_option, 0, "left", "option", search_x1, search_y1, search_x2, search_y2)
       return true
    return false
}

; the right click menu in the game is open, and we either just knocked them out, or it was a glancing blow and they are
;   about to attack. To counteract their attack, we can click pickpocket on them.
ClickPickpocket()
{
    MouseGetPos(&x, &y)
    search_x1 := x - 130
    search_y1 := y
    search_x2 := x + 120
    search_y2 := y + 255

    if image_search_and_click(images.pickpocket_option, 0, "left", "option", search_x1, search_y1, search_x2, search_y2)
       return true
    return false
}

; searches in a square area around the player and expands the search area until an image is found or we are off screen.
RightClickNPC_old()
{
    ; clicks need to be fast (but not instant), we'll add sleeps when necessary
    SetDefaultMouseSpeed(1)

    if WinActive(runelite_window)
    {
        ; First check if the right click option is already active
        if (ImageExists(images.knockout_option) || ImageExists(images.pickpocket_option))
            return true
        
        target_click_area := GetTargetClickArea()
        offset_x := Random(-50, 50)
        offset_y := Random(-50, 50)
        target_x := target_click_area.x + offset_x
        target_y := target_click_area.y + offset_y
        
        Click(target_x, target_y, "Right")
        ;ToolTip, in while %count%: `r%x1%x%y1%'r%x2%x%y2% `rPixel:%enemy_color%, %tooltip_x%, %tooltip_y%, 2
        return true
    }
    return false
}

; right clicks around the chest area of the NPC
RightClickNPC()
{
    ; clicks need to be fast (but not instant), we'll add sleeps when necessary
    SetDefaultMouseSpeed(1)

    ; Get the target click area
    click_area := GetTargetClickArea()
    offset_x := Random(-40, 40)
    offset_y := Random(-30, 30)

    ; Randomize within the area and right click
    ToolTip("Right Clicking:`roffset x:" offset_x ", y:" offset_y "`rx:" click_area.x ", y:" click_area.y, 100, 1000, 6)
    x := click_area.x + offset_x
    y := click_area.y + offset_y
    MouseMove(x, y)
    sleep_random(10,20)
    ; If target is in sight
    if ImageExists(images.attack_menaphite_hovering_text) {
        Click("Right")
        return true
    }
    return false
}

; click the money bag in your inventory
 ClickMoneyBag()
{
    ;ensure bag is open
    if ImageExists(images.open_bag) {
        sleep_random(10, 100)
        if image_search_and_click(images.open_bag, "whole_screen", "left", "item2")
            return true
    }
    return false
}

; click the first availableb lobster in your inventory
EatLobster()
{        
    open_bag()
    sleep_random(100, 1000)
    ; ToolTip("Searching coord.bag: " coord.bag.x1 coord.bag.y1 coord.bag.x2 coord.bag.y2 "`r" images.lobster_cooked, 900, 900, 2)
    if image_search_and_click(images.lobster_cooked, "whole_screen", "left", "item2")
       return true
    return false
}

HealthIsOkay()
{
    if ImageExists(images.healthbar, 1400, 820, 1700, 850)
        return true
    return false
}

WasGlancingBlow()
{
    if (exists("chat", images.glancing_blow))
        return true
    return false
}

IsUnconscious()
{
    if ImageExists(images.unconscious, 231, 970, 390, 990)
        return true
    return false
}