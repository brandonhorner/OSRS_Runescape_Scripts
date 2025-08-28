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

SetWorkingDir "C:\Git\OSRS_Runescape_Scripts\ardy_knight"

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"

; this is the path to the QRes executable, if you don't have it, you can download it from here: https://sourceforge.net/projects/qres/
global qres_path := "C:\Tools\QRes\QRes.exe"

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")


F1::
{
    if WinActive(runelite_window)
        Main()
}

+F1::
{
    ; Switch to 2560x1440 resolution
    ChangeResolution(2560, 1440)
    sleep_random(300, 500)
    Reload()

}

F2::
{
    ; Switch to 2560x1440 resolution
    ChangeResolution(2560, 1440)
    sleep_random(300, 500)
}

^F2::ExitApp()

Main()
{
    setup_in()
    noNPCtoRight := 0
    clickAttempts := 0
    totalMoneyMade := 0
    fullMoneyBagsOpened := 0
    totalMoneyBags := 0

    while(noNPCtoRight < 150)
    {
        ; set the click location. each time we are full on money bags this will reset
        x := Random(1105, 1185)
        y := Random(485, 545)
        
        ; while we don't have full money bags, let's
        while (noNPCtoRight < 150)
        {
            ; make sure menu is closed
            if(menu_is_open()) {
                MsgBox "Close the menu in Runelite to continue."
                continue
            }
            
            ;1. Preliminaries ----------------------
            ; if CheckIfStunned()
            ;     continue                                                        ; check if we are stunned, wait it out if we are
            
            ; if HealthIsLow() {                                                   ; check if health is low

            ;     ClickMoneyBag()

            ;     if !EatLobster() {                                             ; try to eat a lobster if it is

            ;         ReloadFood()                                                 ; pause for player to reload inventory if you're out of lobbies
            ;     }
            ; }
            ; ; -------------------------------------
            WaitForTick()
            
            ;2. Main Loop --------------------------
            ; Wait for the next tick, then left click the ardy night.. then wait some more.
            if EnemyToRight()
            {
                LeftClickArdyKnight(x, y)
            }
            else
            { 
                PixelSearchAndClick(pixel_color.tile_purple, "p2", "left", "tile_se")
                sleep_random(800, 5000)
                noNPCtoRight++
            }

            clickAttempts++
            ToolTip "Counter:`nSingle pickpocket (clicks attempted, not pickpockets): " clickAttempts "`nComplete stacks of money bags: " fullMoneyBagsOpened " (" totalMoneyBags " total)`nNPC wasn't to the right " noNPCtoRight " times.`nYou made " totalMoneyMade " gold this run.", X_TOOLTIP.9, Y_TOOLTIP.9, 9
            
            WaitForTick()

            if (CheckIfFullOnMoneyBags())
            {
                fullMoneyBagsOpened++
                totalMoneyMade := fullMoneyBagsOpened * 28 * 100
                totalMoneyBags := fullMoneyBagsOpened * 28
                break
            }
        }
    }
}

EnemyToRight()
{   ;1115, 410, 1230, 575
    loop(3)
    {
        if (PixelSearchAndClick(pixel_color.npc,,,,1115, 410, 1230, 575, 30))
            {
                return true
            }
            sleep_random(200, 500)    
    }
    return false
}

setup_in()
{
    if WinActive(runelite_window)
    {
        ; Switch to 1920x1080 resolution
        ChangeResolution(1920, 1080)
        sleep_random(300, 500)

        ;zoom all the way out
        zoom("in")
        sleep_random(100, 200)
        Send("{W down}")
        ;Face North (click compass)
        ClickCompass()
        sleep_random(2000, 2000)
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
    MouseMove(x, y)
    sleep_random(120, 210)
    Click
}