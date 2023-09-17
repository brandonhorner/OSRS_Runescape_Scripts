;REQUIRED:
; Runelite client, change your name in the window names in the code below.
; This was made on a 1920 x 1080 screen size. (In Windows)
; You must set the bot up each time:
;   - your inventory depletes of lobsters.
;   - the target disappears through a wall
; You must have 'Status Bars' in RuneLite on so that your health bar is shown on the left of your "bag".
; You must have 'NPC Indicators' highlight color the same as in the script (0xA4FF00).
;OPTIONAL:
; Have your chat turned to "Game" Chat, this is required because we search for phrases in the chat box.
; (You can still split your friend chat)

#SingleInstance Force
#Include ..\utilities.ahk

SetWorkingDir A_MyDocuments "\AutoHotkey_Scripts\runescape"

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")


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
    open_bag : A_WorkingDir "\image_library\open_bag.bmp",
    open_curtain_option : A_WorkingDir "\image_library\blackjacking\open_curtain.png",
    close_curtain_option : A_WorkingDir "\image_library\blackjacking\close_curtain.png",
    select_an_option : A_WorkingDir "\image_library\blackjacking\select_an_option.png",
    stunned : A_WorkingDir "\image_library\been_stunned.bmp"
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
    ;       p1       ;       p2       ;       p3      ;
    ;       p1       ;       p2       ;       p3      ;
    ;_______p1_______;_______p2_______;_______p3______;
    ;       p4       ;       p5       ;       p6      ;
    ;       p4       ;       p5       ;       p6      ;
    ;       p4       ;       p5       ;       p6      ;
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
    npc : 0xA4FF00,
    npc_dark : 0x84CD00,
    tick : 0x00DFDF,
    tick_2 : 0x1580AD,
    tick_3 : 0x01E0E1
}


F1::
{
    if WinActive(runelite_window)
        Main()
}

+F1::Reload()

^F2::ExitApp()

Main()
{
    setup_in()
    
    clickAttempts := 0
    fullMoneyBagOpens := 0

    while(true)
    {
        ; set the click location. each time we are full on money bags this will reset
        x := Random(1085, 1165)
        y := Random(480, 525)
        
        ; while we don't have full money bags, let's
        while (!CheckIfFullOnMoneyBags())
        {
            ; make sure menu is closed
            if(menu_is_open()) {
                MsgBox "Close the menu in Runelite to continue."
                continue
        }
        
        ;1. Preliminaries ----------------------
        if CheckIfStunned()
            continue                                                        ; check if we are stunned, wait it out if we are
        
        if HealthIsLow() {                                                   ; check if health is low

            ClickMoneyBag()

            if !EatLobster() {                                             ; try to eat a lobster if it is

                ReloadFood()                                                 ; pause for player to reload inventory if you're out of lobbies
            }
        }
        ; -------------------------------------

        WaitForTick()
        sleep_random(300,500)
        ; Wait for the next tick, then left click the ardy night.. then wait some more.
        if EnemyToRight()
        {
            LeftClickArdyKnight(x, y)
        }
        else
        {
            PixelSearchAndClick(pixel_color.tile_purple, "p2", "left", "tile_se")
            sleep_random(5000, 7000)
        }
        clickAttempts++
        sleep_random(200,300)
        WaitForTick()

        totalMoneyBags := fullMoneyBagOpens * 28
        ToolTip "Counter:`nSingle pickpocket (clicks attempted, not pickpockets): " clickAttempts "`nComplete 28 stacks of money bags: " fullMoneyBagOpens "`nThat makes " totalMoneyBags " total money bags", X_TOOLTIP.9, Y_TOOLTIP.9, 9
        ; wait for the final message for double pickpocket (or 2 ticks)   
        }

        fullMoneyBagOpens++
    }
}

EnemyToRight()
{   ;1115, 410, 1230, 575
    if (PixelSearchAndClick(pixel_color.npc,,,,1115, 410, 1230, 575, 30))
    {
        return true
    }
    return false
}

setup_in()
{
    if WinActive(runelite_window)
    {
        ;zoom all the way out
        zoom("in")
        sleep_random(100, 200)
        Send("{W down}")
        ;Face North (click compass)
        click_compass()
        sleep_random(1000, 1000)
        Send("{W up}")

    }
}

ReloadFood()
{
    MsgBox("Go get food then come back and press OK")
}

/*Assumes you will be replacing your left click option with pickpocket*/
LeftClickArdyKnight(x, y)
{
    Click x, y, "Left"
}