#Requires AutoHotkey v2.0
#SingleInstance Force
#Include utilities.ahk

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
            ; Move the mouse up and to the right first
            MouseGetPos(&mx, &my)
            newX := mx + Random(100, 300)
            newY := my - Random(100, 300)
            MouseMove(newX, newY, 20)
            sleep_random(300, 700)
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
        5              ; shade_varianced
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
        sleep_random(400, 700)
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
        ,                       ; scanAreaInput
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
            ; Move the mouse up and to the right first
            MouseGetPos(&mx, &my)
            newX := mx + Random(100, 300)
            newY := my - Random(100, 300)
            MouseMove(newX, newY, 20)
            sleep_random(100, 200)
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
    ; Move the mouse up and to the right first
    MouseGetPos(&mx, &my)
    newX := mx + Random(100, 300)
    newY := my - Random(100, 300)
    MouseMove(newX, newY, 20)
    sleep_random(100, 200)

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
        if (!tryLeftClickPinkTile()) {
            failedToClickPinkTile++
            continue
        }
        interactedSuccessfully := true
    }
}

tryLeftClickPinkTile() {
    ShowSequentialTooltip("[PinkTile] Searching for Pink Tile pixel...")

    foundPinkTile := PixelSearchAndClick(
        0xFF00FF,      ; PixelColor (#FFFF00FF) pink
        ,             ; omit for custom scan area
        "mouseover",  ; click_type
        "boat_pink_tile",    ; offset (random offset down/right)
        0, 0, A_ScreenWidth ,A_ScreenHeight, ; x1,y1,x2,y2
        5              ; shade_variance
    )
    if (!foundPinkTile)
    {
        ShowSequentialTooltip("[PinkTile] Could not find pink tile pixel in scan area: " A_ScreenWidth "x" A_ScreenHeight)
        sleep_random(500, 700)
        return false
    }
    sleep_random(100, 300)
    Click()
    ShowSequentialTooltip("[PinkTile] Found pink tile pixel! Left-clicked.")
    return true
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


plugLeaks() {
    ShowSequentialTooltip("[Leaks] Checking columns for teal...")

    ; We have 3 columns. For each column:
    ; 1) detection area = we look for teal (#00FFFF)
    ; 2) click area     = we actually click to fix the leak
    columns := [
        {
            name:    "Column 1",
            detect:  { x1: 921, y1: 669, x2: 1045, y2: 787 },   ; detection area
            click:   { x1: 853, y1: 844, x2: 1102, y2: 1144 }   ; actual click area
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

    leakColor := 0x00FFFF  ; teal
    shadeVariance := 10    ; adjust if needed
    foundAny := false

    for _, col in columns {
        ShowSequentialTooltip("[Leaks] Searching " col.name " detection area for teal pixel...")

        if WinActive(runelite_window)
        {
            ; Use AHK v2's built-in PixelSearch. Returns true if successful
            success := PixelSearch(
                &foundX, &foundY,
                col.detect.x1, col.detect.y1,
                col.detect.x2, col.detect.y2,
                leakColor,
                shadeVariance
            )
            if (success) {
                ShowSequentialTooltip("[Leaks] Found leak in " col.name "! Clicking in lower area to fix...")

                ; Randomly pick a point within the click area
                clickX := Random(col.click.x1 + 20, col.click.x2 - 20)
                clickY := Random(col.click.y1 + 20, col.click.y2 - 20)

                ; Move+click. If you prefer a 'mouseover' plus 'right-click', adapt as needed.
                MouseMove(clickX, clickY, 2)  ; move speed ~15
                sleep_random(100, 200)
                Click()
                sleep_random(1200, 1300)
                foundAny := true

                ; If you only need to fix one column per pass, break here
                return true
            }
        }
    }

    if (!foundAny) {
        ShowSequentialTooltip("[Leaks] No teal pixels found in any column.")
        sleep_random(100, 250)
        return false
    }
}
; if the pink tile is to my left, right, or south, I need to move the mouse to the pink tile and left click it
correctToPinkTile() { ; TODO FIX THIS
    global images

    ShowSequentialTooltip("[PinkTile] Searching for Pink Tile pixel...")

    ; Search the left side of the character
    foundPinkTile := PixelSearchAndClick(
        0xFF00FF,      ; PixelColor (#FFFF00FF) pink
        ,             ; omit for custom scan area
        "mouseover",  ; click_type
        "tile_se",    ; offset (random offset down/right)
        921, 669, 1045, 787, ; x1, y1, x2, y2 for the left side
        5              ; shade_variance
    )
    if (foundPinkTile) {
        sleep_random(400, 700)
        Click()
        ShowSequentialTooltip("[PinkTile] Found pink tile pixel on the left side! Left-clicked.")
        return true
    }

    ; Search the right side of the character
    foundPinkTile := PixelSearchAndClick(
        0xFF00FF,      ; PixelColor (#FFFF00FF) pink
        ,             ; omit for custom scan area
        "mouseover",  ; click_type
        "tile_sw",    ; offset (random offset down/right)
        1471, 689, 1610, 782, ; x1, y1, x2, y2 for the right side
        5              ; shade_variance
    )
    if (foundPinkTile) {
        sleep_random(400, 700)
        Click()
        ShowSequentialTooltip("[PinkTile] Found pink tile pixel on the right side! Left-clicked.")
        return true
    }

    ; Search the south side of the character
    foundPinkTile := PixelSearchAndClick(
        0xFF00FF,      ; PixelColor (#FFFF00FF) pink
        ,             ; omit for custom scan area
        "mouseover",  ; click_type
        "tile_south",    ; offset (random offset down/right)
        1122, 1016, 1406, 1125, ; x1, y1, x2, y2 for the south side
        5              ; shade_variance
    )
    if (foundPinkTile) {
        sleep_random(400, 700)
        Click()
        ShowSequentialTooltip("[PinkTile] Found pink tile pixel on the south side! Left-clicked.")
        return true
    }

    ShowSequentialTooltip("[PinkTile] Could not find pink tile pixel in specified scan areas.")
    
    sleep_random(500, 700)
    return false
}

; click on bailing_bucket.png in the inventory
; bailing_bucket offset
clickBucket()
{
    global images

    ShowSequentialTooltip("[Bucket] Searching for bailing bucket in inventory...")

    ; Search for bailing bucket
    foundBucket := ImageSearchAndClick(
        images.bailing_bucket,  ; For example, images.bailing_bucket
        "0",                    ; scanAreaInput
        "mouseover",            ; click_type
        "bailing_bucket",       ; offset
        0, 0, A_ScreenWidth, A_ScreenHeight,
        5                       ; shade_variance
    )
    
    ; If bailing bucket is not found, search for bailing bucket empty
    if (!foundBucket)
    {
        foundBucket := ImageSearchAndClick(
            images.bailing_bucket_empty, ; For example, images.bailing_bucket_empty
            "0",                   ; scanAreaInput
            "mouseover",           ; click_type
            "bailing_bucket",      ; offset
            0, 0, A_ScreenWidth, A_ScreenHeight,
            5                      ; shade_variance
        )
    }

    if (!foundBucket)
    {
        ShowSequentialTooltip("[Bucket] Bailing bucket not found.")
        return false
    }
    sleep_random(100, 200)
    Click()
    ShowSequentialTooltip("[Bucket] Bailing bucket found! Clicked.")
    return true
}
 

^`::
{
     ; Used for testing
}

^F1::
{
    ; Ask user if they want to start by looting the trawler net
    response := MsgBox("Do you want to start by looting the trawler net?", "Trawler Setup", "YesNo")
    
    ; Set runIteration based on user choice
    if (response = "Yes")
    {
        runIteration := 1
        skipToBoat := false
    }
    else
    {   
        runIteration := 0
        ;Ask user if they want to skip to the boat
        response2 := MsgBox("Do you want to skip to the boat?", "Trawler Setup", "YesNo")
        if (response2 = "Yes")
            skipToBoat := true
        else
            skipToBoat := false
    }

    ; set the number of runs here
    while (runIteration <= 20)
    {
        if (!skipToBoat)
        {
            setup_out()
            zoom("in", "6")
            sleep_random(300, 500)
            clickPinkTile()
            sleep_random(1500,2000)
            ; if we have finished our first run we need to check the fishing trawler net
            if (runIteration > 0)
            {
                clickFishingTrawlerNet()
            }
            clickGangPlank()
            waitForLoadingScreen()
        }
        
        clickPinkTile()
        zoom("in", "12")
        correctToPinkTile()

        leaksPlugged := 0
        failedToPlugLeaks := 0
        while(leaksPlugged <= 14)
        {
            ShowSequentialTooltip("[MiniGame] Starting to plug leaks...")
            if(plugLeaks())
            {
                ShowSequentialTooltip("[MiniGame] Plugged a leak!")
                leaksPlugged++
            }
            else
            {
                ShowSequentialTooltip("[MiniGame] No leaks found...")
                failedToPlugLeaks++
                if(failedToPlugLeaks = 20)
                {
                    ShowSequentialTooltip("[MiniGame] Failed to plug leaks 50 times. Clicking Pink Tile...")
                    clickPinkTile()
                }
            }
        }
        SendKey("B")
        while(checkIfRoundIsOver())
        {
            ToolTip(" Waiting for round to be over...", X_TOOLTIP.8, Y_TOOLTIP.8, 8)
            ; click bucket in inventory
            clickBucket()
            sleep_random(200, 1000)
        }
        ToolTip("Round " . runIteration++ . " complete.", X_TOOLTIP.9, Y_TOOLTIP.9, 9)
        sleep_random(12000, 13000)
        skipToBoat := false
    }
}

+`::Reload()
