#Requires AutoHotkey v2.0
#SingleInstance Force
#Include ..\utilities.ahk

SetWorkingDir "C:\Git\OSRS_Runescape_Scripts\fishing_trawler"

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"

; ==========================
; Enhanced Sequential Tooltip System
; ==========================
;
; This version stores each message in a global buffer and displays them all in a single tooltip.
; After 10 messages, it starts overwriting the oldest entry.
;
; USAGE:
;   Instead of ToolTip "some text", do: ShowSequentialTooltip("some text")
;   That way, you'll see an accumulating list of the last 10 messages.

global tooltipHistory := [] ; holds up to 10 messages

ShowSequentialTooltip(msg) {
    global tooltipHistory, X_TOOLTIP, Y_TOOLTIP

    ; Add the new message to the list
    tooltipHistory.Push(msg)

    ; If we exceed 10, remove the oldest
    if (tooltipHistory.Length > 10) {
        tooltipHistory.RemoveAt(1)
    }

    ; Build a multiline text block showing recent messages
    displayText := ""
    for idx, item in tooltipHistory {
        displayText .= item "`n"
    }

    ; Show them in a single tooltip
    ToolTip(displayText, X_TOOLTIP.9, Y_TOOLTIP.9, 9)
}

clickFishingTrawlerNet() {
    global images

    interactedSuccessfully := false
    failedToClickTrawlerNet := 0
    maxAttempts := 100

    while (!interactedSuccessfully && failedToClickTrawlerNet < maxAttempts)
    {
        if (!tryRightClickTrawlerNet()) {
            failedToClickTrawlerNet++
            continue
        }
        if (!tryConfirmTrawlerNet()) {
            failedToClickTrawlerNet++
            continue
        }
        if (!waitForBankAllButton()) {
            failedToClickTrawlerNet++
            continue
        }

        interactedSuccessfully := true
    }
}

tryRightClickTrawlerNet() {
    ShowSequentialTooltip("[TrawlerNet] Searching for Trawler Net pixel...")

    foundTrawlerNet := PixelSearchAndClick(
        0xFF0000,      ; PixelColor (#FFFF0000)
        "p2",          ; scanAreaInput (top-middle portion of screen)
        "mouseover",   ; click_type
        "trawler_net", ; offset (random offset down/right)
        0,0,0,0,       ; x1,y1,x2,y2
        5              ; shade_variance
    )

    if (!foundTrawlerNet)
    {
        ShowSequentialTooltip("[TrawlerNet] Could not find red pixel.")
        sleep_random(500, 700)
        return false
    }
    sleep_random(400, 700)
    Click("right")
    ShowSequentialTooltip("[TrawlerNet] Found net pixel! Right-clicked.")
    return true
}

tryConfirmTrawlerNet() {
    ShowSequentialTooltip("[TrawlerNet] Searching for confirmation image...")

    foundInteractTrawlerNetOption := ImageSearchAndClick(
        images.inspect_trawler_net, ; For example, images.inspect_trawler_net
        "p2",                       ; scanAreaInput
        "mouseover",                ; click_type
        "option_short",            ; offset
        0,0,0,0,
        5                           ; shade_variance
    )

    if (!foundInteractTrawlerNetOption)
    {
        ShowSequentialTooltip("[TrawlerNet] Confirmation NOT found.")
        sleep_random(500, 700)
        return false
    }
    ShowSequentialTooltip("[TrawlerNet] Confirmation found! Looted successfully.")
    sleep_random(400, 700)
    Click()
    sleep_random(4500, 5700)
    return true
}

waitForBankAllButton() {
    maxAttempts := 20 
    ShowSequentialTooltip("[TrawlerNet] Waiting for 'Bank all' button to appear...")
    while (!tryClickBankAll() && !trawlerLootMessageExists() && maxAttempts > 0) 
    {
        sleep_random(800, 1000)
        maxAttempts--
    }
    if (maxAttempts == 0)
    {
        ShowSequentialTooltip("[TrawlerNet] 'Bank all' button not found.")
        return false
    }
    return true
}

tryClickBankAll() {
    ShowSequentialTooltip("[TrawlerNet] Searching for 'Bank all' button...")
    foundBankAllButton := ImageSearchAndClick(
        images.bank_all_trawler_net, ; For example, images.bank_all_trawler_net
        "0",                       ; scanAreaInput
        "mouseover",                ; click_type
        "item",                     ; offset
        0,0, A_ScreenWidth, A_ScreenHeight,
        5                            ; shade_variance
    )
    if (!foundBankAllButton)
    {
        ShowSequentialTooltip("[TrawlerNet] Bank all not found.")
        return false
    }
    sleep_random(100, 200)
    Click()
    ShowSequentialTooltip("[TrawlerNet] Bank all found! Banked successfully.")
    return true
}

trawlerLootMessageExists() {
    global images

    ShowSequentialTooltip("[TrawlerNet] Searching for message in chatbox stating that we don't have trawler loot...")
    foundTrawlerLootMessage := ImageSearchAndClick(
        images.no_loot_trawler_net, ; For example, images.no_loot_trawler_net
        "v2",                       ; scanAreaInput
        "mouseover",                ; click_type
        "no offset",
        0,0,0,0,
        5                           ; shade_variance
    )
    if (foundTrawlerLootMessage)
    {
        ShowSequentialTooltip("[TrawlerNet] Message found-- No loot in net.")
        return true
    }
    return false
}


clickGangPlank() {
    global images

    interactedSuccessfully := false
    failedToClickGangPlank := 0
    maxAttempts := 10

    while (!interactedSuccessfully && failedToClickGangPlank < maxAttempts)
    {
        if (!tryRightClickGangPlank()) {
            failedToClickGangPlank++
            continue
        }
        if (!tryConfirmGangPlank()) {
            failedToClickGangPlank++
            continue
        }

        interactedSuccessfully := true
    }
}

tryRightClickGangPlank() {
    ShowSequentialTooltip("[GangPlank] Searching for Gang Plank pixel...")

    foundGangPlank := PixelSearchAndClick(
        0x00FFFF,      ; PixelColor (#FFFF0000) ???
        "p3",         ; scanAreaInput (top-middle portion of screen)
        "mouseover",  ; click_type
        "gangplank",  ; offset (random offset down/right)
        0,0,0,0,       ; x1,y1,x2,y2
        5              ; shade_variance
    )

    if (!foundGangPlank)
    {
        ShowSequentialTooltip("[GangPlank] Could not find gang plank pixel.")
        sleep_random(500, 700)
        return false
    }
    sleep_random(400, 700)
    Click("right")
    ShowSequentialTooltip("[GangPlank] Found gang plank pixel! Right-clicked.")
    return true
}

tryConfirmGangPlank() {
    ShowSequentialTooltip("[GangPlank] Searching for confirmation image...")

    foundInteractGangPlankOption := ImageSearchAndClick(
        images.cross_gangplank, ; For example, images.cross_gangplank
        "p3",                  ; scanAreaInput
        "mouseover",           ; click_type
        "option_short",        ; offset
        0,0,0,0,
        5                       ; shade_variance
    )

    if (!foundInteractGangPlankOption)
    {
        ShowSequentialTooltip("[GangPlank] Confirmation NOT found.")
        sleep_random(500, 700)
        return false
    }
    ShowSequentialTooltip("[GangPlank] Confirmation found! Crossing.")
    sleep_random(400, 700)
    Click()
    sleep_random(7000, 10000)
    return true
}

waitForLoadingScreen() {
    global images
    attempts := 0
    while (attempts < 300)
    {
        ShowSequentialTooltip("[Waiting] Waiting for Fishing Trawler loading screen... Attempt #" attempts)
        foundSailingText := ImageSearchAndClick(
            images.you_sail_out_to_see_text, 
            "v2", 
            "mouseover", 
            "no offset",
            0,0,0,0, 
            5
        )
        if (foundSailingText)
        {
            ShowSequentialTooltip("[Waiting] Found Fishing Trawler loading screen! Round starting in 12s.")
            sleep_random(12000, 12000)
            break
        }
        attempts++
        sleep_random(1000, 2000)
    }
}

clickLadder() {
    global images

    interactedSuccessfully := false
    failedToClickLadder := 0
    maxAttempts := 20

    while (!interactedSuccessfully && failedToClickLadder < maxAttempts)
    {
        if (!tryRightClickLadder()) {
            failedToClickLadder++
            continue
        }
        if (!tryConfirmClimbLadder()) {
            failedToClickLadder++
            continue
        }

        interactedSuccessfully := true
    }
}

tryRightClickLadder() {
    ShowSequentialTooltip("[Ladder] Searching for Ladder pixel...")

    foundLadder := PixelSearchAndClick(
        0xFF00FF,      ; PixelColor (#FFFF00FF) pink
        "h1",         ; scanAreaInput (top-middle portion of screen)
        "mouseover",  ; click_type
        "ladder",     ; offset (random offset down/right)
        0,0,0,0,       ; x1,y1,x2,y2
        5              ; shade_variance
    )

    if (!foundLadder)
    {
        ShowSequentialTooltip("[Ladder] Could not find ladder pixel.")
        sleep_random(500, 700)
        return false
    }
    sleep_random(400, 700)
    Click("right")
    ShowSequentialTooltip("[Ladder] Found ladder pixel! Right-clicked.")
    return true
}

tryConfirmClimbLadder() {
    ShowSequentialTooltip("[Ladder] Searching for confirmation image...")

    foundInteractLadderOption := ImageSearchAndClick(
        images.climb_ship_ladder, ; For example, images.climb_ship_ladder
        "h1",                  ; scanAreaInput
        "mouseover",           ; click_type
        "option_short",        ; offset
        0,0,0,0,
        5                       ; shade_variance
    )

    if (!foundInteractLadderOption)
    {
        ShowSequentialTooltip("[Ladder] Confirmation NOT found.")
        sleep_random(500, 700)
        return false
    }
    ShowSequentialTooltip("[Ladder] Confirmation found! Climbing.")
    sleep_random(400, 700)
    Click()
    sleep_random(2000, 3000)
    return true
}

clickPinkTile() {
    global images

    interactedSuccessfully := false
    failedToClickPinkTile := 0
    maxAttempts := 20

    while (!interactedSuccessfully && failedToClickPinkTile < maxAttempts)
    {
        if (!tryRightClickPinkTile()) {
            failedToClickPinkTile++
            continue
        }
        interactedSuccessfully := true
    }
}

tryRightClickPinkTile() {
    ShowSequentialTooltip("[PinkTile] Searching for Pink Tile pixel...")

    foundPinkTile := PixelSearchAndClick(
        0xFF00FF,      ; PixelColor (#FFFF00FF) pink
        ,             ; omit for custom scan area
        "mouseover",  ; click_type
        "tile_se_reduced",    ; offset (random offset down/right)
        0, 0, A_ScreenWidth ,A_ScreenHeight, ; x1,y1,x2,y2
        5              ; shade_variance
    )
    if (!foundPinkTile)
    {
        ShowSequentialTooltip("[PinkTile] Could not find pink tile pixel in scan area: " A_ScreenWidth "x" A_ScreenHeight)
        sleep_random(500, 700)
        return false
    }
    sleep_random(400, 700)
    Click()
    ShowSequentialTooltip("[PinkTile] Found pink tile pixel! Left-clicked.")
    return true
}

; Here we will pixel search and click for the kraken (teal pixels in p2 area),
; then we also search for a kraken in the south (teal pixels in p4 area). Depending on which one is found,
; that will determine the offset to use (north_kraken, south_kraken). Then we just repeatedly click for
; 6 seconds every second 
clickKraken() {
    global images

    interactedSuccessfully := false
    failedToClickKraken := 0
    maxAttempts := 5

    while (!interactedSuccessfully && failedToClickKraken < maxAttempts)
    {
        if (!tryRightClickKraken()) {
            failedToClickKraken++
            continue
        }
        if (!tryConfirmClickKraken()) {
            failedToClickKraken++
            continue
        }
        interactedSuccessfully := true
    }
}

tryRightClickKraken() {
    ShowSequentialTooltip("[Kraken] Searching for Kraken (Teal Pixel)...")

    foundNorthKraken := PixelSearchAndClick(
        0x00FFFF,      ; PixelColor (#FF00FFFF) teal
        "p2",         ; scanAreaInput (top-middle portion of screen)
        "mouseover",  ; click_type
        "north_kraken",  ; offset (random offset down)
        0,0,0,0,       ; x1,y1,x2,y2
        5              ; shade_variance
    )
    foundSouthKraken := PixelSearchAndClick(
        0x00FFFF,      ; PixelColor (#FF00FFFF) teal
        "p5",         ; scanAreaInput (bottom-middle portion of screen)
        "mouseover",  ; click_type
        "south_kraken",  ; offset (random offset up)
        0,0,0,0,       ; x1,y1,x2,y2
        5              ; shade_variance
    )
    if (!foundNorthKraken && !foundSouthKraken)
    {
        ShowSequentialTooltip("[Kraken] Could not find kraken (Teal pixel).")
        sleep_random(1000, 1200)
        return false
    }

    sleep_random(50, 75)
    Click("right")
    ShowSequentialTooltip("[Kraken] Found kraken! Right-clicked.")
    return true
}

tryConfirmClickKraken() {
    ; try clicking on image of chop_tentacle, if failure move mouse up and to the right to clear the right click
    ShowSequentialTooltip("[Kraken] Searching for confirmation image...")
    foundInteractKrakenOption := ImageSearchAndClick(
        images.chop_tentacle, ; For example, images.chop_tentacle
        "v2",                  ; scanAreaInput
        "mouseover",           ; click_type
        "option_short",        ; offset
        0,0,0,0,
        5                       ; shade_variance
    )
}

checkIfRoundIsOver() {
    global images

    foundRoundOver := ImageSearchAndClick(
        images.you_sail_back_to_port_khazard, 
        "v2", 
        "mouseover", 
        "no offset",
        0,0,0,0, 
        5
    )
    if (!foundRoundOver)
    {
        return true
    }
    return false
}

; --------------------------------------------------------------------------
;  Wait for Kraken side (north or south) by re-calling findKrakenSide() up to 30 times
; --------------------------------------------------------------------------
waitForKrakenSide(maxAttempts := 120) {
    side := ""
    attempt := 1
    while (attempt <= maxAttempts) {
        side := findKrakenSide()
        if (side) {
            return side
        }
        ShowSequentialTooltip("[Kraken] Kraken not found. Attempt " attempt "/" maxAttempts)
        Sleep 500  ; Wait half a second
        attempt++
    }
    return "" ; gave up
}

krakenBattleSequence() {
    ShowSequentialTooltip("[Kraken] Starting battle sequence...")

    side := waitForKrakenSide(120)
    if (!side) {
        ShowSequentialTooltip("[Kraken] Could not find a North or South Kraken after waiting. Exiting battle sequence.")
        return
    }

    ; Move to the correct tile based on side
    moveToKrakenSide(side)
    sleep_random(2000, 3000)

    ; Spam right-click on the tentacle for ~7 seconds
    spamRightClickTentacle(side, 7000)

    ShowSequentialTooltip("[Kraken] First tentacle spam done. Waiting 2 seconds...")
    sleep_random(2000, 3000)

    ; Optionally move to the opposite tile and spam again
    opposite := (side = "north") ? "south" : "north"
    moveToKrakenSide(opposite)
    sleep_random(2000, 3000)
    spamRightClickTentacle(opposite, 7000)

    ShowSequentialTooltip("[Kraken] Completed both sides of tentacle chopping routine.")
}

findKrakenSide() {
    ShowSequentialTooltip("[Kraken] Checking if Kraken is north or south...")

    ; Try north area (p1 or p2)
    foundNorth := PixelSearchAndClick(
        0x00FFFF,   ; teal
        "p1",       ; top-middle
        "mouseover",
        "tile",     ; offset
        0, 0, 0, 0,
        5
    )
    if (foundNorth) {
        ShowSequentialTooltip("[Kraken] Found Kraken in north portion.")
        return "north"
    }

    foundNorth2 := PixelSearchAndClick(
        0x00FFFF,   ; teal
        "p2",       ; top-right
        "mouseover",
        "tile",
        0, 0, 0, 0,
        5
    )
    if (foundNorth2) {
        ShowSequentialTooltip("[Kraken] Found Kraken in north portion (p3).")
        return "north"
    }

    ; Try south area (p4 & p5)
    foundSouth := PixelSearchAndClick(
        0x00FFFF,   ; teal
        "p4",       ; bottom-middle
        "mouseover",
        "tile",
        0, 0, 0, 0,
        5
    )
    if (foundSouth) {
        ShowSequentialTooltip("[Kraken] Found Kraken in south portion.")
        return "south"
    }

    foundSouth2 := PixelSearchAndClick(
        0x00FFFF,   ; teal
        "p5",       ; bottom-right
        "mouseover",
        "tile",
        0, 0, 0, 0,
        5
    )
    if (foundSouth2) {
        ShowSequentialTooltip("[Kraken] Found Kraken in south portion (p6).")
        return "south"
    }

    ShowSequentialTooltip("[Kraken] Could not detect teal Kraken in north or south areas.")
    return ""
}


moveToKrakenSide(side) {
    if (side = "north") {
        ShowSequentialTooltip("[Kraken] Moving to the red tile for north side.")
        PixelSearchAndClick(
            0xFF0000,    ; red tile color
            0,           ; full screen
            "left",
            "tile_se_reduced",
            0, 0, A_ScreenWidth, A_ScreenHeight,
            5
        )
    } else {
        ShowSequentialTooltip("[Kraken] Moving to the yellow tile for south side.")
        PixelSearchAndClick(
            0xFFFF00,    ; yellow tile color
            0,
            "left",
            "tile_se_reduced",
            0, 0, A_ScreenWidth, A_ScreenHeight,
            5
        )
    }
}

spamRightClickTentacle(side, totalDuration := 7000) {
    ShowSequentialTooltip("[Kraken] Starting spamRightClickTentacle for " totalDuration " ms...")

    startTime := A_TickCount
    loop
    {
        elapsed := A_TickCount - startTime
        if (elapsed > totalDuration) {
            ShowSequentialTooltip("[Kraken] Finished tentacle spam after " totalDuration " ms.")
            break
        }

        ; Let's define a rough location offset from your current tile
        MouseGetPos(&mx, &my)
        offsetX := mx - 50  ; up/left
        offsetY := my - 50

        ; Right-click attempt
        ShowSequentialTooltip("[Kraken] Trying to right-click tentacle at (" offsetX "," offsetY ")")
        Click("right", offsetX, offsetY)
        sleep_random(300, 500)

        ; Check if we have 'Chop Kraken Tentacle' in the menu
        foundChop := lookForChopTentacleOption()
        if (!foundChop) {
            ShowSequentialTooltip("[Kraken] 'Chop Kraken Tentacle' NOT found. Moving mouse away to close menu.")
            ; Move mouse up & right randomly 100-300 px to dismiss
            newX := offsetX + Random(100, 300)
            newY := offsetY - Random(100, 300)
            MouseMove(newX, newY, 20)
            sleep_random(400, 700)
        } else {
            ShowSequentialTooltip("[Kraken] Found 'Chop Kraken Tentacle' in menu! Waiting 1s and continuing spam.")
            sleep_random(1000, 1000)
        }
    }
    ShowSequentialTooltip("[Kraken] Exiting spam loop for tentacle.")
}

lookForChopTentacleOption() {
    global images
    ShowSequentialTooltip("[Kraken] Checking for 'Chop Kraken Tentacle' in menu...")

    foundChop := ImageSearchAndClick(
        images.chop_tentacle,
        0,          ; full screen
        "mouseover",
        "option_short",
        0,0, A_ScreenWidth, A_ScreenHeight,
        5
    )
    return foundChop
}

plugLeaks()
{
    
}


^`::
{
    while(checkIfRoundIsOver())
        {
            ShowSequentialTooltip("[Battle] Engaging Kraken battle sequence...")
            krakenBattleSequence()        
        }
}

^F1::
{
    runIteration := 0

    while (runIteration <= 5000)
    {
        setup_out()
        zoom("in", "6")
        ; if we have finished our first run we need to check the fishing trawler net
        if (runIteration > 0)
        {
            clickFishingTrawlerNet()
        }
        clickGangPlank()
        
        waitForLoadingScreen()

        clickPinkTile()

        while(checkIfRoundIsOver())
        {
            ShowSequentialTooltip("[MiniGame] Starting to plug leaks...")
            plugLeaks()
        }

        ToolTip "Round " . ++runIteration . " complete.", X_TOOLTIP.9, Y_TOOLTIP.9, 9
        sleep_random(1500, 2500)
    }
}

+`::Reload()
