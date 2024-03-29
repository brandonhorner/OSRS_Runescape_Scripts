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
;#Include ..\utilities.ahk
#Include ..\utilities_controlclick.ahk

SetWorkingDir A_MyDocuments "\AutoHotkey_Scripts\runescape"

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"

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
    SetupZoomIn()
    noNPCtoRight := 0
    clickAttempts := 0
    fullMoneyBagOpens := 0

    while(noNPCtoRight < 10)
    {
        ; set the click location. each time we are full on money bags this will reset
        x := Random(1085, 1165)
        y := Random(480, 525)
        
        ; while we don't have full money bags, let's
        while (!CheckIfFullOnMoneyBags() or noNPCtoRight < 10)
        {
            ; make sure menu is closed
            if(menu_is_open()) {
                MsgBox "Close the menu in Runelite to continue."
                continue
        }
        
        ; then complete preliminaries ----------------------
        if CheckIfStunned()
            continue                                                       ; check if we are stunned, wait it out if we are
        
        if HealthIsLow() {                                                 ; check if health is low

            ClickMoneyBag()

            if !EatLobster() {                                             ; try to eat a lobster if it is

                ReloadFood()                                               ; pause for player to reload inventory if you're out of lobbies
            }
        }
        ; -------------------------------------
        ; obligitory sleep command seemed nice, might delete later
        WaitForTick()
        SleepRandom(300,500)

        ; wait for the next tick, then left click the ardy knight.. then wait some more.
        if EnemyToRight()
        {
            LeftClickArdyKnight(x, y)
        }
        else
        { 
            PixelSearchAndClick(pixel_color.tile_purple, "p2", "left", "tile_se")
            SleepRandom(4000, 8000)
            noNPCtoRight++
        }

        clickAttempts++
        SleepRandom(200,300)
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
    if ( PixelSearchAndClick(pixel_color.npc,,,,1115, 410, 1230, 575, 30))
    {
        return true
    }
    return false
}

SetupZoomIn()
{
    if WinActive(runelite_window)
    {
        ;zoom all the way out
        zoom("in")
        SleepRandom(100, 200)
        ControlSend "{W Down}",, runelite_window
        ;Face North (click compass)
        click_compass()
        SleepRandom(1000, 1000)
        ControlSend "{W up}",, runelite_window

    }
}

ReloadFood()
{
    MsgBox("Go get food then come back and press OK")
}

/*Assumes you will be replacing your left click option with pickpocket*/
LeftClickArdyKnight(x, y)
{
    ControlClick "x" x " y" y, runelite_window,, "Left"
}