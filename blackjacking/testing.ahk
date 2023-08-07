#Include ..\utilities.ahk
#Include BlackJacker.ahk

;if WinActive(runelite_window)
    ;Tooltip("testing On +` to reload and F3-F5 to test, ", 0, 22, 8)

+`::Reload()

F3::
{
    test_ImageExists()
}

F4::
{
    test_RightClickNPC()
}

F5::
{
    setup_in()
}

test_ImageExists()
{
    if (ImageExists(states["pickpocket_success"]["image_url"], coord.chat.x1, coord.chat.y1, coord.chat.x2, coord.chat.y2 ))
        ToolTip "Found it!", 500, 500, 9
    else
        ToolTip "Didn't find it!", 500, 500, 9

}

test_EatLobster()
{
    if EatLobster()
        ToolTip("EatLobster succeeded!", tooltip_x, 500, 2)
    else
        ToolTip("eat_Lobster failed...", tooltip_x, 500, 2)
}
test_RightClickNPC()
{
    ; clicks need to be fast (but not instant), we'll add sleeps when necessary
    SetDefaultMouseSpeed(1)

    if WinActive(runelite_window)
    {
        ; First check if the right click option is already active
        if (ImageExists(images.knockout_option) || ImageExists(images.pickpocket_option))
            return true
        
        target_click_area := GetTargetClickArea()
        offset_x := Random(-50, 50)
        offset_y := Random(-50, 50)
        target_x := target_click_area.x + offset_x
        target_y := target_click_area.y + offset_y
        
        Click(target_x, target_y, "Right")
        ;ToolTip, in while %count%: `r%x1%x%y1%'r%x2%x%y2% `rPixel:%enemy_color%, %tooltip_x%, %tooltip_y%, 2
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
    if pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + offset, target_coord.standing_top_left.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + offset, target_coord.standing_top_left.y + offset, enemy_color_dark) ||
        pixel_search_and_click(target_coord.standing_top_left_2.x, target_coord.standing_top_left_2.y, target_coord.standing_top_left_2.x + offset, target_coord.standing_top_left_2.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_top_left_2.x, target_coord.standing_top_left_2.y, target_coord.standing_top_left_2.x + offset, target_coord.standing_top_left_2.y + offset, enemy_color_dark)
        top_left_found := True
    
    top_right_found := false
    if pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + offset, target_coord.standing_top_right.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + offset, target_coord.standing_top_right.y + offset, enemy_color_dark) ||
        pixel_search_and_click(target_coord.standing_top_right_2.x, target_coord.standing_top_right_2.y, target_coord.standing_top_right_2.x + offset, target_coord.standing_top_right_2.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_top_right_2.x, target_coord.standing_top_right_2.y, target_coord.standing_top_right_2.x + offset, target_coord.standing_top_right_2.y + offset, enemy_color_dark)
        top_right_found := true
    
    bottom_left_found := false
    if pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + offset, target_coord.standing_bottom_left.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + offset, target_coord.standing_bottom_left.y + offset, enemy_color_dark) ||
        pixel_search_and_click(target_coord.standing_bottom_left_2.x, target_coord.standing_bottom_left_2.y, target_coord.standing_bottom_left_2.x + offset, target_coord.standing_bottom_left_2.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_bottom_left_2.x, target_coord.standing_bottom_left_2.y, target_coord.standing_bottom_left_2.x + offset, target_coord.standing_bottom_left_2.y + offset, enemy_color_dark)
        bottom_left_found := true
    
    bottom_right_found := false
    if pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + offset, target_coord.standing_bottom_right.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + offset, target_coord.standing_bottom_right.y + offset, enemy_color_dark) ||
        pixel_search_and_click(target_coord.standing_bottom_right_2.x, target_coord.standing_bottom_right_2.y, target_coord.standing_bottom_right_2.x + offset, target_coord.standing_bottom_right_2.y + offset, enemy_color) ||
        pixel_search_and_click(target_coord.standing_bottom_right_2.x, target_coord.standing_bottom_right_2.y, target_coord.standing_bottom_right_2.x + offset, target_coord.standing_bottom_right_2.y + offset, enemy_color_dark)
        bottom_right_found := true
    
    
    ToolTip("Standing?`nTop Left: " top_left_found " Top Right: " top_right_found " `nBottom Left: " bottom_left_found " Bottom Right: " bottom_right_found, 100, 600, 7)
}

test_target_is_laying_down()
{
    left_found := False
    if (pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, enemy_color_dark))
        left_found := True
    middle_found := false
    if (pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, enemy_color_dark))
        middle_found := true
    right_found := false
    if (pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, enemy_color_dark))
        right_found := true

    bottom_found := false
    if (pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, enemy_color_dark))
        bottom_found := true
    
    ToolTip("Laying Down?`n     Top: " middle_found " `nLeft: " left_found " Right: " right_found "`n    Bottom: " bottom_found, 100, 660, 6)
}

testing_RightClickNPC()
{
    if(RightClickNPC())
        ToolTip("Right click achieved!...", tooltip_x, 500, 2)
    else
        ToolTip("Right click failed...", tooltip_x, 500, 2)
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
