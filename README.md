Hello, these are Pixel/Image Bots for OSRS (RuneLite client). Do not try any of these scripts without supervising the first few times for bad loops. Most of these scripts are probably broken or lack proper pre-req information but try going back to a previous commit (one where it says, "it's working great!"). You may be better off starting over with a clean structure :P

Pre-requisites for scripts before <2023 are likely to be AutoHotkey (AHK) V1 and for 2024 and beyond AHK V2 is used.

For later 2024 into 2025 we had the advent of smarter LLMs and I started making Python bots because there is a lot more training data on how Python works versus AHK.

If you use some of the Python scripts, obv you'll need Python 3+
  + I implemented OCR (Tesseract) in some scripts which you'll have to install and point to in scripts (if ya get an error)
  + I use OpenCV for image detection (you probably have to pip install it)
  + There are several other dependencies that I probably installed but you'll know when you try to run code :)

Most every (non utilities) script will have a line pointing to the window title (oughtta switch this to a config file read). This window title can be found with AutoHotkey Window Spy tool which comes with AHK, however you likely just need to replace your character's name.

Most every script will utilize highlighted tiles on the game world.
