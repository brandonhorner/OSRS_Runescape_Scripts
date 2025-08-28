;THERE IS AN UPDATED VERSION
;REQUIRED:
; Runelite client, change your name in the window names in the code below.
; Runelite client must have the options open (of some sort).
; This was made on a 1920 x 1080 screen size. (In Windows)
; Have a lobster pot in your 2nd bank inventory space, turn on "Always set placeholders"
; Have your chat turned to "Game" Chat, Public chat will currently mess up one function.


#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%\..  ; Ensures a consistent starting directory.

CoordMode, Pixel, Screen    ; Starts pixel search at top left of ACTUAL SCREEN, delete if you want to search from top left of WINDOW
CoordMode, Mouse, Screen

global bank_inventory_x1 := 450
global bank_inventory_y1 := 50
global bank_inventory_x2 := 1060
global bank_inventory_y2 := 850

global bank_deposit_all_items := "image_library\bank_deposit_all_items.bmp"
global lobster_pot := "image_library\lobster_pot.bmp"

SetMouseDelay, 80

^+`::
{
    resetCharacter()
    catchLobsters()
    return
}

findStarfish( ByRef x, ByRef y )
{
    ; unique color of starfish on beach...
    starfish_color := 0xDC884E   
    starfish_color2 := 0xA5663C
    
    ; start by searching for the starfish.
    PixelSearch, x1, y1, 0, 0, A_ScreenWidth, A_ScreenHeight, %starfish_color%, 1, RGB Fast
    PixelSearch, x2, y2, 0, 0, A_ScreenWidth, A_ScreenHeight, %starfish_color2%, 2, RGB Fast

    ; if we see the starfish, return x,y coordinates
    if ( x1 )  
    {
        x := x1
        y := y1
        TrayTip,, findStarfish() was true`nif(x1):%x% %y%, 1
        return true
    }
    else if ( x2 )
    {
        x := x2
        y := y2
        
        TrayTip,, findStarfish() was true`nif(x2):%x% %y%, 1
        return true
    }
    else
    {
        TrayTip,, findStarfish() was false, 1
        return false
    }
}


resetCharacter()
{
    IfWinActive, RuneLite - BinaryBilly 
    {
        ; if we find the starfish
        if ( findStarfish( x, y ) )
        {   
            clickToSpotTwo( x, y )
        }
        else
        {
            TrayTip,, I can't see the starfish from here`nmoving down and to the "right"!,1
            
            clickDownToTheRight()
            
            resetCharacter() ; try again to reset
        }
        
        ; wait to be reset!
        sleep_random( 7000, 9000 )
    }
    return
}


catchLobsters()
{
    WinActivate, RuneLite - BinaryBilly

    ;The unique color we picked is up on the lobster tail (on the sprite). In order to seem 
    ;   more human, we will randomly offset our clicks from the tail to around the sprite.
    lobster_color := 0x925424   ; a color (hopefully) unique to the lobster sprite
    
    if ( !clickLobstersInFront() )  ; if we can't click lobsters in front of us, search!
    {
        resetCharacter()
        
        ; Search Area 1, 3, 4 (Left to Right)
        PixelSearch, x1, y1, 464, 495, 714, 527, %lobster_color%, 0, RGB Fast
        PixelSearch, x3, y3, 1036, 765, 1222, 796, %lobster_color%, 0, RGB Fast
        PixelSearch, x4, y4, 1214, 655, 1366, 684, %lobster_color%, 0, RGB Fast
        
        Random, offset_horizontal, -11, 11
        Random, offset_vertical, -2, 14    
        
        if ( x1 )
        {
            offset_x1 := x1 + offset_horizontal
            offset_y1 := y1 + offset_vertical
            Click, %offset_x1%, %offset_y1%
        }
        else if ( x3 )
        {
            offset_x3 := x3 + offset_horizontal
            offset_y3 := y3 + offset_vertical
            Click, %offset_x3%, %offset_y3%
        }
        else if ( x4 )
        {
            offset_x4 := x4 + offset_horizontal
            offset_y4 := y4 + offset_vertical
            Click, %offset_x4%, %offset_y4%
        }
        else
        {
            TrayTip,, Something is wrong. `nI can't see any lobsters. `nreturning., 1
            resetCharacter()
            return
        }
    }
    ; if there are lobsters in front of us, continue to watch the spawn
    else
    {
        watchSpawn()
    }

    return
}


watchSpawn()
{
    openInventory()
    sleep_random( 7000, 15000 )
    loop, 1000
    {
        IfWinActive, RuneLite - BinaryBilly
        {
            ;Check if the color we clicked on is still in the pool in front of us.
            ;         Otherwise, the pool has moved, so check nearby or reset.
            
            sleep_random( 2450, 3650 )
            
            if ( spawnMoved() )
                catchLobsters()
            
            if( messageAppeared() )
                clickInFrontOfChar()
            
            ; check if inventory is full
            if( bagIsFull() )
            {
                clickTowardBank()
                goToBank()
                resetCharacter()
            }
            
            sleep_random( 950, 1150 )
            
            ; Every 100 times this loops, click in front of you, to stay logged in.
            value := Mod( A_Index, 10 )
            if( value = 0 )
            {
                TrayTip,, 10th iteration of watchspawn(), 1
            }
        }
    }
    return
}


; if the spawn has moved return true, otherwise false
spawnMoved()
{
    lobster_color := 0x925424
    lobster_color2 := 0x7B461D

    ; search the area below you for differing lobster colors
    PixelSearch, x, y, 808, 548, 825, 560, %lobster_color%, 10, RGB Fast
    PixelSearch, x1, y1, 808, 548, 825, 560, %lobster_color2%, 10, RGB Fast
    PixelSearch, x2, y2, 808, 548, 825, 560, %lobster_color2%, 20, RGB Fast
    
    ; if we see any of these variables with value, the spawn hasn't moved!
    if( x or x1 or x2 )
    {   
        return, false
    }
    ; otherwise return true
    return, true
}


goToBank()
{
    TrayTip,, You are full!`nreturning to bank., 1
    
    ; Walk towards the bank
    clickRandom( 300, 335, 350, 360 )
    sleep_random( 8800, 10200 )
    
    ; should be clicking bank stall
    clickRandom( 77, 328, 132, 355 )
    sleep_random( 10000, 12000 )
    
    ; click on the 'Deposit inventory' button
    image_search_and_click(bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, bank_deposit_all_items, 0)
    sleep_random( 4800, 6400 )
    
    ; click the lobster cage in bank to withdraw it again
    image_search_and_click(bank_inventory_x1, bank_inventory_y1, bank_inventory_x2, bank_inventory_y2, lobster_pot, 0)
    sleep_random( 1000, 1800 )
    
    ; leave the bank, clicking on the minimap
    clickRandom( 1620, 115, 1635, 123 )
    sleep_random( 8800, 10200 )
    
    closeInventory()
    
    ; run back in LOS of the starfish!
    clickRandom( 1615, 133, 1620, 139 )
    sleep_random( 6000, 7900 )
    
    return
}


messageAppeared()  ; What happens when you are full inventory!?
{
    message_color := 0x0000FF
    PixelSearch, x, y, 150, 977, 400, 995, %message_color%, 0, RGB Fast
    
    ; if we are full on inventory or leveled or just have a message!
    if ( ErrorLevel = 0 )
    {
        return true
    }
    return false    
}


; Checks to see if there is a lobster in the last inventory space.
bagIsFull()
{
    lobster_color := 0x925424   ; a color (hopefully) unique to the lobster sprite
    
    ; make sure lobster is in bottom "right" slot!
    PixelSearch, x, y, 1580, 960, 1616, 992, %lobster_color%, 0, RGB Fast
    
    ; if it is not full
    if( ErrorLevel >= 1 )
    {   
        return false
    }
    ; if it is full
    return true
}


openInventory()
{
    open_inventory_color := 0x3C1510
    PixelSearch, x, y, 1314, 1004, 1343, 1041, %open_inventory_color%, 2, RGB Fast
    
    if( ErrorLevel = 1 ) ; if we didn't see the open "bag" color, the "bag" is closed
    {
        ; So open the "bag"
        SendInput, {F3}
    }
    return
}


closeInventory()
{
    open_inventory_color := 0x3C1510
    PixelSearch, x, y, 1314, 1004, 1343, 1041, %open_inventory_color%, 2, RGB Fast
    
    if( ErrorLevel = 0 )
    {
        ; If we did see the open "bag" color then we close the "bag"!
        SendInput, {F3}
    }
    return
}


clickTowardBank()
{
    findStarfish( x, y )
    ; These random values are to offset to spot two
    Random, offset_horizontal, -333, -324
    Random, offset_vertical, -31, -21
    
    ; offset the values randomly to spot two
    offset_x := x + offset_horizontal
    offset_y := y + offset_vertical
    
    Click, %offset_x%, %offset_y%
    TrayTip,, Moving towards the bank!,1
    
}

clickToSpotTwo( x_coord, y_coord )
{
    ; These random values are to offset to spot two
    Random, offset_horizontal, -333, -324
    Random, offset_vertical, -31, -21
    
    ; offset the values randomly to spot two
    offset_x := x_coord + offset_horizontal
    offset_y := y_coord + offset_vertical
    
    Click, %offset_x%, %offset_y%
    TrayTip,, Moving to position 2!,1
    
    return
}

; Clicks down to the "right" of the character one or two squares
clickDownToTheRight()
{
    Random, x_pos, 840, 900
    Random, y_pos, 550, 615
    
    Click, %x_pos%, %y_pos%
    
    sleep_random( 2800, 3800 )
    
    return
}


clickInFrontOfChar()
{
    Random, x_pos, 808, 825
    Random, y_pos, 548, 560
    
    Click, %x_pos%, %y_pos% 
    
    return
}


; Searches for lobsters in front, and clicks on them, returning true, or false
;   if it is unable to find any.
clickLobstersInFront()
{
    lobster_color2 := 0x7B461D ;TODO: Fix initial bank movement
    PixelSearch, x_pos, y_pos, 715, 550, 940, 576, %lobster_color2%, 20, RGB Fast
    
    if( ErrorLevel = 0 )  ; if we see the lobster
    {
        Random, offset_horizontal, -7, 7
        Random, offset_vertical, 0, 10
      
        offset_x := x_pos + offset_horizontal
        offset_y := y_pos + offset_vertical
        
        sleep_random( 1200, 3000 )
        Click, %offset_x%, %offset_y%
        
        return, true
    }
    
    TrayTip,, clickLobstersInFront() failed...,1
    return, false
}

;Search for an image and click on it. If modifier = "right", "right" click,
;    otherwise left click.
image_search_and_click(x1, y1, x2, y2, image_url, modifier)
{
    Random, offset_horizontal, -10, 10
    Random, offset_vertical, -10, 10
    abort_counter = 3
Retry:
    IfWinActive, RuneLite - BinaryBilly
    {
        ; how fast the mouse moves should be randomized
        Random, delaySpeed, 60, 110
        SetMouseDelay, %delaySpeed%

        ; search for the image
        ImageSearch, found_x, found_y, %x1%, %y1%, %x2%, %y2%, %image_url%
        if (ErrorLevel = 2)
        {
            TrayTip,, Could not conduct the search using: %x1%- %y1%- %x2%- %y2%- %image_url%
            return
        }

        else if (ErrorLevel = 1)
        {
            ;mouse_move_random_offset()
            sleep_random(1000, 1200)
            abort_counter--
            if (abort_counter > 0)
            {
                Goto, Retry
            } 
            else
            {
                TrayTip,, Retried 3 times- bot failed to find image. `rIt must be off screen or blocked.
                return
            }
        }
        else
        {
            offset_x := found_x + offset_horizontal
            offset_y := found_y + offset_vertical
            if (modifier = "right")
                Click, right, %offset_x%, %offset_y%
            else
                Click, %offset_x%, %offset_y%
            return
        }
    }
    return
}

; ---------------------- Utilities --------------------------------------------

sleep_random( sleep_time_low, sleep_time_high )
{
    Random, sleep_time, sleep_time_low, sleep_time_high
    Sleep, %sleep_time%
    
    return
}

; Randomly clicks within the specified coordinates.
clickRandom( x1, y1, x2, y2 )
{
    Random, x, x1, x2
    Random, y, y1, y2
    
    Click, %x%, %y%
    
    return
}

+`::Reload

^`::ExitApp



