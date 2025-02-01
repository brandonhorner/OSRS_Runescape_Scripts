; ***********************************************
; Fishing Trawler – Utilities File (AutoHotkey v2)
; ***********************************************

global XTOOLTIP := 600
global YTOOLTIP := 550

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")

SetWorkingDir "C:\Git\OSRS_Runescape_Scripts"

; ----------------------------
; Images used in Fishing Trawler
; ----------------------------
global images := {
    inspect_trawler_net:      A_WorkingDir "\image_library\fishing_trawler\inspect_trawler_net.png",
    bank_all_trawler_net:     A_WorkingDir "\image_library\fishing_trawler\bank_all_trawler_net.png",
    cross_gangplank:          A_WorkingDir "\image_library\fishing_trawler\cross_gangplank.png",
    you_sail_out_to_see_text: A_WorkingDir "\image_library\fishing_trawler\you_sail_out_to_see_text.png",
    climb_ship_ladder:        A_WorkingDir "\image_library\fishing_trawler\climb_ship_ladder.png",
    you_sail_back_to_port_khazard: A_WorkingDir "\image_library\fishing_trawler\you_sail_back_to_port_khazard.png",
    no_loot_trawler_net:      A_WorkingDir "\image_library\fishing_trawler\no_loot_trawler_net.png",
    bailing_bucket:           A_WorkingDir "\image_library\fishing_trawler\bailing_bucket.png",
    bailing_bucket_empty:     A_WorkingDir "\image_library\fishing_trawler\bailing_bucket_empty.png",
    xp_minimap_button:        A_WorkingDir "\image_library\xp_minimap_button.png"
}

; ----------------------------
; Tooltip Coordinates (for logging)
; ----------------------------
global X_TOOLTIP := {
    1: 0,
    2: 0,
    3: 0,
    4: 980,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0
}

global Y_TOOLTIP := {
    1: 100,
    2: 125,
    3: 150,
    4: 205,
    5: 205,
    6: 230,
    7: 285,
    8: 325,
    9: 375
}

; ----------------------------
; Utility Functions
; ----------------------------

SleepRandom(sleepTimeLow, sleepTimeHigh) {
    sleepTime := Random(sleepTimeLow, sleepTimeHigh)
    Sleep sleepTime
    return sleepTime
}

SetRandomDelays(mouseDelayLow := 20, mouseDelayHigh := 23, keyDelayLow := 30, keyDelayHigh := 50, pressDurationLow := 20, pressDurationHigh := 30) {
    delaySpeed := Random(mouseDelayLow, mouseDelayHigh)
    SetMouseDelay(delaySpeed)
    
    keyDelaySpeed := Random(keyDelayLow, keyDelayHigh)
    pressDuration := Random(pressDurationLow, pressDurationHigh)
    SetKeyDelay(keyDelaySpeed, pressDuration)
}

MoveMouseCenter() {
    offsetX := Random(-300, 300)
    offsetY := Random(-300, 300)
    newXPos := A_ScreenWidth / 2 + offsetX
    newYPos := A_ScreenHeight / 2 + offsetY
    MouseMove(newXPos, newYPos)
}

Zoom(zoomDirection, zoomLevel := 30) {
    MoveMouseCenter()
    if (zoomDirection = "out") {
        Loop zoomLevel {
            Send("{Wheeldown}")
            SleepRandom(45, 65)
        }
    } else {
        Loop zoomLevel {
            Send("{Wheelup}")
            SleepRandom(35, 55)
        }
    }
}

ClickCompass() {
    shadeVariation := 50
    options := "*" shadeVariation " " images.xp_minimap_button
    if ImageSearch(&foundX, &foundY, 0, 0, A_ScreenWidth, A_ScreenHeight, options) {
        xOffset := Random(30, 60)
        yOffset := Random(-23, 0)
        xOffset += foundX
        yOffset += foundY
        Click("left", xOffset, yOffset)
        return true
    } else {
        ToolTip("Could not find the compass button.", 100, 500, 20)
        return false
    }
}

SetupOut() {
    if WinActive(runelite_window) {
        Zoom("out")
        ClickCompass()
        Send("{up down}")
        SleepRandom(1300, 2200)
        Send("{up up}")
        return
    }
}

SendKey(key, presses := 1) {
    ToolTip "Key: " key "`nPresses: " presses " time(s)", X_TOOLTIP.3, Y_TOOLTIP.3, 3
    SetRandomDelays(45, 85)
    if (presses <= 1) {
        Send("{" key "}")
        return
    }
    if (presses > 1) {
        Send("{" key "}")
        SendKey(key, presses - 1)
        return
    }
}

; ----------------------------
; Image & Pixel Searching Functions
; ----------------------------

PixelSearchAndClick(PixelColor, scanAreaInput := 0, clickType := 0, offset := 0, x1 := 0, y1 := 0, x2 := 0, y2 := 0, shadeVariance := 0) {
    menuWidth := 140
    if scanAreaInput != 0 {
        scanArea := GetScanArea(scanAreaInput)
    } else {
        scanArea := { x1: x1, y1: y1, x2: x2, y2: y2 }
    }
    if WinActive(runelite_window) {
        SetRandomDelays()
        if PixelSearch(&foundX, &foundY, scanArea.x1, scanArea.y1, scanArea.x2, scanArea.y2, PixelColor, shadeVariance) {
            offsetObj := GetOffset(offset)
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            ClickOffset(clickType, offsetX, offsetY)
            return true
        }
    }
    return false
}

ImageSearchAndClick(ImageURL, scanAreaInput := 0, clickType := 0, offset := 0, x1 := 0, y1 := 0, x2 := 0, y2 := 0, shadeVariance := 50) {
    menuWidth := 140
    if scanAreaInput != 0 {
        scanArea := GetScanArea(scanAreaInput)
    } else {
        scanArea := { x1: x1, y1: y1, x2: x2, y2: y2 }
    }
    SplitPath ImageURL, &ImageName
    if WinActive(runelite_window) {
        SetRandomDelays()
        if (ImageSearch(&foundX, &foundY, scanArea.x1, scanArea.y1, scanArea.x2, scanArea.y2, "*" shadeVariance " *TransBlack " ImageURL)
         or ImageSearch(&foundX, &foundY, scanArea.x1, scanArea.y1, scanArea.x2, scanArea.y2, "*" shadeVariance " " ImageURL)) {
            ToolTip "8. ImageSearchAndClick: Found " ImageName, X_TOOLTIP.8, Y_TOOLTIP.8, 8
            offsetObj := GetOffset(offset)
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            ClickOffset(clickType, offsetX, offsetY)
            return true
        }
    }
    return false
}

GetScanArea(scanArea := 0) {
    menuWidth := 0
    gameWindowWidth := A_ScreenWidth - 20
    switch scanArea {
        case "top_left":
            scanAreaObj := { x1: 0, y1: 22, x2: 190, y2: 75 }
        case "bag":
            scanAreaObj := { x1: 1645, y1: 700, x2: 1855, y2: 1000 }
        case "chat_all":
            scanAreaObj := { x1: 3, y1: 872, x2: 494, y2: 986 }
        case "chat_bottom":
            scanAreaObj := { x1: 3, y1: 969, x2: 494, y2: 986 }
        case "chat_bottom_2":
            scanAreaObj := { x1: 3, y1: 958, x2: 510, y2: 1015 }
        case "middle":
            scanAreaObj := { x1: 0, y1: 200, x2: 1650, y2: 970 }
        case "center":
            scanAreaObj := { x1: A_ScreenWidth / 4, y1: A_ScreenHeight / 4, x2: A_ScreenWidth * 3 / 4, y2: A_ScreenHeight * 3 / 4 }
        case "bank":
            scanAreaObj := { x1: 575, y1: 50, x2: 1060, y2: 850 }
        case "under_mouse":
            MouseGetPos(&x, &y)
            scanAreaObj := { x1: x - 130, y1: y - 10, x2: x + 120, y2: y + 255 }
        case "p1":
            scanAreaObj := { x1: 0, y1: 20, x2: A_ScreenWidth / 3, y2: A_ScreenHeight / 2 }
        case "p2":
            scanAreaObj := { x1: A_ScreenWidth / 3, y1: 20, x2: A_ScreenWidth * 2 / 3, y2: A_ScreenHeight / 2 }
        case "p3":
            scanAreaObj := { x1: A_ScreenWidth * 2 / 3, y1: 20, x2: A_ScreenWidth - 20, y2: A_ScreenHeight / 2 }
        case "p4":
            scanAreaObj := { x1: 0, y1: A_ScreenHeight / 2, x2: A_ScreenWidth / 3, y2: A_ScreenHeight - 50 }
        case "p5":
            scanAreaObj := { x1: A_ScreenWidth / 3, y1: A_ScreenHeight / 2, x2: A_ScreenWidth * 2 / 3, y2: A_ScreenHeight - 50 }
        case "p6":
            scanAreaObj := { x1: A_ScreenWidth * 2 / 3, y1: A_ScreenHeight / 2, x2: A_ScreenWidth - 20, y2: A_ScreenHeight - 50 }
        default:
            scanAreaObj := { x1: 0, y1: 20, x2: A_ScreenWidth - 20, y2: A_ScreenHeight - 50 }
    }
    if MenuIsOpen() {
        scanAreaObj.x1 -= menuWidth
        scanAreaObj.x2 -= menuWidth
    }
    return scanAreaObj
}

MenuIsOpen() {
    return false
}

GetOffset(offsetItem) {
    switch offsetItem {
        case "option":
            horizontal := Random(0, 200)
            vertical := Random(1, 10)
        case "option_short":
            horizontal := Random(1, 100)
            vertical := Random(1, 5)
        case "item":
            horizontal := Random(5, 15)
            vertical := Random(5, 15)
        case "tile":
            horizontal := Random(-50, 50)
            vertical := Random(-50, 50)
        case "tile_sw":
            horizontal := Random(-50, 0)
            vertical := Random(0, 50)
        case "tile_se":
            horizontal := Random(20, 100)
            vertical := Random(20, 100)
        case "tile_se_reduced":
            horizontal := Random(15, 40)
            vertical := Random(15, 40)
        case "tile_south":
            horizontal := Random(0, 5)
            vertical := Random(10, 30)
        case "south":
            horizontal := 0
            vertical := Random(10, 30)
        case "southish":
            horizontal := Random(-15, 15)
            vertical := Random(20, 80)
        case "minimap_icon":
            horizontal := Random(0, 5)
            vertical := Random(0, 5)
        case "trawler_net":
            horizontal := Random(50, 100)
            vertical := Random(50, 100)
        case "gangplank":
            horizontal := Random(5, 40)
            vertical := Random(5, 10)
        case "ladder":
            horizontal := Random(10, 20)
            vertical := Random(15, 40)
        case "boat_pink_tile":
            horizontal := Random(-10, 10)
            vertical := Random(15, 30)
        case "north_kraken":
            horizontal := Random(3, 10)
            vertical := Random(50, 100)
        case "south_kraken":
            horizontal := Random(3, 8)
            vertical := Random(10, 15)
        case "bailing_bucket":
            horizontal := Random(1, 4)
            vertical := Random(1, 4)
        default:
            horizontal := 0
            vertical := 0
    }
    offset := { x: horizontal, y: vertical }
    return offset
}

ClickOffset(clickType, offsetX := 0, offsetY := 0) {
    switch clickType {
        case "right":
            Click("right", offsetX, offsetY)
        case "left":
            Click(offsetX, offsetY)
        case "mouseover":
            Click(offsetX, offsetY, 0)
        case "doubleclick":
            Click(offsetX, offsetY, 2)
        case "in_place":
            Click()
    }
}
