# Cartoon Cartoon Summer Resort Map Viewer

![A screenshot of the map viewer](./screenshot.png)

This is a work-in-progress map viewer for the Cartoon Cartoon Summer Resort series. The games were made with Adobe Shockwave and published in the summer of 2000 on Cartoon Network's website.

## Instructions
Run the script <code>viewer.py</code> to start the viewer. Use the **arrow keys** to move between maps, and press **G** to show/hide the tile grid.

You can also pass the name of a file as a commandline argument to open that specific map, but you will not be able to scroll with the arrow keys.

## Notes
The map data files from Episode 1 can be found in the <code>maps/episode1</code> folder. It will also work with maps from other episodes (if you have them), but it currently only has the tileset from Episode 1.

You may need to install pygame to run the script. Assuming you already have python, just run <code>pip install pygame</code>.

## Credits
Thanks to tomysshadow for their Movie-Restorer-Xtra which allowed me to decompress the map data from the game file, and thanks to nosamu for the CastRipper tool which I used to export the tile graphics.