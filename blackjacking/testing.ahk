#Include ..\utilities.ahk
#Include BlackJacker.ahk

+`::Reload()

F3::
{
    test_standing_and_laying()
}

F4::
{
    test_target_is_laying_down()
}

F5::
{
    test_right_click_bandit()
}

test_target_is_laying_down()
{
    if (pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, enemy_color_dark))
        left_found := True
    else
        left_found := False
    if (pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, enemy_color_dark))
        middle_found := true
    else
        middle_found := false
    if (pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, enemy_color_dark))
        right_found := true
    else
        right_found := false
    if (pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, enemy_color_dark))
        bottom_found := false
    else
        bottom_found := true
    
    ToolTip("Left: " left_found " Middle: " middle_found " Right: " right_found " Bottom: " bottom_found, 100, 500, 9)
}

test_target_is_standing_up()
{
    if (pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + 30, target_coord.standing_top_left.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + 30, target_coord.standing_top_left.y + 30, enemy_color_dark))
        top_left_found := True
    else
        top_left_found := False
    if (pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + 30, target_coord.standing_top_right.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + 30, target_coord.standing_top_right.y + 30, enemy_color_dark))
        top_right_found := true
    else
        top_right_found := false
    if (pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + 30, target_coord.standing_bottom_left.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + 30, target_coord.standing_bottom_left.y + 30, enemy_color_dark))
        bottom_left_found := true
    else
        bottom_left_found := false
    if (pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + 30, target_coord.standing_bottom_right.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + 30, target_coord.standing_bottom_right.y + 30, enemy_color_dark))
        bottom_right_found := true
    else
        bottom_right_found := false
    
    ToolTip("Top Left: " top_left_found " Top Right: " top_right_found " Bottom Left: " bottom_left_found " Bottom Right: " bottom_right_found, 100, 500, 9)
}

test_right_click_bandit()
{
    if(right_click_bandit())
        ToolTip("Right click achieved!...", tooltip_x, 500, 2)
    else
        ToolTip("Right click failed...", tooltip_x, 500, 2)
}

test_standing_and_laying()
{
    if(target_is_standing_up()){
        ToolTip("Target is... STANDING!", 100, 500, 9)
    }
    else if(target_is_laying_down())
    {
        ToolTip("Target is... LAYING DOWN!", 100, 500, 9)
    }
    else
    {
        ToolTip("Error: Target is.., NOT standing OR laying down.", 100, 500, 9)
    }  
}
