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


; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"


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
        sleep_random(425, 425) ; WAS 725
        CheckAndUpdateStatus(&knockout_failure, &pickpocket_failure)
                                                                    ToolTip "Pickpocket  (1 of 2).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        if !ClickPickpocket()                                       ; if it fails to click pickpocket
            continue                                                ; start the loop over
        
        sngl_pickpockets++
                                                                    ToolTip "Counters:`nSingle pickpockets: " sngl_pickpockets "`nDouble pickpockets: " dbl_pickpockets, X_TOOLTIP.9, Y_TOOLTIP.9, 9
        if CheckIfStunned()
            continue                                                        ; check if we are stunned, wait it out if we are
        CheckIfCombat()
                                                                    ToolTip "Right click (3 of 3).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        RightClickNPC()                                             ; right click the NPC again
        CheckAndUpdateStatus(&knockout_failure, &pickpocket_failure)
        WaitForPickpocketAttempt()
        ;if (knockout_failure and pickpocket_failure) {              ; if the pickpocket failed,
        ;                                                            ToolTip "Epic failure, restarting in .5 to 1.5s", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        ;    sleep_random(500, 1500)
        ;    MsgBox "We in combat..."
        ;    Reload                                                 ; we are in combat :\ Reload.
        ;}
                                                                    ToolTip "Pickpocket  (2 of 2).", X_TOOLTIP.4, Y_TOOLTIP.4, 4
        sleep_random(550,570)
        if !ClickPickpocket()                                       ; try to pickpocket                      
            continue                                                ; start the loop over
        
        dbl_pickpockets++
                                                                    ToolTip "Counters:`nSingle pickpockets: " sngl_pickpockets "`nDouble pickpockets: " dbl_pickpockets, X_TOOLTIP.9, Y_TOOLTIP.9, 9
                                                                    ; wait for the final message for double pickpocket (or 2 ticks)   
    }
}

setup_in()
{
    if WinActive(runelite_window)
    {
        ;zoom all the way out
        zoom("in")
        sleep_random(100, 200)
        
        ;Face North (click compass)
        click_compass()
        sleep_random(100, 200)
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

CheckIfCombat()
{
                                                                            ToolTip "Stunned. Waiting...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    if ImageSearchAndClick(images.cant_pickpocket_combat, "chat_bottom_2",,,,,,,5)
    {
        sleep_random(150, 300)
        PixelSearchAndClick(pixel_color.tile_purple, "p5", "left")
        sleep_random(6000,7500)
        PixelSearchAndClick(pixel_color.npc, "p2", "right")
        sleep_random(300, 500)
        ClickKnockout()
        sleep_random(425, 425)
        ClickPickpocket()
        return true
    }
                                                                            ToolTip "", X_TOOLTIP.1, Y_TOOLTIP.1, 1
    return false
}

ClickPixel(color, coord_obj:="None", offsetInput:="None")
{
    offset := GetOffset(offsetInput)
    pixel_search_and_click(coord_obj.x1, coord_obj.y1, coord_obj.x2, coord_obj.y2, color, "left", offset.x, offset.y)
}

; ClickCurtain() assumes you've zoomed in and are facing north and are in the small building by curtain.
ClickCurtain(scanArea := "None")
{
    if PixelSearchAndClick(pixel_color.object_green, "p5", "right")
    {
        sleep_random(300, 500)
        if (ImageSearchAndClick(images.open_curtain_option, "under_mouse", "left", "option_short") or
            ImageSearchAndClick(images.close_curtain_option, "under_mouse", "left", "option_short"))
        {
            return true
        }
        else{
            MouseMove(150, -150, 5, "Relative")
            sleep_random(300, 500)
            ClickCurtain()
        }
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
    if PixelSearchAndClick(pixel_color.npc, "p1", "left") or PixelSearchAndClick(pixel_color.npc, "p2", "left")
        or PixelSearchAndClick(pixel_color.npc, "p4", "left") or PixelSearchAndClick(pixel_color.npc, "p5", "left")
        or PixelSearchAndClick(pixel_color.npc_dark, "p1", "left") or PixelSearchAndClick(pixel_color.npc_dark, "p2", "left")
        or PixelSearchAndClick(pixel_color.npc_dark, "p4", "left") or PixelSearchAndClick(pixel_color.npc_dark, "p5", "left")
    {
        sleep_random(1500, 1500)
        if ImageSearchAndClick(images.select_an_option, "chat")
            return true
        ClickNotedLobsters() 
        LeftClickNPC()
    }
    return false
}

ReloadLobsters() ;TODO randomize the times
{
    while(!ClickCurtain())
        sleep_random(500, 1500)
    sleep_random(1500, 1500)

    PixelSearchAndClick(pixel_color.tile_teal, "p6", "left", "tile_sw")
    sleep_random(1500, 1500)
    
    while(!ClickCurtain("p5"))
        sleep_random(500, 1500)
    sleep_random(500, 500)

    zoom("out")
    PressAndHoldKey("W", 1500)
    PixelSearchAndClick(pixel_color.tile_pink, "p2", "left", "tile")
    sleep_random(6000,7500)
    PixelSearchAndClick(pixel_color.tile_teal, "p2", "left")
    zoom("in")
    ClickNotedLobsters()
    sleep_random(7500,7500)
    LeftClickNPC()
    sleep_random(1500,1500)
    randNum := Random(300, 300)
    PressAndHoldKey("3", randNum)
    sleep_random(1500,1500 )
    zoom("out")
    PixelSearchAndClick(pixel_color.tile_pink, "p5", "left", "tile")
    sleep_random(8500, 8500)
    
    while(!ClickCurtain())
        sleep_random(500, 1500)
    sleep_random(7500, 7500)

    zoom("in")
    sleep_random(4500, 4500)
    PixelSearchAndClick(pixel_color.tile_pink, "p5", "left", "tile_sw")
    sleep_random(3500, 3500)

    while(!ClickCurtain("p4"))
        sleep_random(500, 1500)
    sleep_random(500, 500)
    
    sleep_random(700, 700)
    PixelSearchAndClick(pixel_color.tile_pink, "p5", "left")
}

