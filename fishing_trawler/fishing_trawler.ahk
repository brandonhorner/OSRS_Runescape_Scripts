#Requires AutoHotkey v2.0
#SingleInstance Force
#Include ..\utilities.ahk

SetWorkingDir "C:\Git\OSRS_Runescape_Scripts\fishing_trawler"

global runelite_window := "RuneLite - BinaryBilly"

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"


clickFishingTrawlerNet() {
    global images

    interactedSuccessfully := false
    failedToClickTrawlerNet := 0

    while (!interactedSuccessfully && failedToClickTrawlerNet < 10)
    {
        ToolTip "ClickFishingTrawlerNet: Searching for Trawler Net pixel...", X_TOOLTIP.9, Y_TOOLTIP.9, 9
        foundTrawlerNet := PixelSearchAndClick(
            0xFF0000,   ; PixelColor (#FFFF0000)
            "p2",       ; scanAreaInput (p2 = top middle of screen)
            "right",    ; click_type
            "trawler_net",   ; offset (random offset down/right)
            ,,,,
            5          ; shade_variance
        )
        if (!foundTrawlerNet)
        {
            ToolTip "ClickFishingTrawlerNet: Could not find red pixel.", X_TOOLTIP.9, Y_TOOLTIP.9, 9
            failedToClickTrawlerNet++
            sleep_random(300, 500)
            continue
        }
        else
        {
            ToolTip "ClickFishingTrawlerNet: Found net pixel! Right-clicked.", X_TOOLTIP.9, Y_TOOLTIP.9, 9
            sleep_random(500, 700)
        }

        ; Now look for the confirmation (e.g., "Inspect Trawler net")
        ToolTip "ClickFishingTrawlerNet: Searching for confirmation image...", X_TOOLTIP.9, Y_TOOLTIP.9, 9
        foundInteractTrawlerNetOption := ImageSearchAndClick(
            images.inspect_trawler_net,
            "p2",         ; scanAreaInput (p2 = full screen)
            "left",       ; click_type (to left-click)
            "option",     ; offset
            ,,,,
            5             ; shade_variance
        )
        if (!foundInteractTrawlerNetOption)
        {
            failedToClickTrawlerNet++
            ToolTip "ClickFishingTrawlerNet: Confirmation NOT found. Attempts so far: " failedToClickTrawlerNet, X_TOOLTIP.9, Y_TOOLTIP.9, 9
            sleep_random(500, 700)
            continue ;the loop
        }
        else
        {
            ToolTip "ClickFishingTrawlerNet: Confirmation found! Looted successfully.", X_TOOLTIP.9, Y_TOOLTIP.9, 9
            interactedSuccessfully := true
            sleep_random(1200, 1500)
        }

        ; Finally we click the bank all button
        foundBankAllTrawlerNet := ImageSearchAndClick(
            images.bank_all_trawler_net,
            "p2",         ; scanAreaInput (p2 = full screen)
            "left",       ; click_type (to left-click)
            "item",       ; offset
            ,,,,
            5             ; shade_variance
        )
        if (!foundBankAllTrawlerNet)
        {
            ToolTip "ClickFishingTrawlerNet: Bank all NOT found. Attempts so far: " failedToClickTrawlerNet, X_TOOLTIP.9, Y_TOOLTIP.9, 9
            failedToClickTrawlerNet++
            sleep_random(500, 750)
            continue
        }
        else
        {
            ToolTip "ClickFishingTrawlerNet: Bank all found! Banked successfully.", X_TOOLTIP.9, Y_TOOLTIP.9, 9
            sleep_random(1200, 1500)
        }
    }

}

^`::
{
    ;testing things here
    clickFishingTrawlerNet()
}

^F1::
{
    if (menu_is_open())
    {
        MsgBox "Menu is open, close it."
    }
    
    runIteration := 0

    while (true)
    {
        ; if we are on our first run we don't need to check the fishing trawler net
        if runIteration > 0
        {
            clickFishingTrawlerNet()
        }
        

        sleep_random(1500, 2500)
    }
}

+`::Reload()

    