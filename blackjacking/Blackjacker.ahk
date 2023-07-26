;REQUIRED:
; Runelite client, change your name in the window names in the code below.
; This was made on a 1920 x 1080 screen size. (In Windows)
; You must set the bot up each time:
;   - your inventory depletes of lobsters.
;   - the target disappears through a wall
; You must have 'Status Bars' in RuneLite on so that your health bar is shown on the left of your "bag".
; You must have 'NPC Indicators' highlight color the same as in the script (0xA4FF00).
;OPTIONAL:
; Have your chat turned to "Game" Chat, this would help because we search for phrases in the chat box.
#SingleInstance
#Include ..\utilities.ahk
SetWorkingDir A_MyDocuments "\AutoHotkey_Scripts\runescape"
CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")

SetMouseDelay(80)


global enemy_color := 0xA4FF00 ; Menaphite - 666317 ; Bandit - CAD0B6 ; - all of them (inaccurate) A4FF00 ; some green color
global enemy_color_dark := 0x84CD00
; Object that holds all of the screen area coordinates
global coord := {
    chat: {
        x1: 7, y1: 965,
        x2: 515, y2: 1015 
    },
    bag: {
        x1:1385, y1:700,
        x2:1855, y2:1000
    },
    top_left: {
        x1:0, y1:22,
        x2:190, y2:75
    },
    middle: {
        x1:0, y1:200,
        x2:1650, y2:970
    }
}

global num_of_tries := 7
global attack_menaphite_hovering_text := A_WorkingDir "\image_library\attack_menaphite_hovering_text.png"
global lobster_cooked := A_WorkingDir "\image_library\lobster_cooked.png"
global attack := A_WorkingDir "\image_library\attack_top_left.bmp"
global failed_pickpocket := A_WorkingDir "\image_library\failed_pickpocket.bmp"
global glancing_blow := A_WorkingDir "\image_library\glancing_blow.bmp"
global knockout_option := A_WorkingDir "\image_library\knockout_option.bmp"
global pickpocket_option := A_WorkingDir "\image_library\pickpocket_option.bmp"
global right_click_options := A_WorkingDir "\image_library\right_click_options.png"
global unconscious := A_WorkingDir "\image_library\unconscious.bmp"
global cannot_knockout := A_WorkingDir "\image_library\cannot_do_that.bmp"
global healthbar := A_WorkingDir "\image_library\healthbar.bmp"
global stunned := A_WorkingDir "\image_library\stunned.bmp"
global missed_right_click := A_WorkingDir "\image_library\missed_right_click.bmp"
global combat := A_WorkingDir "\image_library\combat.bmp"
global money_bag := A_WorkingDir "\image_library\money_bag.bmp"
global runelite_window := "RuneLite - BinaryBilly"

global tooltip_x := 600
global tooltip_y := 550

global target_coord := {
    laying_left: {
        x:670, y:325
    },
    laying_middle: {
        x:840, y:225
    },
    laying_right: {
        x:980, y:380
    },
    laying_bottom: {
        x:805, y:585
    },
    standing_top_left: {
        x:875, y:235
    },
    standing_top_right: {
        x:1055, y:245
    },
    standing_bottom_left: {
        x:890, y:600
    },
    standing_bottom_right: {
        x:1015, y:540
    }
}
if WinActive(runelite_window)
    Tooltip("Blackjacking On", 0, 0, 9)

target_is_standing_up()
{
    if ((pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + 30, target_coord.standing_top_left.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_top_left.x, target_coord.standing_top_left.y, target_coord.standing_top_left.x + 30, target_coord.standing_top_left.y + 30, enemy_color_dark))
        && (pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + 30, target_coord.standing_top_right.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_top_right.x, target_coord.standing_top_right.y, target_coord.standing_top_right.x + 30, target_coord.standing_top_right.y + 30, enemy_color_dark))
        && (pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + 30, target_coord.standing_bottom_left.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_bottom_left.x, target_coord.standing_bottom_left.y, target_coord.standing_bottom_left.x + 30, target_coord.standing_bottom_left.y + 30, enemy_color_dark))
        && (pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + 30, target_coord.standing_bottom_right.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.standing_bottom_right.x, target_coord.standing_bottom_right.y, target_coord.standing_bottom_right.x + 30, target_coord.standing_bottom_right.y + 30, enemy_color_dark)))
        return true
    ; Otherwise the target is not standing up or is in another area of the screen
    return false
}


target_is_laying_down()
{
    ; If the bottom 4 searches result in true, true, true, false
    if ((pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_left.x, target_coord.laying_left.y, target_coord.laying_left.x + 30, target_coord.laying_left.y + 30, enemy_color_dark))
        && (pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_middle.x, target_coord.laying_middle.y, target_coord.laying_middle.x + 30, target_coord.laying_middle.y + 30, enemy_color_dark))
        && (pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_right.x, target_coord.laying_right.y, target_coord.laying_right.x + 30, target_coord.laying_right.y + 30, enemy_color_dark))
        && (pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, enemy_color)
        || pixel_search_and_click(target_coord.laying_bottom.x, target_coord.laying_bottom.y, target_coord.laying_bottom.x + 30, target_coord.laying_bottom.y + 30, enemy_color_dark)))
    {
        ; The target is laying down
        return true
    }
    ; Otherwise the target is not laying down or is in another area of the screen
    return false
}

main()
{
    ;While we have lobsters
    {
        ;if health_is_okay()
        {
            
            
            
        }
        ;else
        {
            ; Try to eat a lobster
            ;if eat_lobster()
            
        }
    }
}



F1::
{  
iteration := 0
Start:
iteration++
if WinActive(runelite_window)
{
    ;1. Check if health is okay
    if (!health_is_okay())
    {
        ToolTip("Health is not okay...!", tooltip_x, 500, 2)
        if (eat_lobster())
        {
            ToolTip("Eating lobster...", tooltip_x, 500, 2)
            ;click_money_bag()
            ;TODO: clarify why we are sleeping
            sleep_random(1800, 8500) 
            ;TODO: HERE we need to check if we are in combat
            Goto("Start")
        }
        else
        {
            MsgBox("Reload your inventory with lobsters!")
            return
        }
    }
    ToolTip("You are healthy...", tooltip_x, 500, 2)

    ;2. Initial knockout of bandit
Knockout:
    if(right_click_bandit())
    {
        sleep_random(200, 255)
        click_knockout()
    }
    else{
        Goto("Knockout")
    }
    right_click_bandit()
    sleep_random(205, 215)
    click_pickpocket()
    sleep_random(45, 50)
    ;3a. If the knockout resulted in a glancing blow.
    if(was_glancing_blow())
    {   ;4a. Retaliate with another knockout + pickpocket.
        ToolTip("Glancing blow - retaliate!", tooltip_x, tooltip_y, 1)
        Goto Knockout
    }
    ;3b. If the knockout was a success, the bandit is now unconscious.
    else if(is_unconscious())
    {   ;4b. Pickpocket twice.
        ToolTip("Is unconscious - pickpocket twice", tooltip_x, tooltip_y, 1)
        right_click_bandit()
        click_pickpocket()
    }
    else
    {
        ToolTip("Not unconscious or glancing blow`rwaiting 5 seconds", tooltip_x, tooltip_y, 1)
        sleep_random(4000, 6000)
    }
    ToolTip(iteration ". Finished--starting over", tooltip_x, 600, 3)
    Goto("Start")
}
return
}  

+F1::Reload()

^F2::ExitApp()


click_knockout()
{
    MouseGetPos(&x, &y)
    search_x1 := x - 130
    search_y1 := y
    search_x2 := x + 120
    search_y2 := y + 255
    
    counter := num_of_tries
    while (counter > 0)
    {
        if (!exists("menu", knockout_option))
        {
            sleep_random(10, 20)
        }
        else
        {
            image_search_and_click_v2(search_x1, search_y1, search_x2, search_y2, knockout_option, "left", "option")
            return true
        }
        counter--
    }
    ;ToolTip, clicking knockout was false, 300, 300, 5
    return false
}

click_pickpocket()
{
    MouseGetPos(&x, &y)
    search_x1 := x - 130
    search_y1 := y
    search_x2 := x + 120
    search_y2 := y + 255
    
    counter := num_of_tries
    while (counter > 0)
    {
        if (!exists("menu", pickpocket_option))
        {   
            sleep_random(10, 20)
        }
        else
        {
            image_search_and_click_v2(search_x1, search_y1, search_x2, search_y2, pickpocket_option, "left", "option")
            return true
        }
        counter--
    }
    return false
}

;searches in a square area around the player and expands the search area until an image is found or we are off screen.
right_click_bandit()
{
    Loop 10
    {
        if WinActive(runelite_window)
        {
            ; First check if the right click option is already active
            if (ImageExists(knockout_option) || ImageExists(pickpocket_option))
            {
                return true
            }
            ;how many pixels to expand the search area each iteration
            expansion_integer := 50
            menu_offset := 140
            ;Random, offset_x, 200, 700
            ;Random, offset_y, 200, 700
            ;center of screen, only character is enclosed
            x1 := 925
            y1 := 515
            x2 := 950
            y2 := 540
            
            while (x2 <= A_ScreenWidth and y2 <= A_ScreenHeight)
            {
                ;ToolTip, in while %count%: `r%x1%x%y1%'r%x2%x%y2% `rPixel:%enemy_color%, %tooltip_x%, %tooltip_y%, 2
                if pixel_search_and_click(x1, y1, x2, y2, enemy_color, "mouseover")
                {
                    if ImageExists(attack_menaphite_hovering_text)
                    {
                        sleep_random(30,50)
                        Click("Right Down")
                        sleep_random(160,250)
                        Click("Right Up")
                        return true
                    }
                }
                else    ;grow search area
                {
                    x1 -= expansion_integer
                    y1 -= expansion_integer
                    x2 += expansion_integer
                    y2 += expansion_integer
                }
                sleep_random(190,280)
            }
        }
    }
    return false


}

;TODO: NOT TESTED WITH MENU OPEN
click_money_bag()
{
    ;ensure bag is open
    open_bag(coord.bag.x1,coord.bag.y1,coord.bag.x2,coord.bag.y2)
    sleep_random(10, 100)
    if(image_search_and_click_v2(coord.bag.x1, coord.bag.y1, coord.bag.x2, coord.bag.y2, money_bag, "left", "item"))
        return true
    return false
}

eat_lobster()
{        
    open_bag(coord.bag.x1,coord.bag.y1,coord.bag.x2,coord.bag.y2)
    sleep_random(100, 1000)
    if(image_search_and_click_v2(coord.bag.x1, coord.bag.y1, coord.bag.x2, coord.bag.y2, lobster_cooked, "left", "item"))
       return true
    return false
}

health_is_okay()
{
    if ImageExists(healthbar, 1400, 820, 1700, 850)
        return true
    return false
}

was_glancing_blow()
{
    if (exists("chat", glancing_blow))
        return true
    return false
}

is_unconscious()
{
    if(exists("chat", unconscious))
        return true
    return false
}

exists(image_area, image_url)
{
    ;options in the top left are good for verification before an action.  
    switch image_area
    {
        case "top_left":
            return image_search_and_click_v2(coord.top_left.x1, coord.top_left.y1, coord.top_left.x2, coord.top_left.y2, image_url, 0, 0)

        case "chat":    ; use coordinates relative to chat window area
            return image_search_and_click_v2(coord.bag.x1, coord.bag.y1, coord.bag.x2, coord.bag.y2, image_url, 0, 0)
        
        default:    ; default to "middle" of screen coordinates 
            return image_search_and_click_v2(coord.middle.x1, coord.middle.y1, coord.middle.x2, coord.middle.y2, image_url, 0, 0)
    }
    
    return image_search_and_click_v2(0, 0, A_ScreenWidth, A_ScreenHeight, image_url, 0, 0)

}  
    


;Search for an image and click on it. If modifier = "right", "right" click,
;    "mouseover" will move the mouse but doesn't click, otherwise left click.
image_search_and_click_v2(x1, y1, x2, y2, image_url, modifier, offset)
{
    abort_counter := 5
    n := 1

Retry:
    if WinActive(runelite_window)
    {
        ; delays should be randomized often
        set_random_delays()

        ; search for the image                         *40 means 40 shades away from the picture's color
        ErrorLevel := !ImageSearch(&found_x, &found_y, x1, y1, x2, y2, "*n " image_url)
        if (ErrorLevel = 2)
        {
            ToolTip("Could not conduct the search using: " x1 "x" y1 " | " x2 "x" y2 " | " image_url, 0, 100, 6)
            return false
        }
        else if (ErrorLevel = 1)
        {
            ;mouse_move_random_offset()
            abort_counter--
            if (abort_counter > 0)
            {
                n += 20
                Goto("Retry")
            }
            else
            {
                ToolTip("Retried 5 times- bot failed to find: `r" image_url "`rCoords:" x1 "x" y1 "  |  " x2 "x" y2 " `rn=" n " `rIt must be off screen or blocked.", 0, 100, 6)
                return false
            }
        }
        else
        {
            ;option refer to when you "right" click in-game, the top left of the image is 0,0
            if (offset = "option")
            {
                ;we want to move mouse to the "right" 52 to 92 pixels to click more in the center of the image
                offset_horizontal := Random(72, 98)
                ;we want to move mouse down 2 to 11 pixels to click randomly within the image
                offset_vertical := Random(3, 10)
            }
            else if (offset = "item")
            {
                offset_horizontal := Random(-10, 10)
                offset_vertical := Random(-10, 10)
            }
            else
            {
                offset_horizontal := Random(0, 0)
                offset_vertical := Random(-0, 0)
            }
            ;TrayTip,, Found: `r%image_url%`rCoords Searched:%x1%x%y1%  |  %x2%x%y2% `r Found at %found_x%x%found_y%
            offset_x := found_x + offset_horizontal
            offset_y := found_y + offset_vertical
            if (modifier = "right")
                Click(offset_x, offset_y, "Right")
            if (modifier = "mouseover")
                MouseMove(offset_x, offset_y)
            if (modifier = "doubleclick")
                Click(offset_x, offset_y, 2)
            if (modifier = "left")
                Click(offset_x, offset_y)
            ;otherwise we do not click and simply return
            return true
        }
    }
    return false
}

