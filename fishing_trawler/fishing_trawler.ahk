#Requires AutoHotkey v2.0
#SingleInstance Force
#Include utilities.ahk

SetWorkingDir "C:\Git\OSRS_Runescape_Scripts\fishing_trawler"

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"

; ==========================
; Enhanced Sequential Tooltip System
; ==========================
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
    if (tooltipHistory.Length > 10)
        tooltipHistory.RemoveAt(1)

    ; Build a multiline text block showing recent messages
    displayText := ""
    for idx, item in tooltipHistory {
        displayText .= item "`n"
    }

    ; Show them in a single tooltip
    ToolTip(displayText, X_TOOLTIP.9, Y_TOOLTIP.9, 9)
}

ClickFishingTrawlerNet() {
    global images

    interactedSuccessfully := false
    failedToClickTrawlerNet := 0
    maxAttempts := 100

    while (!interactedSuccessfully && failedToClickTrawlerNet < maxAttempts) {
        if (!TryRightClickTrawlerNet()) {
            failedToClickTrawlerNet++
            continue
        }
        if (!TryConfirmTrawlerNet()) {
            failedToClickTrawlerNet++
            ; Move the mouse up and to the right first
            MouseGetPos(&mx, &my)
            newX := mx + Random(100, 300)
            newY := my - Random(100, 300)
            MouseMove(newX, newY, 20)
            SleepRandom(300, 700)
            continue
        }
        if (!WaitForBankAllButton()) {
            failedToClickTrawlerNet++
            continue
        }

        interactedSuccessfully := true
    }
}

TryRightClickTrawlerNet() {
    ShowSequentialTooltip("[TrawlerNet] Searching for Trawler Net pixel...")

    foundTrawlerNet := PixelSearchAndClick(0xFF0000, "p2", "mouseover", "trawler_net", 0, 0, 0, 0, 5)
    if (!foundTrawlerNet) {
        ShowSequentialTooltip("[TrawlerNet] Could not find red pixel.")
        SleepRandom(500, 700)
        return false
    }
    SleepRandom(400, 700)
    Click("right")
    ShowSequentialTooltip("[TrawlerNet] Found net pixel! Right-clicked.")
    return true
}

TryConfirmTrawlerNet() {
    ShowSequentialTooltip("[TrawlerNet] Searching for confirmation image...")

    foundInteractTrawlerNetOption := ImageSearchAndClick(images.inspect_trawler_net, "p2", "mouseover", "option_short", 0, 0, 0, 0, 5)
    if (!foundInteractTrawlerNetOption) {
        ShowSequentialTooltip("[TrawlerNet] Confirmation NOT found.")
        SleepRandom(500, 700)
        return false
    }
    ShowSequentialTooltip("[TrawlerNet] Confirmation found! Looted successfully.")
    SleepRandom(400, 700)
    Click()
    SleepRandom(4500, 5700)
    return true
}

WaitForBankAllButton() {
    maxAttempts := 20 
    ShowSequentialTooltip("[TrawlerNet] Waiting for 'Bank all' button to appear...")
    while (!TryClickBankAll() && !TrawlerLootMessageExists() && maxAttempts > 0) {
        SleepRandom(400, 700)
        maxAttempts--
    }
    if (maxAttempts == 0) {
        ShowSequentialTooltip("[TrawlerNet] 'Bank all' button not found.")
        return false
    }
    return true
}

TryClickBankAll() {
    ShowSequentialTooltip("[TrawlerNet] Searching for 'Bank all' button...")
    foundBankAllButton := ImageSearchAndClick(images.bank_all_trawler_net, "", "mouseover", "item", 0, 0, A_ScreenWidth, A_ScreenHeight, 5)
    if (!foundBankAllButton) {
        ShowSequentialTooltip("[TrawlerNet] Bank all not found.")
        return false
    }
    SleepRandom(100, 200)
    Click()
    ShowSequentialTooltip("[TrawlerNet] Bank all found! Banked successfully.")
    return true
}

TrawlerLootMessageExists() {
    global images
    ShowSequentialTooltip("[TrawlerNet] Searching for message in chatbox stating that we don't have trawler loot...")
    foundTrawlerLootMessage := ImageSearchAndClick(images.no_loot_trawler_net, "v2", "mouseover", "no offset", 0, 0, 0, 0, 5)
    if (foundTrawlerLootMessage) {
        ShowSequentialTooltip("[TrawlerNet] Message found-- No loot in net.")
        return true
    }
    return false
}

ClickGangPlank() {
    global images

    interactedSuccessfully := false
    failedToClickGangPlank := 0
    maxAttempts := 10

    while (!interactedSuccessfully && failedToClickGangPlank < maxAttempts) {
        if (!TryRightClickGangPlank()) {
            failedToClickGangPlank++
            continue
        }
        if (!TryConfirmGangPlank()) {
            failedToClickGangPlank++
            MouseGetPos(&mx, &my)
            newX := mx + Random(100, 300)
            newY := my - Random(100, 300)
            MouseMove(newX, newY, 20)
            SleepRandom(100, 200)
            continue
        }
        interactedSuccessfully := true
    }
}

TryRightClickGangPlank() {
    ShowSequentialTooltip("[GangPlank] Searching for Gang Plank pixel...")  
    foundGangPlank := PixelSearchAndClick(0x00FFFF, "p3", "mouseover", "gangplank", 0, 0, 0, 0, 5)
    if (!foundGangPlank) {
        ShowSequentialTooltip("[GangPlank] Could not find gang plank pixel.")
        SleepRandom(500, 700)
        return false
    }
    SleepRandom(400, 700)
    Click("right")
    ShowSequentialTooltip("[GangPlank] Found gang plank pixel! Right-clicked.")
    return true
}

TryConfirmGangPlank() {
    ShowSequentialTooltip("[GangPlank] Searching for confirmation image...")
    foundInteractGangPlankOption := ImageSearchAndClick(images.cross_gangplank, "p3", "mouseover", "option_short", 0, 0, 0, 0, 5)
    if (!foundInteractGangPlankOption) {
        ShowSequentialTooltip("[GangPlank] Confirmation NOT found.")
        SleepRandom(500, 700)
        return false
    }
    ShowSequentialTooltip("[GangPlank] Confirmation found! Crossing.")
    SleepRandom(400, 700)
    Click()
    SleepRandom(7000, 10000)
    return true
}

WaitForLoadingScreen() {
    global images
    attempts := 0
    while (attempts < 300) {
        ShowSequentialTooltip("[Waiting] Waiting for Fishing Trawler loading screen... Attempt #" attempts)
        foundSailingText := ImageSearchAndClick(images.you_sail_out_to_see_text, "v2", "mouseover", "no offset", 0, 0, 0, 0, 5)
        if (foundSailingText) {
            ShowSequentialTooltip("[Waiting] Found Fishing Trawler loading screen! Round starting in 12s.")
            SleepRandom(12000, 12000)
            break
        }
        attempts++
        SleepRandom(1000, 2000)
    }
}

ClickLadder() {
    global images

    interactedSuccessfully := false
    failedToClickLadder := 0
    maxAttempts := 20

    while (!interactedSuccessfully && failedToClickLadder < maxAttempts) {
        if (!TryRightClickLadder()) {
            failedToClickLadder++
            continue
        }
        if (!TryConfirmClimbLadder()) {
            failedToClickLadder++
            continue
        }
        interactedSuccessfully := true
    }
}

TryRightClickLadder() {
    MouseGetPos(&mx, &my)
    newX := mx + Random(100, 300)
    newY := my - Random(100, 300)
    MouseMove(newX, newY, 20)
    SleepRandom(100, 200)
    ShowSequentialTooltip("[Ladder] Searching for Ladder pixel...")
    foundLadder := PixelSearchAndClick(0xFF00FF, "h1", "mouseover", "ladder", 0, 0, 0, 0, 5)
    if (!foundLadder) {
        ShowSequentialTooltip("[Ladder] Could not find ladder pixel.")
        SleepRandom(500, 700)
        return false
    }
    SleepRandom(400, 700)
    Click("right")
    ShowSequentialTooltip("[Ladder] Found ladder pixel! Right-clicked.")
    return true
}

TryConfirmClimbLadder() {
    ShowSequentialTooltip("[Ladder] Searching for confirmation image...")
    foundInteractLadderOption := ImageSearchAndClick(images.climb_ship_ladder, "h1", "mouseover", "option_short", 0, 0, 0, 0, 5)
    if (!foundInteractLadderOption) {
        ShowSequentialTooltip("[Ladder] Confirmation NOT found.")
        SleepRandom(500, 700)
        return false
    }
    ShowSequentialTooltip("[Ladder] Confirmation found! Climbing.")
    SleepRandom(400, 700)
    Click()
    SleepRandom(2000, 3000)
    return true
}

ClickPinkTile() {
    global images

    interactedSuccessfully := false
    failedToClickPinkTile := 0
    maxAttempts := 20

    while (!interactedSuccessfully && failedToClickPinkTile < maxAttempts) {
        if (!TryLeftClickPinkTile()) {
            failedToClickPinkTile++
            continue
        }
        interactedSuccessfully := true
    }
}

TryLeftClickPinkTile() {
    ShowSequentialTooltip("[PinkTile] Searching for Pink Tile pixel...")
    foundPinkTile := PixelSearchAndClick(0xFF00FF, "", "mouseover", "boat_pink_tile", 0, 0, A_ScreenWidth, A_ScreenHeight, 5)
    if (!foundPinkTile) {
        ShowSequentialTooltip("[PinkTile] Could not find pink tile pixel in scan area: " A_ScreenWidth "x" A_ScreenHeight)
        SleepRandom(500, 700)
        return false
    }
    SleepRandom(100, 300)
    Click()
    ShowSequentialTooltip("[PinkTile] Found pink tile pixel! Left-clicked.")
    return true
}

CheckIfRoundIsOver() {
    global images
    foundRoundOver := ImageSearchAndClick(images.you_sail_back_to_port_khazard, "v2", "mouseover", "no offset", 0, 0, 0, 0, 5)
    if (!foundRoundOver)
        return true
    return false
}

PlugLeaks() {
    ShowSequentialTooltip("[Leaks] Checking columns for teal...")
    columns := [
        {
            name:    "Column 1",
            detect:  { x1: 921, y1: 669, x2: 1045, y2: 787 },
            click:   { x1: 853, y1: 844, x2: 1102, y2: 1144 }
        },
        {
            name:    "Column 2",
            detect:  { x1: 1198, y1: 705, x2: 1317, y2: 754 },
            click:   { x1: 1127, y1: 850, x2: 1400, y2: 1148 }
        },
        {
            name:    "Column 3",
            detect:  { x1: 1471, y1: 689, x2: 1610, y2: 782 },
            click:   { x1: 1402, y1: 847, x2: 1704, y2: 1155 }
        }
    ]
    leakColor := 0x00FFFF
    shadeVariance := 10
    foundAny := false

    for _, col in columns {
        ShowSequentialTooltip("[Leaks] Searching " col.name " detection area for teal pixel...")
        if WinActive(runelite_window) {
            success := PixelSearch(&foundX, &foundY, col.detect.x1, col.detect.y1, col.detect.x2, col.detect.y2, leakColor, shadeVariance)
            if (success) {
                ShowSequentialTooltip("[Leaks] Found leak in " col.name "! Clicking in lower area to fix...")
                clickX := Random(col.click.x1 + 20, col.click.x2 - 20)
                clickY := Random(col.click.y1 + 20, col.click.y2 - 20)
                MouseMove(clickX, clickY, 2)
                SleepRandom(100, 200)
                Click()
                SleepRandom(1200, 1300)
                foundAny := true
                return true
            }
        }
    }
    if (!foundAny) {
        ShowSequentialTooltip("[Leaks] No teal pixels found in any column.")
        SleepRandom(100, 250)
        return false
    }
}

CorrectToPinkTile() { ; TODO FIX THIS
    global images
    ShowSequentialTooltip("[PinkTile] Searching for Pink Tile pixel...")

    foundPinkTile := PixelSearchAndClick(0xFF00FF, "", "mouseover", "tile_se", 921, 669, 1045, 787, 5)
    if (foundPinkTile) {
        SleepRandom(400, 700)
        Click()
        ShowSequentialTooltip("[PinkTile] Found pink tile pixel on the left side! Left-clicked.")
        return true
    }
    foundPinkTile := PixelSearchAndClick(0xFF00FF, "", "mouseover", "tile_sw", 1471, 689, 1610, 782, 5)
    if (foundPinkTile) {
        SleepRandom(400, 700)
        Click()
        ShowSequentialTooltip("[PinkTile] Found pink tile pixel on the right side! Left-clicked.")
        return true
    }
    foundPinkTile := PixelSearchAndClick(0xFF00FF, "", "mouseover", "tile_south", 1122, 1016, 1406, 1125, 5)
    if (foundPinkTile) {
        SleepRandom(400, 700)
        Click()
        ShowSequentialTooltip("[PinkTile] Found pink tile pixel on the south side! Left-clicked.")
        return true
    }
    ShowSequentialTooltip("[PinkTile] Could not find pink tile pixel in specified scan areas.")
    SleepRandom(500, 700)
    return false
}

ClickBucket() {
    global images
    ShowSequentialTooltip("[Bucket] Searching for bailing bucket in inventory...")

    foundBucket := ImageSearchAndClick(images.bailing_bucket, "", "mouseover", "bailing_bucket", 0, 0, A_ScreenWidth, A_ScreenHeight, 5)
    if (!foundBucket) {
        foundBucket := ImageSearchAndClick(images.bailing_bucket_empty, "", "mouseover", "bailing_bucket", 0, 0, A_ScreenWidth, A_ScreenHeight, 5)
    }
    if (!foundBucket) {
        ShowSequentialTooltip("[Bucket] Bailing bucket not found.")
        return false
    }
    SleepRandom(100, 200)
    Click()
    ShowSequentialTooltip("[Bucket] Bailing bucket found! Clicked.")
    return true
}

^`:: 
{ }  ; Used for testing

^F1:: {
    response := MsgBox("Do you want to start by looting the trawler net?", "Trawler Setup", "YesNo")
    if (response = "Yes") {
        runIteration := 1
        skipToBoat := false
    } else {
        runIteration := 0
        response2 := MsgBox("Do you want to skip to the boat?", "Trawler Setup", "YesNo")
        if (response2 = "Yes")
            skipToBoat := true
        else
            skipToBoat := false
    }

    while (runIteration <= 20) {
        if (!skipToBoat) {
            SetupOut()
            Zoom("in", "6")
            SleepRandom(300, 500)
            ClickPinkTile()
            SleepRandom(1500,2000)
            if (runIteration > 0)
                ClickFishingTrawlerNet()
            ClickGangPlank()
            WaitForLoadingScreen()
        }
        ClickPinkTile()
        Zoom("in", "12")
        CorrectToPinkTile()

        leaksPlugged := 0
        failedToPlugLeaks := 0
        while(leaksPlugged <= 14) {
            ShowSequentialTooltip("[MiniGame] Starting to plug leaks...")
            if(PlugLeaks()) {
                ShowSequentialTooltip("[MiniGame] Plugged a leak!")
                leaksPlugged++
            } else {
                ShowSequentialTooltip("[MiniGame] No leaks found...")
                failedToPlugLeaks++
                if(failedToPlugLeaks = 20) {
                    ShowSequentialTooltip("[MiniGame] Failed to plug leaks 50 times. Clicking Pink Tile...")
                    ClickPinkTile()
                }
            }
        }
        SendKey("B")
        while(CheckIfRoundIsOver()) {
            ToolTip(" Waiting for round to be over...", X_TOOLTIP.8, Y_TOOLTIP.8, 8)
            ClickBucket()
            SleepRandom(200, 1000)
        }
        ToolTip("Round " . runIteration++ . " complete.", X_TOOLTIP.9, Y_TOOLTIP.9, 9)
        SleepRandom(12000, 13000)
        skipToBoat := false
    }
}

+`:: Reload()
