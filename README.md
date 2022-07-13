# stickySample
Nuke command to save a RGB sample value on a stickyNote

Autor: Jorge Hernandez

Web: https://www.linkedin.com/in/jorgehi-vfx/

## Installation

The way you can use this command is storing the stickySample.py in a directory that is been reading by nuke and adding this line in your menu.py

nuke.menu("Nodes").addCommand("Actions/SampleOnSticky", "import stickySample;stickySample.sampleOnSticky()", 'alt+a')

You can change the shotcut if your prefer other than alt+a.

If you don´t know how to do this, here i let you a basic instalation steps:

1. Go to this path C:\Users\\[username]\\.nuke where username is your windows username.
2. If you don´t have a menu.py file here, create it with a basic text editor.
3. In your menu.py file add these lines:
import nuke
nuke.menu("Nodes").addCommand("Actions/SampleOnSticky", "import stickySample;stickySample.sampleOnSticky()", 'alt+a')
4. Add the stickySample.py file in this path C:\Users\[username]\.nuke\stickySample.py
5. Open Nuke, now you can use alt+a like command to store your viewer samples.

## Known issues

The sample funtion that provides the Nuke api for python and TCL don't have the same accuracy level than the internal method used in the official Nuke Viewport. So when you sample medium or large areas the result value can be diferent in the last decimals. I'm looking for other method to solve this problem.
