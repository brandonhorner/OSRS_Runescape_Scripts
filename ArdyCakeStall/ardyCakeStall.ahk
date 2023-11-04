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

F3::
{
    if PixelSearchAndClick(pixel_color.tile_pink, "p2", "mouseover", "south") or PixelSearchAndClick(pixel_color.tile_pink, "p3", "mouseover", "south")
    {
        Click
        ToolTip "Made it", 5, 5, 1
    }
    else{
        ToolTip "No", 5, 5, 1
    }    
    return
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
    SetupZoomIn()
    sleep_random(500,1000)
    clickAttempts := 0
    runs := 0
    while(true)
    {
        ; set the click location. each time we are full on money bags this will reset
        x := Random(638, 741)
        y := Random(462, 626)
        
        ; while we don't have full money bags, let's
        while (runs < 10)
        {
            ; make sure menu is closed
            if(menu_is_open()) {
                MsgBox "Close the menu in Runelite to continue."
                continue
        }
        
        ;1. Preliminaries ----------------------
        if HealthIsLow() or InventoryIsFull(){                                                   ; check if health is low
            runs++
            BankItems()
            ReturnToStall()
            SetupZoomIn()
            sleep_random(500,1000)
        }
        ; -------------------------------------
        sleep_random(350, 450)

        ; Wait for the next tick, then left click the ardy night.. then wait some more.
        if StallToLeft()
        {
            LeftClickCakeStall(x, y)
        }
        else
        {
            sleep_random(200, 700)
        }
        clickAttempts++

        ToolTip "Counter:`nClicks attempted:" clickAttempts "`nRuns: " runs, X_TOOLTIP.9, Y_TOOLTIP.9, 9
        ; wait for the final message for double pickpocket (or 2 ticks)   
        }

    }
    return
}

BankItems()
{
    ClickMiniMap("bank_from_cake_stall")
    ToolTip "Sleeping 30s" 500, 200, 8
    sleep_random(33000, 37000)
    ToolTip "" 500, 200, 8

    zoom("out", 5)
    sleep_random(250, 450)
    
    DepositBoxOpen(0)
    sleep_random(1500, 3000)

    QuickDepositAll()
    sleep_random(500, 1000)

    return true
}

DepositBoxOpen(index)
{
    ; click the deposit box
    if PixelSearchAndClick(pixel_color.npc, "p4", "mouseover", "southish") or PixelSearchAndClick(pixel_color.npc, "p5", "mouseover", "southish") or PixelSearchAndClick(pixel_color.npc, "p6", "mouseover", "southish")
    {
        Click
        if WaitForImage(images.deposit_inventory) 
            return true
    }
    else
    {
        zoom("out", 2)
        sleep_random(300, 500)
        if(index < 5)
            DepositBoxOpen(index)
        else
            return false
    }
}

QuickDepositAll()
{
    ; click the deposit inventory button
    if ImageSearchAndClick(images.deposit_inventory, "p5", "left", "item")
        return true
    return false
}

ClickMiniMap(minimap_icon_img_path)
{
    switch minimap_icon_img_path {
        case "cake_stall":
            x := Random(1820, 1826) 
            y := Random(50, 52)

        case "bank_from_cake_stall":
            x := Random(1767, 1774)
            y := Random(155, 165)
    }

    Click(x,y)
}

StallToLeft()
{   ;1115, 410, 1230, 575
    if (PixelSearchAndClick(pixel_color.npc, "p5",,, 426, 231, 763, 667, 30))
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
        sleep_random(100, 200)
        Send("{W down}")
        ;Face North (click compass)
        click_compass()
        sleep_random(800, 1200)
        Send("{W up}")
    }
}

ReturnToStall()
{
    ClickMiniMap("cake_stall")
    
    zoom("in")
    zoom("out", 10)

    ToolTip "Sleeping 30s" 500, 200, 8
    sleep_random(33000, 37000)
    ToolTip "" 500, 200, 8

    if PixelSearchAndClick(pixel_color.tile_pink, "p2", "mouseover", "tile_se_reduced") or PixelSearchAndClick(pixel_color.tile_pink, "p3", "mouseover", "tile_se_reduced")
        Click
    sleep_random(6000, 9000)
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
