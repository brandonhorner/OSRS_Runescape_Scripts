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
global runelite_window := "RuneLite - Bradensky"

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")


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

    while(true)
    {
        ; set the click location. each time we are full on money bags this will reset
        x := Random(638, 741)
        y := Random(462, 626)
        
        ; while we don't have full money bags, let's
        while (true)
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
        if StallToLeft()
        {
            LeftClickCakeStall(x, y)
        }
        else
        {
            sleep_random(300, 800)
        }
        clickAttempts++
        sleep_random(200,300)
        WaitForTick()

        ToolTip "Counter:`nClicks attempted:" clickAttempts, X_TOOLTIP.9, Y_TOOLTIP.9, 9
        ; wait for the final message for double pickpocket (or 2 ticks)   
        }

    }
}


StallToLeft()
{   ;1115, 410, 1230, 575
    if (PixelSearchAndClick(pixel_color.npc,,,, 426, 231, 763, 667, 30))
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
        sleep_random(800, 1200)
        Send("{W up}")
    }
}

ReloadFood()
{
    MsgBox("Go get food then come back and press OK")
}

/*Assumes you will be replacing your left click option with pickpocket*/
LeftClickCakeStall(x, y)
{
    Click x, y, "Left"
}
