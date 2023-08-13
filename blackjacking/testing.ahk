#Include ..\utilities.ahk
#Include BlackJacker.ahk

;if WinActive(runelite_window)
    ;Tooltip("testing On +` to reload and F3-F5 to test, ", 0, 22, 8)

+`::Reload()

F3::
{
    if ImageSearchAndClick(images.money_bag, "bag", "mouseover", "item")
        ToolTip "Found it!", 0, 500, 9
    else
        ToolTip "Didn't find it!", 0, 500, 9
}

F4::
{
    RightClickNPC()
}

F5::
{
    ClickKnockout()
    ToolTip "knockout success: ", 100, 100, 1
}

F6::
{
    ClickPickpocket()
}

test_ImageExists()
{
    if ( ImageExists(images.pickpocket_success), coord.chat.x1, coord.chat.y1, coord.chat.x2, coord.chat.y2 )
        ToolTip "Found it!", 100, 500, 9
    else
        ToolTip "Didn't find it!", 100, 500, 9
}

test_ImageExistsRightClick()
{
    if (ImageExists(images.right_click_options))
        ToolTip "Found it!", 100, 500, 9
    else
        ToolTip "Didn't find it!", 100, 500, 9
}

test_EatLobster()
{
    if EatLobster()
        ToolTip("EatLobster succeeded!", 0, 500, 2)
    else
        ToolTip("eat_Lobster failed...", 0, 500, 2)
}

test_RightClickNPC()
{
    if (ImageExists(images.right_click_options))
        return true
    ; clicks need to be fast (but not instant), we'll add sleeps when necessary
    SetDefaultMouseSpeed(1)

    ; Get the target click area
    click_area := GetTargetClickArea()
    offset_x := Random(-70, 70)
    offset_y := Random(-70, 120)

    ; Randomize within the area and right click
    ToolTip("Right Clicking:`roffset x:" offset_x ", y:" offset_y "`rx:" click_area.x ", y:" click_area.y, 100, 600, 8)
    x := click_area.x + offset_x
    y := click_area.y + offset_y
    MouseMove(x, y)
    ; If target is in sight
    if WaitForImage(images.menaphite_hovering_text, 700) {
        Click("Right")
        return true
    }
    return false
}

test_GetTargetClickArea()
{
    target_area := {
        x:0 , y:0
    }

    if TargetIsLayingDownFacingMe()
    {
        ; x is (left + (right - left) / 2))
        target_area.x := target_coord.laying_left.x + 15 + ((target_coord.laying_right.x - target_coord.laying_left.x) / 2)
        ; y is (bottom - ((bottom - top) / 2))
        target_area.y := target_coord.laying_bottom.y - ((target_coord.laying_bottom.y - target_coord.laying_left.y) / 2)
    }
    else if TargetIsStandingUpFacingMe()
    {   ; x is (left + (right - left) / 2))
        target_area.x := target_coord.standing_top_left.x + 15 + ((target_coord.standing_top_right.x - target_coord.standing_top_left.x) / 2)
        ; y is (bottom - ((bottom - top) / 2))
        target_area.y := target_coord.standing_bottom_right.y - ((target_coord.standing_bottom_right.y - target_coord.standing_top_right.y) / 2)
    }
    return target_area
}

test_target_is_standing_up()
{
    offset := 30
    top_left_found := False
    if pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + offset, target_coord.standing_top_left.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + offset, target_coord.standing_top_left.y + offset, pixel_color.enemy_dark) ||
        pixel_search_and_click(target_coord.standing_top_left_2.x, target_coord.standing_top_left_2.y, target_coord.standing_top_left_2.x + offset, target_coord.standing_top_left_2.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_top_left_2.x, target_coord.standing_top_left_2.y, target_coord.standing_top_left_2.x + offset, target_coord.standing_top_left_2.y + offset, pixel_color.enemy_dark)
        top_left_found := True
    
    top_right_found := false
    if pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + offset, target_coord.standing_top_right.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + offset, target_coord.standing_top_right.y + offset, pixel_color.enemy_dark) ||
        pixel_search_and_click(target_coord.standing_top_right_2.x, target_coord.standing_top_right_2.y, target_coord.standing_top_right_2.x + offset, target_coord.standing_top_right_2.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_top_right_2.x, target_coord.standing_top_right_2.y, target_coord.standing_top_right_2.x + offset, target_coord.standing_top_right_2.y + offset, pixel_color.enemy_dark)
        top_right_found := true
    
    bottom_left_found := false
    if pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + offset, target_coord.standing_bottom_left.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + offset, target_coord.standing_bottom_left.y + offset, pixel_color.enemy_dark) ||
        pixel_search_and_click(target_coord.standing_bottom_left_2.x, target_coord.standing_bottom_left_2.y, target_coord.standing_bottom_left_2.x + offset, target_coord.standing_bottom_left_2.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_bottom_left_2.x, target_coord.standing_bottom_left_2.y, target_coord.standing_bottom_left_2.x + offset, target_coord.standing_bottom_left_2.y + offset, pixel_color.enemy_dark)
        bottom_left_found := true
    
    bottom_right_found := false
    if pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + offset, target_coord.standing_bottom_right.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + offset, target_coord.standing_bottom_right.y + offset, pixel_color.enemy_dark) ||
        pixel_search_and_click(target_coord.standing_bottom_right_2.x, target_coord.standing_bottom_right_2.y, target_coord.standing_bottom_right_2.x + offset, target_coord.standing_bottom_right_2.y + offset, pixel_color.enemy) ||
        pixel_search_and_click(target_coord.standing_bottom_right_2.x, target_coord.standing_bottom_right_2.y, target_coord.standing_bottom_right_2.x + offset, target_coord.standing_bottom_right_2.y + offset, pixel_color.enemy_dark)
        bottom_right_found := true
    
    
    ToolTip("Standing?`nTop Left: " top_left_found " Top Right: " top_right_found " `nBottom Left: " bottom_left_found " Bottom Right: " bottom_right_found, 100, 600, 7)
}

test_target_is_laying_down()
{
    left_found := False
    if (pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, pixel_color.enemy)
        || pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, pixel_color.enemy_dark))
        left_found := True
    middle_found := false
    if (pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, pixel_color.enemy)
        || pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, pixel_color.enemy_dark))
        middle_found := true
    right_found := false
    if (pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, pixel_color.enemy)
        || pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, pixel_color.enemy_dark))
        right_found := true

    bottom_found := false
    if (pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, pixel_color.enemy)
        || pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, pixel_color.enemy_dark))
        bottom_found := true
    
    ToolTip("Laying Down?`n     Top: " middle_found " `nLeft: " left_found " Right: " right_found "`n    Bottom: " bottom_found, 100, 660, 6)
}

testing_RightClickNPC()
{
    if(RightClickNPC())
        ToolTip("Right click achieved!...", 0, 500, 2)
    else
        ToolTip("Right click failed...", 0, 500, 2)
}

test_standing_and_laying()
{
    if(TargetIsStandingUpFacingMe()){
        ToolTip("Target is... STANDING!", 100, 550, 5)
    }
    else if(TargetIsLayingDownFacingMe())
    {
        ToolTip("Target is... LAYING DOWN!", 100, 550, 5)
        return
    }
    else
    {
        ToolTip("Error: Target is.., NOT standing OR laying down.", 100, 550, 5)
    }  
}

test_waitforpixel()
{
    if (WaitForPixel(pixel_color.tick,1700, 121, 1701, 121))
        ToolTip("Found ze pixel!...", 0, 500, 2)
}

test_Eat_Lobster()
{    
    if ImageSearchAndClick(images.lobster_cooked, "bag", "mouseover", "item") {
        sleep_random(400, 1500)
        ToolTip("Found the Lobster!...", X_TOOLTIP.4, Y_TOOLTIP.4, 4)
        return true
    }
    return false
}