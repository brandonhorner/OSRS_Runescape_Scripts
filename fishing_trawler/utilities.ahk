; ***********************************************
; Fishing Trawler – Utilities File (AutoHotkey v2)
; ***********************************************

global XTOOLTIP := 600
global YTOOLTIP := 550

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")

; Set working directory to the parent folder for all your projects.
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

; Sleep for a random time between sleep_time_low and sleep_time_high (milliseconds)
sleep_random(sleep_time_low, sleep_time_high) {
    sleep_time := Random(sleep_time_low, sleep_time_high)
    Sleep sleep_time
    return sleep_time
}

; Set randomized delays for mouse and key actions.
set_random_delays(mouse_delay_low := 20, mouse_delay_high := 23, key_delay_low := 30, key_delay_high := 50, press_duration_low := 20, press_duration_high := 30) {
    delaySpeed := Random(mouse_delay_low, mouse_delay_high)
    SetMouseDelay(delaySpeed)
    
    key_delay_speed := Random(key_delay_low, key_delay_high)
    press_duration := Random(press_duration_low, press_duration_high)
    SetKeyDelay(key_delay_speed, press_duration)
}

; Move the mouse to roughly the center of the screen with a random offset.
move_mouse_center() {
    offset_x := Random(-300, 300)
    offset_y := Random(-300, 300)
    new_x_pos := A_ScreenWidth / 2 + offset_x
    new_y_pos := A_ScreenHeight / 2 + offset_y
    MouseMove(new_x_pos, new_y_pos)
}

; Zoom the camera in or out by simulating mouse wheel scrolls.
; zoom_direction: "in" or "out"
; zoom_level: number of wheel steps (default is 30)
zoom(zoom_direction, zoom_level := 30) {
    move_mouse_center()
    if (zoom_direction = "out") {
        Loop zoom_level {
            Send("{Wheeldown}")
            sleep_random(45, 65)
        }
    } else {  ; zoom in
        Loop zoom_level {
            Send("{Wheelup}")
            sleep_random(35, 55)
        }
    }
}

; Click the RuneLite compass button.
; (This uses the xp_minimap_button image and offsets the click to a likely “North” location.)
ClickCompass() {
    shade_variation := 50
    options := "*" shade_variation " " images.xp_minimap_button
    if ImageSearch(&foundX, &foundY, 0, 0, A_ScreenWidth, A_ScreenHeight, options) {
        x_offset := Random(30, 60)
        y_offset := Random(-23, 0)
        x_offset += foundX
        y_offset += foundY
        Click("left", x_offset, y_offset)
        return true
    } else {
        ToolTip("Could not find the compass button.", 100, 500, 20)
        return false
    }
}

; A setup routine that “zooms out,” clicks the compass and tilts the camera.
setup_out() {
    if WinActive(runelite_window) {
        zoom("out")
        ClickCompass()
        Send("{up down}")
        sleep_random(1300, 2200)
        Send("{up up}")
        return
    }
}

; Display a tooltip then send a key. (Used for, e.g., sending "B" after plugging leaks.)
SendKey(key, presses := 1) {
    ToolTip "Key: " key "`nPresses: " presses " time(s)", X_TOOLTIP.3, Y_TOOLTIP.3, 3
    set_random_delays(45, 85)
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

; Searches a given screen area for a pixel of the given color then clicks it.
; scanAreaInput can be a preset name (see GetScanArea below)
PixelSearchAndClick(PixelColor, scanAreaInput := 0, click_type := 0, offset := 0, x1 := 0, y1 := 0, x2 := 0, y2 := 0, shade_variance := 0) {
    menu_width := 140
    if scanAreaInput != 0 {
        scanArea := GetScanArea(scanAreaInput)
    } else {
        scanArea := { x1: x1, y1: y1, x2: x2, y2: y2 }
    }
    if WinActive(runelite_window) {
        set_random_delays()
        if PixelSearch(&foundX, &foundY, scanArea.x1, scanArea.y1, scanArea.x2, scanArea.y2, PixelColor, shade_variance) {
            offsetObj := GetOffset(offset)
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            ClickOffset(click_type, offsetX, offsetY)
            return true
        }
    }
    return false
}

; Searches a given screen area for an image then clicks it.
; scanAreaInput may be a preset area name.
ImageSearchAndClick(ImageURL, scanAreaInput := 0, click_type := 0, offset := 0, x1 := 0, y1 := 0, x2 := 0, y2 := 0, shade_variance := 50) {
    menu_width := 140
    if scanAreaInput != 0 {
        scanArea := GetScanArea(scanAreaInput)
    } else {
        scanArea := { x1: x1, y1: y1, x2: x2, y2: y2 }
    }
    SplitPath ImageURL, &ImageName
    if WinActive(runelite_window) {
        set_random_delays()
        if (ImageSearch(&foundX, &foundY, scanArea.x1, scanArea.y1, scanArea.x2, scanArea.y2, "*" shade_variance " *TransBlack " ImageURL)
         or ImageSearch(&foundX, &foundY, scanArea.x1, scanArea.y1, scanArea.x2, scanArea.y2, "*" shade_variance " " ImageURL)) {
            ToolTip "8. ImageSearchAndClick: Found " ImageName, X_TOOLTIP.8, Y_TOOLTIP.8, 8
            offsetObj := GetOffset(offset)
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            ClickOffset(click_type, offsetX, offsetY)
            return true
        }
    }
    return false
}

; Returns a scan area object based on preset names.
; (These names – such as "p2", "middle", "bank", etc. – are used in your Fishing Trawler script.)
GetScanArea(scan_area := 0) {
    menu_width := 0
    gameWindowWidth := A_ScreenWidth - 20
    switch scan_area {
        case "top_left":
            scan_area_obj := { x1: 0, y1: 22, x2: 190, y2: 75 }
        case "bag":
            scan_area_obj := { x1: 1645, y1: 700, x2: 1855, y2: 1000 }
        case "chat_all":
            scan_area_obj := { x1: 3, y1: 872, x2: 494, y2: 986 }
        case "chat_bottom":
            scan_area_obj := { x1: 3, y1: 969, x2: 494, y2: 986 }
        case "chat_bottom_2":
            scan_area_obj := { x1: 3, y1: 958, x2: 510, y2: 1015 }
        case "middle":
            scan_area_obj := { x1: 0, y1: 200, x2: 1650, y2: 970 }
        case "center":
            scan_area_obj := { x1: A_ScreenWidth / 4, y1: A_ScreenHeight / 4, x2: A_ScreenWidth * 3 / 4, y2: A_ScreenHeight * 3 / 4 }
        case "bank":
            scan_area_obj := { x1: 575, y1: 50, x2: 1060, y2: 850 }
        case "under_mouse":
            MouseGetPos(&x, &y)
            scan_area_obj := { x1: x - 130, y1: y - 10, x2: x + 120, y2: y + 255 }
        case "p1":
            scan_area_obj := { x1: 0, y1: 20, x2: A_ScreenWidth / 3, y2: A_ScreenHeight / 2 }
        case "p2":
            scan_area_obj := { x1: A_ScreenWidth / 3, y1: 20, x2: A_ScreenWidth * 2 / 3, y2: A_ScreenHeight / 2 }
        case "p3":
            scan_area_obj := { x1: A_ScreenWidth * 2 / 3, y1: 20, x2: A_ScreenWidth - 20, y2: A_ScreenHeight / 2 }
        case "p4":
            scan_area_obj := { x1: 0, y1: A_ScreenHeight / 2, x2: A_ScreenWidth / 3, y2: A_ScreenHeight - 50 }
        case "p5":
            scan_area_obj := { x1: A_ScreenWidth / 3, y1: A_ScreenHeight / 2, x2: A_ScreenWidth * 2 / 3, y2: A_ScreenHeight - 50 }
        case "p6":
            scan_area_obj := { x1: A_ScreenWidth * 2 / 3, y1: A_ScreenHeight / 2, x2: A_ScreenWidth - 20, y2: A_ScreenHeight - 50 }
        default:
            scan_area_obj := { x1: 0, y1: 20, x2: A_ScreenWidth - 20, y2: A_ScreenHeight - 50 }
    }
    if menu_is_open() {
        scan_area_obj.x1 -= menu_width
        scan_area_obj.x2 -= menu_width
    }
    return scan_area_obj
}

; In this project we assume the RuneLite menu is closed.
menu_is_open() {
    return false
}

; Returns an offset object based on a preset offset name.
GetOffset(offset_item) {
    switch offset_item {
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

; Click at a given offset using the specified click type.
ClickOffset(click_type, offset_x := 0, offset_y := 0) {
    switch click_type {
        case "right":
            Click("right", offset_x, offset_y)
        case "left":
            Click(offset_x, offset_y)
        case "mouseover":
            Click(offset_x, offset_y, 0)
        case "doubleclick":
            Click(offset_x, offset_y, 2)
        case "in_place":
            Click()
    }
}
