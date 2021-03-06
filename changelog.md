# Changelog
Cartoon Cartoon Summer Resort Map Viewer
by TheOnlyZac

## v0.5
March 7 2022
* Added episodes 2, 3, and 4 maps
* Added episode select when you start the script
* Implemented changing between episodes with number keys
* Added sound effects for:
 * Showing invisible objects
 * Changing between episodes
 * Map loading errors

## v0.4
March 5 2022
* Press C to capture a snapshot of the map
* Press V to show/hide invisible tiles
* Viewer now works on Windows 7 using Python 3.8
* If pygame is not detected it will ask you to install it

## v0.3
March 5, 2022
* Sprites now render with transparency
* Added window title and icon

## v0.2
March 5, 2022
* Use the arrow keys to move between maps
* Press G to toggle the grid overlay
* Missing sprites render as red boxes
* JSON parser will skip tiles if they throw an error
* Fixed some filenames and bad data in map 0106

## v0.1
March 4, 2022
* First implementation of map renderer
* Maps 0106, 0106b, 0306, 0502, and 0506b throw an error when parsing tile JSON 