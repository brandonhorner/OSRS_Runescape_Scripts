; This file is for testing purposes and should remain convenient to open
global XTOOLTIP := 600
global YTOOLTIP := 550

CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")

SetWorkingDir A_MyDocuments "\AutoHotkey_Scripts\runescape"
SetControlDelay -1

; these are image files used for image searching
global images := {
    menaphite_hovering_text : A_WorkingDir "\image_library\blackjacking\menaphite_hovering_text.png",
    lobster_cooked : A_WorkingDir "\image_library\lobster_cooked.png",
    lobster_cooked_noted : A_WorkingDir "\image_library\blackjacking\lobster_cooked_noted.png",
    knockout_option : A_WorkingDir "\image_library\blackjacking\knockout_option.bmp",
    knockout_success : A_WorkingDir "\image_library\blackjacking\knockout_success.bmp",
    knockout_failure : A_WorkingDir "\image_library\blackjacking\knockout_failure.bmp",
    pickpocket_option : A_WorkingDir "\image_library\blackjacking\pickpocket_option.bmp",
    pickpocket_attempt : A_WorkingDir "\image_library\blackjacking\pickpocket_attempt.bmp",
    pickpocket_success : A_WorkingDir "\image_library\blackjacking\pickpocket_success.bmp",
    pickpocket_failure : A_WorkingDir "\image_library\blackjacking\pickpocket_failure.bmp",
    cant_pickpocket_combat : A_WorkingDir "\image_library\blackjacking\cant_pickpocket_combat.png",
    right_click_options : A_WorkingDir "\image_library\blackjacking\right_click_options.png",
    cannot_knockout : A_WorkingDir "\image_library\blackjacking\cannot_do_that.bmp",
    healthbar : A_WorkingDir "\image_library\blackjacking\healthbar.bmp",
    stunned : A_WorkingDir "\image_library\blackjacking\stunned.bmp",
    imstunned : A_WorkingDir "\image_library\blackjacking\imstunned.png",
    missed_right_click : A_WorkingDir "\image_library\blackjacking\missed_right_click.bmp",
    combat : A_WorkingDir "\image_library\blackjacking\combat.bmp",
    money_bag : A_WorkingDir "\image_library\blackjacking\money_bag.png",
    money_bag_full : A_WorkingDir "\image_library\blackjacking\money_bag_full.png",
    minimap_bank_icon : A_WorkingDir "\image_library\minimap_bank_icon.png",
    open_bag : A_WorkingDir "\image_library\open_bag.bmp",
    minimap_cake_stall_icon : A_WorkingDir "\image_library\minimap_cake_stall_icon.png",
    deposit_inventory : A_WorkingDir "\image_library\deposit_inventory.png",
    open_curtain_option : A_WorkingDir "\image_library\blackjacking\open_curtain.png",
    close_curtain_option : A_WorkingDir "\image_library\blackjacking\close_curtain.png",
    select_an_option : A_WorkingDir "\image_library\blackjacking\select_an_option.png",
    stunned : A_WorkingDir "\image_library\been_stunned.bmp"
}

; some tooltip coords
global X_TOOLTIP := {
    1: 0,   ; <-| main functions
    2: 0,   ; <-|
    3: 0,   ; <-|
    4: 980, ; <-|
    
    5: 0,  ; <-| image search / support functions
    6: 0,  ; <-|
    7: 0,  ; <-|
    8: 0,  ; <-|
    9: 0   ; <-|
}

global Y_TOOLTIP := {
    1: 100, ; <-| main functions
    2: 125, ; <-|
    3: 150, ; <-|
    4: 205, ; <-|

    5: 205, ; <-| image search / support functions
    6: 230, ; <-|
    7: 285, ; <-|
    8: 325, ; <-|
    9: 375  ; <-|
}


gameWindowWidth := A_ScreenWidth - 20
; object that holds all of the screen area coordinates
global coord := {
    chat_all:       { x1: 3, y1: 872, x2: 494, y2: 986 },
    chat_bottom:    { x1: 3, y1: 969, x2: 494, y2: 986 },
    chat_bottom_2:  { x1: 3, y1: 958, x2: 494, y2: 986 },
    bag:        { x1:1385, y1:700, x2:1855, y2:1000 },
    top_left:   { x1:0, y1:22, x2:200, y2:128 },
    middle:     { x1:0, y1:200, x2:1650, y2:970 },
    health:     { x1:1400, y1:820, x2:1700, y2:850 },
    
    ; Screen below is split up like this:
    ;                ;                ;               ;
    ;       p1       ;       p2       ;       p3      ;
    ;________________;________________;_______________;
    ;                ;                ;               ;
    ;       p4       ;       p5       ;       p6      ;
    ;                ;                ;               ;
    p1 : { x1:0, y1:20, x2:gameWindowWidth / 3, y2:A_ScreenHeight / 2 },
    p2 : { x1:gameWindowWidth / 3, y1:20, x2:gameWindowWidth * 2 / 3, y2:A_ScreenHeight / 2 },
    p3 : { x1:gameWindowWidth * 2 / 3, y1:20, x2:gameWindowWidth, y2:A_ScreenHeight / 2 },
    p4 : { x1:0, y1:A_ScreenHeight / 2, x2:gameWindowWidth / 3, y2:A_ScreenHeight},
    p5 : { x1:gameWindowWidth / 3, y1:A_ScreenHeight / 2, x2:gameWindowWidth * 2 / 3, y2:A_ScreenHeight},
    p6 : { x1:gameWindowWidth * 2 / 3, y1:A_ScreenHeight / 2, x2:gameWindowWidth, y2:A_ScreenHeight}
}

/**
 * coords to ensure an NPC's orientation
 * add more vertices to these :o
 */
global target_coord := {
    laying_left:    { x:745, y:330 },
    laying_middle:  { x:890, y:225 },
    laying_right:   { x:1030,y:380 },
    laying_bottom:  { x:805, y:600 },
    laying_left_2:    { x:824, y:330 },
    laying_middle_2:  { x:965, y:225 },
    laying_right_2:   { x:1105,y:375 },
    laying_bottom_2:  { x:890, y:600 },
    standing_top_left:      { x:805, y:240 },
    standing_top_right:     { x:975, y:245 },
    standing_bottom_left:   { x:805, y:600 },
    standing_bottom_right:  { x:940, y:535 },
    standing_top_left_2:        { x:885, y:245 },
    standing_top_right_2:       { x:1055,y:245 },
    standing_bottom_left_2:     { x:890, y:600 },
    standing_bottom_right_2:    { x:1030,y:530 }
}

; these are the colors of outlines around NPCs and the tick on the compass
global pixel_color := {
    tile_teal : 0x00FAFF,
    tile_purple : 0x6655FF,
    tile_pink : 0xD769E8,
    object_green: 0xAAFF00,
    bag_background: 0x3E3529,
    npc : 0xA4FF00,
    npc_dark : 0x84CD00,
    tick : 0x00DFDF,
    tick_2 : 0x1580AD,
    tick_3 : 0x01E0E1
}


;zooms the camera out to max by default
zoom(zoom_direction, zoom_level:=30)
{
    if (zoom_direction = "out")
    {
        Loop zoom_level
        {
            ControlSend "{WheelDown}",, runelite_window
            SleepRandom(45, 65)
        }
    }
    else ;zooming in
    {
        Loop zoom_level
        {
            ControlSend "{WheelUp}",, runelite_window
            SleepRandom(35, 55)
        }
    }
    return
}


CheckIfFullOnMoneyBags()
{
    SendKey("1")
    if offset := ImageSearchAndClick(images.money_bag_full, "bag", "mouseover", "item") {
                                                                                ToolTip "Clicking the FULL money bag :')...", X_TOOLTIP.1, Y_TOOLTIP.1, 1
        SleepRandom(400, 900)
        ControlClick( "x" offset.x " y" offset.y, runelite_window,, "Left")
        SleepRandom(500, 900)
        return true
    }
    return false
}

; Function to display tooltip and send a key
SendKey(key, presses := 1){

    if (presses <= 1){
        ControlSend "{" key "}",, runelite_window
        return
    }
    if (presses > 1){
        ControlSend "{" key "}",, runelite_window
        SendKey key, presses - 1
        Return
    }
}

SleepRandom(sleep_time_low, sleep_time_high)
{
    sleep_time := Random(sleep_time_low, sleep_time_high)
    Sleep sleep_time
    
    return sleep_time
}

ImageSearchAndClick(ImageURL, scanAreaInput:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0, shade_variance:=50)
{
    menu_width := 140
    
    if scanAreaInput != 0
    {
        scanArea := GetScanArea(scanAreaInput)
    }
    else
    {
        scanArea := {
            x1: x1, y1: y1, 
            x2: x2, y2: y2
        }
    }
    
    SplitPath ImageURL, &ImageName
    
    if WinActive(runelite_window)
    {
        if (ImageSearch(&foundX, &foundY,
                        scanArea.x1, scanArea.y1,
                        scanArea.x2, scanArea.y2, 
                        "*" shade_variance " *TransBlack " ImageURL)
        or ImageSearch(&foundX, &foundY,
                        scanArea.x1, scanArea.y1,
                        scanArea.x2, scanArea.y2,
                        "*" shade_variance " " ImageURL))
        {
                                                                                    ToolTip "8. ImageSearchAndClick: Looking for:`n" ImageName " was found at: (" foundX ", " foundY ")", X_TOOLTIP.8, Y_TOOLTIP.8, 8
            ;depending on what type of image, the offset will be different
            offsetObj := GetOffset(offset)
            
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            offset := {
                x : offsetX,
                y : offsetY
            }

            ClickOffset(click_type, offsetX, offsetY)
            return offset
        }
    }
    return false
}

; if menu is open, create a msg box to close the menu, false otherwise
MenuIsOpen()
{
    menu_bg_color := 0x282828

    if(PixelSearchAndClick(1867, 450, 1874, 600, menu_bg_color,,,,0))
    {
        MsgBox("Please close the RuneLite menu.")
        MenuIsOpen()
    }
    ; menu was not open (pixel color of menu background was not found)
    return false
}

PixelSearchAndClick(PixelColor, scanAreaInput:=0, click_type:=0, offset:=0, x1:=0, y1:=0, x2:=0, y2:=0, shade_variance:=0)
{
    menu_width := 140
    
    if scanAreaInput != 0
    {
        scanArea := GetScanArea(scanAreaInput)
    }
    else
    {
        scanArea := {
            x1: x1, y1: y1, 
            x2: x2, y2: y2
        }
    }

    if WinActive(runelite_window)
    {
        ; delays should be randomized often
        ;set_random_delays()
        
        if PixelSearch(&foundX, &foundY,
                        scanArea.x1, scanArea.y1,
                        scanArea.x2, scanArea.y2, 
                        PixelColor, shade_variance ) {
                                                                                          ToolTip "8. PixelSearchAndClick: " PixelColor " was found at: (" foundX ", " foundY ")", X_TOOLTIP.8, Y_TOOLTIP.8, 8
            ;depending on what area we are clicking, the offset will be different
            offsetObj := GetOffset(offset) ;TODO separate this into GetPixelOffset / GetImageOffset?
            
            offsetX := foundX + offsetObj.x
            offsetY := foundY + offsetObj.y
            
            ClickOffset(click_type, offsetX, offsetY)
            return true
        }
    }
    return false
}

GetScanArea(scan_area := 0)
{
    menu_width := 0
    ; adjusted window width to not include menu.. clashes with the menu width adjustment though :\
    gameWindowWidth := A_ScreenWidth - 20
    switch scan_area
    {
        case "top_left":
            scan_area_obj := {
                x1: 0, y1: 22,
                x2: 190, y2: 75
            }
            menu_width := 0
            
        case "bag":
            scan_area_obj := {
                x1: 1645, y1: 700,
                x2: 1855, y2: 1000
            }
            menu_width += 100
            
        case "chat_all":
            scan_area_obj := {
                x1: 3, y1: 872,
                x2: 494, y2: 986
            }
            menu_width := 0

        case "chat_bottom":
            scan_area_obj := {
                x1: 3, y1: 969,
                x2: 494, y2: 986
            }
            menu_width := 0

        case "chat_bottom_2":
            scan_area_obj := {
                x1: 3, y1: 958,
                x2: 510, y2: 1015
            }
            menu_width := 0
            
        case "middle":
            scan_area_obj := {
                x1: 0, y1: 200,
                x2: 1650, y2: 970
            }
            menu_width := 0

        case "center":
            scan_area_obj := {
                x1: A_ScreenWidth / 4, y1: A_ScreenHeight /4,
                x2: A_ScreenWidth * 3 / 4, y2: A_ScreenHeight * 3 / 4
            }
            menu_width := 0
            
        case "bank":
            scan_area_obj := {
                x1: 575, y1: 50, 
                x2: 1060, y2: 850
            }

        case "under_mouse":
            MouseGetPos(&x, &y)
            scan_area_obj := {
                x1: x - 130, y1: y - 10,
                x2: x + 120, y2: y + 255
            } 
            menu_width := 0
        
        case "p1":
            scan_area_obj := {
                x1:0, y1:20, 
                x2:A_ScreenWidth / 3, y2:A_ScreenHeight / 2
            } 
            menu_width := 0
        case "p2":
            scan_area_obj := {
                x1:A_ScreenWidth / 3, y1:20,
                x2:A_ScreenWidth * 2 / 3, y2:A_ScreenHeight / 2
            } 
            menu_width := 0
        case "p3":
            scan_area_obj := {
                x1:A_ScreenWidth * 2 / 3, y1:20,
                x2:A_ScreenWidth - 20, y2:A_ScreenHeight / 2
            } 
            menu_width := 0
        case "p4":
            scan_area_obj := {
                x1:0, y1:A_ScreenHeight / 2,
                x2:A_ScreenWidth / 3, y2:A_ScreenHeight - 50
            } 
            menu_width := 0
        case "p5":
            scan_area_obj := {
                x1:A_ScreenWidth / 3, y1:A_ScreenHeight / 2,
                x2:A_ScreenWidth * 2 / 3, y2:A_ScreenHeight - 50
            } 
            menu_width := 0

        case "p6":
            scan_area_obj := {
                x1:A_ScreenWidth * 2 / 3, y1:A_ScreenHeight / 2,
                x2:A_ScreenWidth - 20, y2:A_ScreenHeight - 50
            } 
            menu_width := 0

        default:
            scan_area_obj := {
                x1: 0, y1: 20, 
                x2: A_ScreenWidth-20, y2: A_ScreenHeight-50
            }
            menu_width := 0
    }
    if MenuIsOpen()
    {
        scan_area_obj.x1 -= menu_width
        scan_area_obj.x2 -= menu_width
    }
    return scan_area_obj
}

GetOffset(offset_item)
{
    switch offset_item {
        ;"option" refers to when you "right" click in-game, the top "left" of the image is 0,0
        case "option":
            ;we want to move mouse to the right 52 to 92 pixels to click more in the center of the image
            horizontal := Random(0, 200)
            ;we want to move mouse down 2 to 11 pixels to click randomly within the image
            vertical := Random(1, 10)

        ;"option_short" refers to when the right click menu is half sized from the usual
        case "option_short":
            ;we want to move mouse horizontally to click more in the center of the image
            horizontal := Random(-1, 100) ;30
            ;we want to move mouse down vertical pixels to click randomly within the image
            vertical := Random(-2, 5)

        ;"item" refers to an item in the bag, also works for fishing spot indicators
        case "item":
            ;item pictures are cut so that the"middle" of the image is the starting point
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

        case "south":
            horizontal := Random(0, 0)
            vertical := Random(10, 30)

        case "southish":
            horizontal := Random(-15, 15)
            vertical := Random(20, 80)

        case "minimap_icon":
            horizontal := Random(0,5)
            vertical := Random(0,5)

        ;default is no offset, can be used when searching but not clicking on an image
        default:
            horizontal := 0
            vertical := 0
    }

    offset := {
        x : horizontal, 
        y : vertical
    }

    return offset
}

ClickOffset(click_type, offset_x := 0, offset_y := 0)
{
    switch click_type
    {
        case "right":
            ControlClick "x" offset_x " y" offset_y, runelite_window,, "Right",, "NA"
            
        case "left":
            ControlClick "x" offset_x " y" offset_y, runelite_window,,,, "NA"
            
        case "mouseover":
            ControlClick "x" offset_x " y" offset_y, runelite_window,,,, "NA"
            
        case "doubleclick":
            ControlClick "x" offset_x " y" offset_y, runelite_window,,, 2, "NA"
            
        case "in_place":
            ControlClick , runelite_window,,,, "NA"

        ; otherwise we don't do anything
    }
}
