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

#SingleInstance
#Include ..\utilities.ahk
#Include testing.ahk
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
    
    dbl_pickpockets := 0
    sngl_pickpockets := 0

    while (true)
    {
        if(menu_is_open()) {
            MsgBox "Close the menu in Runelite to continue."
            continue
        }
        knockout_failure := false
        pickpocket_failure := false
        ;1. Preliminaries
        if CheckIfStunned()
            continue                                                        ; check if we are stunned, wait it out if we are
        
        CheckIfFullOnMoneyBags()
        
        if HealthIsLow() {                                                   ; check if health is low
            ClickMoneyBag()
            if (!EatLobster()) {                                             ; try to eat a lobster if it is
                ReloadLobsters()
                MsgBox "You ugly mug -- reload your lobsters!"              ; pause for player to reload inventory if you're out of lobbies
            }
        }

        if !TargetIsStandingUpFacingMe() and !TargetIsLayingDownFacingMe() {                                  ; ensure we are facing the NPC
                                                                            ToolTip "Target isn't facing me.. Restarting...", X_TOOLTIP.2, Y_TOOLTIP.2, 2
            sleep_random(100, 300)                                        ; if we aren't, then pause
            continue
        }
                                                                            ToolTip "Right click (1 of 3).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        ;2. Knockout
        RightClickNPC()                                                     ; start by right clicking the NPC if the menu isn't open
        WaitForTick()                                                       ; once the tick starts, we can start
        
        if CheckIfStunned()
            continue                                                        ; check if we are stunned, wait it out if we are
                                                                    ToolTip "Knockout    (1 of 1).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        if (!ClickKnockout()){                                              ; attempt to knockout, if it fails we'll continue back to the start 
            continue
        }
                                                                            ToolTip "Right click (2 of 3).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        RightClickNPC()                                                     ; prime another right click menu
        sleep_random(725, 725)
        CheckAndUpdateStatus(&knockout_failure, &pickpocket_failure)
                                                                    ToolTip "Pickpocket  (1 of 2).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        if !ClickPickpocket()                                       ; if it fails to click pickpocket
            continue                                                ; start the loop over
        
        sngl_pickpockets++
                                                                    ToolTip "Counters:`nSingle pickpockets: " sngl_pickpockets "`nDouble pickpockets: " dbl_pickpockets, X_TOOLTIP.9, Y_TOOLTIP.9, 9
        if CheckIfStunned()
            continue                                                        ; check if we are stunned, wait it out if we are
                                                                    ToolTip "Right click (3 of 3).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        RightClickNPC()                                             ; right click the NPC again
        CheckAndUpdateStatus(&knockout_failure, &pickpocket_failure)
        WaitForPickpocketAttempt()
        if (knockout_failure and pickpocket_failure) {              ; if the pickpocket failed,
                                                                    ToolTip "Epic failure, restarting in .5 to 1.5s", X_TOOLTIP.4, Y_TOOLTIP.4, 4
            sleep_random(500, 1500)
            MsgBox "We in combat..."
            Reload                                                 ; we are in combat :\ Reload.
        }
                                                                    ToolTip "Pickpocket  (2 of 2).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        sleep_random(550,550)
        if !ClickPickpocket()                                       ; try to pickpocket                      
            continue                                                ; start the loop over
        
        dbl_pickpockets++
                                                                    ToolTip "Counters:`nSingle pickpockets: " sngl_pickpockets "`nDouble pickpockets: " dbl_pickpockets, X_TOOLTIP.9, Y_TOOLTIP.9, 9
                                                                    ; wait for the final message for double pickpocket (or 2 ticks)   
    }
}

WaitForPickPocketAttempt()
{
    if WaitForImage(images.pickpocket_attempt, 100, coord.chat_bottom)
        return true

    return false
}

CheckAndUpdateStatus(&knockout_failure, &pickpocket_failure)
{
    if ImageExists(images.knockout_failure, coord.chat_bottom_2.x1, coord.chat_bottom_2.y1, coord.chat_bottom_2.x2, coord.chat_bottom_2.y2,)
        knockout_failure := true
    if ImageExists(images.pickpocket_failure, coord.chat_bottom_2.x1, coord.chat_bottom_2.y1, coord.chat_bottom_2.x2, coord.chat_bottom_2.y2,)
        pickpocket_failure := true
}

CheckIfStunned()
{
                                                                            ToolTip "Stunned. Waiting...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    if ImageSearchAndClick(images.imstunned, "top_left",,,,,,,5)
    {
        sleep_random(10, 10)
        return true
    }
                                                                            ToolTip "", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return false
}

HealthIsLow()
{
    if ImageExists(images.healthbar, 1400, 820, 1700, 850)
    {
        return false
    }
                                                                            ToolTip "Health is low...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return true
}

; click the first availableb lobster in your inventory
EatLobster()
{
                                                                            ToolTip "Eating lobster...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    open_bag()
    sleep_random(500, 1500)
    if ImageSearchAndClick(images.lobster_cooked, "bag", "mouseover", "item") {
        sleep_random(500, 1500)
        Click("Left")
        sleep_random(500, 1500)
        return true
    }
                                                                            ToolTip "...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return false
}

CheckIfFullOnMoneyBags()
{
    if ImageSearchAndClick(images.money_bag_full, "bag", "mouseover", "item") {
                                                                            ToolTip "Clicking the FULL money bag :')...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
        sleep_random(400, 1500)
        Click("Left")
        sleep_random(500, 1500)
        return true
    }
    return false
}

; 1 in 4 chance to click the money bag in your inventory
ClickMoneyBag()
{
    lucky_number := Random(1,5)
    if !(lucky_number = 4)
        return false    
    
    SendKey(1)
    if ImageExists(images.open_bag) {                                       ;ensure bag is open
        sleep_random(10, 100)
        if ImageSearchAndClick(images.money_bag, "bag", "mouseover", "item")
                                                                            ToolTip "Clicking the money bag...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
            sleep_random(500, 1500)
            Click("Left")
            sleep_random(500, 1500)
            return true
    }
                                                                            ToolTip "", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return false
}

; at this point, the right click menu in the game is open, now we left click the knockout option
ClickKnockout() {
                                                                            ToolTip "Trying to click knockout...", X_TOOLTIP.2, Y_TOOLTIP.2, 2    
    ; if the knockout option isn't visible, wait for a bit
    WaitForImage(images.knockout_option, 200)
    if ImageSearchAndClick(images.knockout_option,, "mouseover", "option") {
                                                                            ToolTip "Clicking knockout...", X_TOOLTIP.2, Y_TOOLTIP.2, 2 
        Sleep 300
        Click "Left"
        Sleep 100
        return true
    }
    ; If we've reached here, timeout has passed without detecting the image
                                                                            ToolTip "Couldn't click knockout in time... Restarting in 3 to 4 sec", X_TOOLTIP.2, Y_TOOLTIP.2, 2
    return false    ; failed? give up hombre
}

; at this point, the right click menu in the game is open, and we either just knocked them out, or it was a glancing blow and they are
;   about to attack. To counteract their attack, we can click pickpocket on them.
ClickPickpocket(timeout_ms := 300) {
                                                                            ToolTip "Trying to click pickpocket...", X_TOOLTIP.2, Y_TOOLTIP.2, 2
    if ImageSearchAndClick(images.pickpocket_option, "under_mouse", "mouseover", "option") {
        Sleep 100
        Click("Left")
        return true
    }                                                       ; if we've reached here, timeout_ms has passed without detecting the image
                                                                            ToolTip "Couldn't click pickpocket in time... Restarting in 3 to 4 sec.", X_TOOLTIP.2, Y_TOOLTIP.2, 2
    sleep_random(500, 1500)
    return false                                            ; failed.. give up hombre
}

; right clicks around the chest area of the NPC
RightClickNPC()
{
    ; clicks need to be fast (but not instant), we'll add sleeps when necessary
    SetDefaultMouseSpeed(1)

    ; Get the target click area
    click_area := GetTargetClickArea()
    offset_x := Random(-50, 50)
    offset_y := Random(-70, 70)

    x := click_area.x + offset_x                            ; randomize within the area and right click
    y := click_area.y + offset_y
    MouseMove(x, y)

    if WaitForImage(images.menaphite_hovering_text, 700) {  ; if target is in sight
        Click("Right")                                      ; right click
                                                                            ToolTip("Right Clicking:`roffset x:" offset_x ", y:" offset_y "`rx:" click_area.x ", y:" click_area.y, X_TOOLTIP.3, Y_TOOLTIP.3, 3)
        return true
    }
    return false
}

ClickPixel(color, coord_obj:="None", offsetInput:="None")
{
    offset := GetOffset(offsetInput)
    pixel_search_and_click(coord_obj.x1, coord_obj.y1, coord_obj.x2, coord_obj.y2, color, "left", offset.x, offset.y)
}

; ClickCurtain() assumes you've zoomed in and are facing north and are in the small building by curtain.
ClickCurtain(sleepTime := 1500)
{
    if pixel_search_and_click(0, 20, A_ScreenWidth-20, A_ScreenHeight, pixel_color.object_green, "right",,,0)
    {
        if ImageSearchAndClick(images.open_curtain_option, "under_mouse", "left", "option_short") or
            ImageSearchAndClick(images.close_curtain_option, "under_mouse", "left", "option_short") 
            sleep_random(sleepTime, sleepTime + 1500)
            return true
    }
    return false
}

ClickNotedLobsters()
{
    if ImageSearchAndClick(images.lobster_cooked_noted, coord.bag, "left", "item2")
        return true
    return false
}

LeftClickNPC()
{
    if PixelSearchAndClick(pixel_color.npc, "p1", "mouseover") or PixelSearchAndClick(pixel_color.npc, "p2", "mouseover")
        or PixelSearchAndClick(pixel_color.npc, "p4", "mouseover") or PixelSearchAndClick(pixel_color.npc, "p5", "mouseover")
        or PixelSearchAndClick(pixel_color.npc_dark, "p1", "mouseover") or PixelSearchAndClick(pixel_color.npc_dark, "p2", "mouseover")
        or PixelSearchAndClick(pixel_color.npc_dark, "p4", "mouseover") or PixelSearchAndClick(pixel_color.npc_dark, "p5", "mouseover")
    {
        Click("Left")
        return true
    }
    return false
}

ReloadLobsters() ;TODO randomize the times
{
    while(!ClickCurtain(2500))
        sleep_random(500, 1500)
    PixelSearchAndClick(pixel_color.tile_teal, "p6", "left")
    sleep_random(2500, 2500)
    ClickCurtain(500)

    zoom("out")
    PressAndHoldKey("W", 1700)
    sleep_random(500, 1500)
    PixelSearchAndClick(pixel_color.tile_pink, "p2", "left", "tile")
    sleep_random(6000,7500)
    PixelSearchAndClick(pixel_color.tile_teal, "p2", "left")
    zoom("in")
    ClickNotedLobsters()
    sleep_random(7500,7500)
    LeftClickNPC()
    sleep_random(2500,2500)
    randNum := Random(300, 300)
    PressAndHoldKey("3", randNum)
    sleep_random(1500,1500)
    zoom("out")
    PixelSearchAndClick(pixel_color.tile_pink, "p5", "left", "tile")
    sleep_random(8500, 8500)
    while(!ClickCurtain(7500))
        sleep_random(500, 1500)
    zoom("in")
    sleep_random(4500, 4500)
    PixelSearchAndClick(pixel_color.tile_pink, "p5", "left", "tile_sw")
    sleep_random(1500, 1500)
    ClickCurtain(500)
    sleep_random(700, 700)
    PixelSearchAndClick(pixel_color.tile_pink, "p5", "left")

}

