---v1.0.2 MOD v1.0.0.0---
This version is "v1.0.2 MOD v1.0.0.0", the same as version v1.0.2. The difference is that it is made to be working on Windows 10 with few new features.
It was decompiled, modified and then recompiled. Called it "v1.0.2 MOD v1.0.0.0" to differentiate it from other version in the future and NOT confuse people.

FIXES:
1. Runs on Windows 10. Not crashing before it lunches like it does before. (Why you are most likely here)

2.MOSAIC -> Granite 1A->Giallo Veneziano was crashing VMPPMaya.
MOSAIC -> Granite 1A->Baltic Brown is NOT implemented officially by SIGER STUDIO resulting in "Giallo Veneziano" crashing when selected due to out of bound array exception.
I implemented it after digging through the maps to see which one it uses. Baltic Brown uses 5_2_2_d.jpg. I used the Almond Cream code to create it. Baltic Brown works now.

3.App not opening in a position that displays the whole GUI. 
Reduced the width and the height of the App then made it to be opening the middle of the screen. 
Alt+Space then left,up,down or right arrow WAS required to move the Apps screen to the right position. Not anymore. 

4.No longer required to restart VMPPMaya when Port Number or VMPP Maps Directory Location is changed for it to take effect. 

NEW FEATURES:
1.Instead of Exception being thrown when Maya port is NOT open, the user is given steps to open port in Maya.

2.Blinks green once if Material is successfully sent to Maya.

3.Blinks red twice if Material failed to send followed by feature 1 action.

4.Clicking on the Selected image on the right will enlarge it just like the tiny official button under it.
(Much more easier to click on than using the tiny official button to enlarge the image)

5.Hold SHIFT key, the "TO HYPERSHADE" button will change to "INSTALL SHELF/ICON". Click on the new  "INSTALL SHELF/ICON"
button. It should install the VMPPMaya Shelf/Icon to any Version of Maya installed. You should get a confirmation message when finished.
This should add VMPPMaya Shelf/Icon to the Maya Custom shelf and make easier to start the server just by one click.

6.Hold CONTROL key, the "TO HYPERSHADE" button will change to "REMOVE SHELF/ICON". Click on the new  "REMOVE SHELF/ICON"
button. It should uninstall/remove all VMPPMaya Shelf/Icon from all Maya version installed. You should get a confirmation message when finished.
This should Remove VMPPMaya Shelf/Icon from the Maya Custom shelf and make it easier to uninstall the Shelft from all Maya version just by doing this.

7. Hold 'D' key, the "TO HYPERSHADE" button will change to "ADD HDR DOME LIGHT". Click on the new  "ADD HDR DOME LIGHT" to add
a Dome Light to the scene. This will add Dome Light attached with HDR Image to the scene. (This was added to make test rendering faster).
The hdr is located at \img\hdr\austria.hdr. 
You can grab any HDR image online, rename it to austria.hdr then put it at \img\hdr to change it's default hdr image but the included one should be fine.



MISC FEATURES:
1. Allow clicking on the VMPPMaya Icon on the taskbar to minimize it.(Saves time than clicking on the tiny minimize icon while switching 
between VMPPMaya and Maya)

Known Problems:
1. Text on the Slider such as (Icon Size, 150, 125,100,75,50) are NOT displaying but they do not affect the App functionality.
The slider itself displays.

Thanks to Innonee