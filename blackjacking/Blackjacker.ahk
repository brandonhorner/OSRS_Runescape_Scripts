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

; these are image files used for image searching
global images := {
    attack_menaphite_hovering_text : A_WorkingDir "\image_library\blackjacking\attack_menaphite_hovering_text.png",
    lobster_cooked : A_WorkingDir "\image_library\lobster_cooked.png",
    attack : A_WorkingDir "\image_library\blackjacking\attack_top_left.bmp",
    failed_pickpocket : A_WorkingDir "\image_library\blackjacking\failed_pickpocket.bmp",
    glancing_blow : A_WorkingDir "\image_library\blackjacking\glancing_blow.bmp",
    knockout_option : A_WorkingDir "\image_library\blackjacking\knockout_option.bmp",
    pickpocket_option : A_WorkingDir "\image_library\blackjacking\pickpocket_option.bmp",
    right_click_options : A_WorkingDir "\image_library\blackjacking\right_click_options.png",
    unconscious : A_WorkingDir "\image_library\blackjacking\unconscious.png",
    cannot_knockout : A_WorkingDir "\image_library\blackjacking\cannot_do_that.bmp",
    healthbar : A_WorkingDir "\image_library\blackjacking\healthbar.bmp",
    stunned : A_WorkingDir "\image_library\blackjacking\stunned.bmp",
    imstunned : A_WorkingDir "\image_library\blackjacking\imstunned.png",
    missed_right_click : A_WorkingDir "\image_library\blackjacking\missed_right_click.bmp",
    combat : A_WorkingDir "\image_library\blackjacking\combat.bmp",
    money_bag : A_WorkingDir "\image_library\blackjacking\money_bag.png",
    open_bag : A_WorkingDir "\image_library\open_bag.bmp"
}

; this is the name of the window, if the script isn't working it's because you need to change this to your name.
global runelite_window := "RuneLite - BinaryBilly"

; some tooltip coords
global tooltip_x := 600
global tooltip_y := 550

; object that holds all of the screen area coordinates
global coord := {
    chat:       { x1: 3, y1: 969, x2: 494, y2: 986 },
    bag:        { x1:1385, y1:700, x2:1855, y2:1000 },
    top_left:   { x1:0, y1:22, x2:190, y2:75 },
    middle:     { x1:0, y1:200, x2:1650, y2:970 },
    health:     { x1:1400, y1:820, x2:1700, y2:850 }
}

; coords to ensure an NPC's orientation
; add more vertices to these :o
global target_coord := {
    laying_left:    { x:745, y:330 },
    laying_middle:  { x:890, y:225 },
    laying_right:   { x:1030, y:380 },
    laying_bottom:  { x:805, y:600 },
    laying_left_2:    { x:824, y:330 },
    laying_middle_2:  { x:965, y:225 },
    laying_right_2:   { x:1105, y:375 },
    laying_bottom_2:  { x:890, y:600 },
    standing_top_left:      { x:805, y:240 },
    standing_top_right:     { x:975, y:245 },
    standing_bottom_left:   { x:805, y:600 },
    standing_bottom_right:  { x:940, y:535 },
    standing_top_left_2:        { x:885, y:245 },
    standing_top_right_2:       { x:1055, y:245 },
    standing_bottom_left_2:     { x:890, y:600 },
    standing_bottom_right_2:    { x:1030, y:530 }
}

; these are the colors of outlines around enemy NPCs
global enemy_color := 0xA4FF00
global enemy_color_dark := 0x84CD00
global tick_color := 0x00DFDF
global tick_color2 := 0x1580AD
global tick_color3 := 0x01E0E1

F1::main()

+F1::Reload()

^F2::ExitApp()
Main()
{
    while (true)
    {
        
    }  
}
Main_old()
{
    while (true)
    {
        ; Set all states to inactive
        for state, data in states {
            data.active := false
        }
        
        ; Get the current states from chat image
        currentActiveStates := GetActiveStates()
        if !currentActiveStates
        {
            ToolTip "Continuing..." 900, 100, 6
            continue
        }
        ; Update state data based on current states
        for state in currentActiveStates {
            states[state]["active"] := true
        }

        nextState := "None"
        ; Find the highest-priority active state
        highestPriority := 100 ; Start with a high number
        for state in states {
            data := states[state]
            if (data["active"] && data["priority"] < highestPriority) {
                ToolTip ("highest priority state: " state, 100, 300, 9)
                highestPriority := data["priority"]
                nextState := state
            }
        }
        if (nextState = "None")
        {
            sleep_random(10, 20)
            continue
        }
        ; Perform action for the highest-priority active state
        if (nextState = "stunned") 
        {
            ; Perform action for stunned state
            sleep_random(4000,6000)
        }
        else if (nextState = "low_health")
        {
            if (!EatLobster())
            {
                MsgBox "Restock your lobsters - punkass"
            }
        }
        else if (nextState = "pickpocket_attempt") 
        {
            ; Perform action for pickpocket_attempt state
            PickpocketAttempt()
        } 
        else if (nextState = "pickpocket_success") 
        {
            ; Perform action for pickpocket_success state
            PickpocketSuccess()
        } 
        else if (nextState = "pickpocket_failure") 
        {
            ; Perform action for pickpocket_failure state
            PickpocketFailure()
        } 
        else if (nextState = "knockout_success") 
        {
            ; Perform action for knockout_success state
            KnockoutSuccess()
        } 
        else if (nextState = "knockout_failure") 
        {
            ; Perform action for knockout_failure state
            KnockoutFailure()
        }


        Sleep 10 ; Wait 10 ms before checking chat again
    }
}

; Define an object to store state data (this needs to be an associative + Map array because objects aren't iterable :\)
; Ex: isactive := states["stunned"]["active"]
global states := Map(
    "stunned", Map("active", false, "priority", 7, "image_url", A_WorkingDir "\image_library\been_stunned.bmp"),
    "low_health", Map("active", false, "priority", 6, "image_url", A_WorkingDir "\image_library\healthbar.bmp"),
    "pickpocket_attempt", Map("active", false, "priority", 5, "image_url", A_WorkingDir "\image_library\pickpocket_attempt.bmp"),
    "pickpocket_success", Map("active", false, "priority", 4, "image_url", A_WorkingDir "\image_library\pickpocket_success.bmp"),
    "pickpocket_failure", Map("active", false, "priority", 3, "image_url", A_WorkingDir "\image_library\pickpocket_failure.bmp"),
    "knockout_success", Map("active", false, "priority", 2, "image_url", A_WorkingDir "\image_library\knockout_success.bmp"),
    "knockout_failure", Map("active", false, "priority", 1, "image_url", A_WorkingDir "\image_library\knockout_failure.bmp")
)

GetActiveStates()
{
    ; Define an array to store the active states
    activeStates := []

    ; Iterate over the states
    for state, data in states {
        ToolTip "State: " state " priority " data["priority"], 100, 800, 4
        if (state = "low_health")
        {
            if ImageExists(data["image_url"], coord.health.x1, coord.health.y1, coord.health.x2, coord.health.y2)
                ToolTip "Health wasn't missing: image_url: " data["image_url"], 100, 200, 2
            else
            {
                activeStates.push(state)
                ToolTip "Found image_url: " data["image_url"], 100, 100, 1
                sleep_random(500,1500)
            }
        }
        else
        {
            ; If the image for the current state is found, add the state to the activeStates array
            if ImageExists(data["image_url"], coord.chat.x1, coord.chat.y1, coord.chat.x2, coord.chat.y2)
            {
                activeStates.push(state)
                ToolTip "Found image_url: " data["image_url"], 100, 100, 1
                sleep_random(500,1500)
            }
            else
                ToolTip "Didn't Find: image_url: " data["image_url"], 100, 200, 2
        }
    }
    
    ; Return the array of active states
    return activeStates
}
; ToolTip "Found image_url: " data["image_url"], 100, 100, 1
IAmStunned()
{
    ToolTip "Stunned: Waiting.. ", 1200, 900, 5
    while(!ImageExists(images.imstunned))
    {
        sleep_random(10, 10)
    }
    ToolTip "Stunned", 1200, 900, 5
}

; If the pickpocket attempt is still on the screen, we just want to wait a little before pick pocketing
PickpocketAttempt()
{
    ToolTip "Pickpocket Attempt: Waiting.. ", 1200, 900, 5

    RightClickNPC() ; ensure right click menu is open

    while(ImageExists(states["pickpocket_attempt"]["image_url"]))
    {
        sleep_random(10, 10)
    }
}

PickpocketSuccess()
{
    ToolTip "Pickpocket Success: Waiting.. ", 1200, 900, 5
    while(ImageExists(states["pickpocket_success"]["image_url"]))
    {
        sleep_random(10, 10)
    }
}

PickpocketFailure()
{
    KnockoutSuccess()
}

KnockoutSuccess()
{
    RightClickNPC()
    sleep_random(30, 50)
    ClickPickpocket()
}

KnockoutFailure()
{
    KnockoutSuccess()
}

WaitForTick()
{
    if WaitForPixel(1697, 117, 1701, 123, tick_color)
        return true
    return false
}

; the right click menu in the game is open, now we left click the knockout option
ClickKnockout()
{
    offset := GetMousePosOffsets()

    if image_search_and_click(images.knockout_option, 0, "left", "option", offset.x1, offset.y1, offset.x2, offset.y2)
       return true
    return false
}

; the right click menu in the game is open, and we either just knocked them out, or it was a glancing blow and they are
;   about to attack. To counteract their attack, we can click pickpocket on them.
ClickPickpocket()
{
    offset := GetMousePosOffsets()

    if image_search_and_click(images.pickpocket_option, 0, "left", "option", offset.x1, offset.y1, offset.x2, offset.y2) {
        ; Store the current tick count
        startTime := A_TickCount

        ; Keep checking until 400ms have passed
        while (A_TickCount - startTime) < 400 {
            ; Check for the image
            if ImageExists(states["pickpocket_attempt"]["image_url"]) {
                return true
            }
            ; Sleep for a short period to not hog the CPU
            Sleep 10
        }

        ; If we've reached here, 400ms have passed without detecting the image
        return false
    }
    return false
}

CheckForKnockoutToDoublePickpocket()
{
    ; Store the current tick count
    startTime := A_TickCount

    ; Keep checking until 400ms have passed
    while (A_TickCount - startTime) < 400 {
        ; Check for the image
        if ImageExists(images.["pickpocket_attempt"]["image_url"]) {
            return true
        }
        ; Sleep for a short period to not hog the CPU
        Sleep 10
    }

    ; If we've reached here, 400ms have passed without detecting the image
    return false
}

; searches in a square area around the player and expands the search area until an image is found or we are off screen.
RightClickNPC_old()
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

; right clicks around the chest area of the NPC
RightClickNPC()
{
    if (ImageExists(images.right_click_options))
        return true
    ; clicks need to be fast (but not instant), we'll add sleeps when necessary
    SetDefaultMouseSpeed(1)

    ; Get the target click area
    click_area := GetTargetClickArea()
    offset_x := Random(-40, 40)
    offset_y := Random(-30, 30)

    ; Randomize within the area and right click
    ToolTip("Right Clicking:`roffset x:" offset_x ", y:" offset_y "`rx:" click_area.x ", y:" click_area.y, 100, 1000, 6)
    x := click_area.x + offset_x
    y := click_area.y + offset_y
    MouseMove(x, y)
    sleep_random(10,20)
    ; If target is in sight
    if ImageExists(images.attack_menaphite_hovering_text) {
        Click("Right")
        return true
    }
    return false
}

; click the money bag in your inventory
 ClickMoneyBag()
{
    ;ensure bag is open
    if ImageExists(images.open_bag) {
        sleep_random(10, 100)
        if image_search_and_click(images.open_bag, "whole_screen", "left", "item2")
            return true
    }
    return false
}

; click the first availableb lobster in your inventory
EatLobster()
{        
    open_bag()
    sleep_random(100, 1000)
    ; ToolTip("Searching coord.bag: " coord.bag.x1 coord.bag.y1 coord.bag.x2 coord.bag.y2 "`r" images.lobster_cooked, 900, 900, 2)
    if image_search_and_click(images.lobster_cooked, "whole_screen", "left", "item2")
       return true
    return false
}

HealthIsOkay()
{
    if ImageExists(images.healthbar, 1400, 820, 1700, 850)
        return true
    return false
}

WasGlancingBlow()
{
    if (exists("chat", images.glancing_blow))
        return true
    return false
}

IsUnconscious()
{
    if ImageExists(images.unconscious, 231, 970, 390, 990)
        return true
    return false
}