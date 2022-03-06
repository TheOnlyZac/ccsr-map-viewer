# Cartoon Cartoon Summer Resort Map Viewer
# by TheOnlyZac

import sys
import json
import re
try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
except:
    print("Pygame not found. Please install it with 'pip insall pygame'.")
    sys.exit()

(screenWidth, screenHeight) = (416, 320)
bgcolor = (200, 200, 200)

# Opens map data file and converts the map data to json
def processMapData(data):
    # remove all newlines from file
    data = data.replace("\n", "")

    # swap []s and {}s
    data = data.replace('[', '{')
    data = data.replace(']', '}')

    # iterate over data to convert {}s back to []s for list attributes
    s = ""
    depth = 0
    inList = False
    inString = False
    for i,char in enumerate(data):
        if char == ',':
            s = ""
            continue

        if char == '"':
            inString = not inString

        if inList and s == "#COND:" and not char in [' ', '{']:
            inList = False

        s += char
        if not inString:
            s = s.strip()

        if inList:
            if char == '{':
                if depth == 0:
                    data = data[:i] + '[' + data[i + 1:]
                depth += 1
            if char == '}':
                depth -= 1
                if depth == 0:
                    data = data[:i] + ']' + data[i + 1:]
                    inList = False
        else:
            if s in ["#location", "#COND", "#message"]:
                depth = 0
                inList = True

    # iterate over file again and remove all extra whitespace
    json = ""
    inString = False
    for i,char in enumerate(data):
        json += char

        if char == '"':
            inString = not inString

        if not inString:
            json = json.strip()
    
    # use regex to add quotes around all necessary fields (all of which are prefixed with #)
    json = re.sub(r'([#]{1}\w+)', r'"\1"', json)

    return json


# Reads the given map data and separate each tile into it's own string in an array
def separateTileStrings(data):

    data = data[slice(1, -1)] # remove bounding {} around whole file

    s = ""
    depth = 0
    tiles = []
    for char in data:
        if depth == 0 and char == ',':
            continue
        s += char
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                tiles.append(s)
                s = ""
    
    return tiles


# Reads each tile string in the given data and convert it to a dict using json.loads
def jsonLoadTileData(data):
    tiles = []
    for tile in data:
        try:
            tiles.append(json.loads(tile.__str__()))
        except:
            continue

    return tiles


def convertWhiteToAlpha(surface):
    # replace white pixels with transparent
    arr = pygame.PixelArray(surface)
    arr.replace((255, 255, 255), (255, 255, 255, 0))
    del arr


def drawTiles(screen, tileData, renderInvis=False):
    # clear screen
    bgcolor = (255, 255, 255) # white
    screen.fill(bgcolor)

    # draw each tile
    for tile in tileData:
        try:
            (x, y, tileWidth, tileHeight) = (tile["#location"][0], tile["#location"][1],
                                            tile["#width"], tile["#height"])

            # skip tile if it is invisible when the game starts
            if (not renderInvis) and (tile["#data"]["#item"]["#visi"]["#visiObj"] != "" or tile["#data"]["#item"]["#visi"]["#visiAct"] != ""):
                continue

            spriteSurface = pygame.Surface((tileWidth, tileHeight), pygame.SRCALPHA)

            sprite = None
            try:
                # load sprite image
                sprite = pygame.image.load('tiles/episode1/' + tile["#member"] + '.png')
            except:
                pass

            # if sprite is missing, draw red box and continue
            if sprite == None:
                rect = (0, 0, tileWidth, tileHeight)
                color = (255, 32, 32, 255) # red
                pygame.draw.rect(spriteSurface, color, rect)
                screen.blit(spriteSurface, (16*x, 16*y))
                continue
            
            # draw sprite as tile
            if "tile" in tile["#member"] or "Tile" in tile["#member"]:
                for i in list(range(round(tileWidth/32))):
                    for j in list(range(round(tileHeight/32))):
                            spriteSurface.blit(sprite, (i*32, j*32))
                convertWhiteToAlpha(spriteSurface)
                screen.blit(spriteSurface, (16*x, 16*y))
                continue
            
            # draw sprite as block
            spriteSurface.blit(sprite, (0, 0))
            convertWhiteToAlpha(spriteSurface)
            screen.blit(spriteSurface, (16*x - 16, 16*y - 16))
            
        except:
            continue


def openMapFile(filename):
    # open map data file
    file = open(filename, "r")
    processedFile = processMapData(file.read())
    tileStrings = separateTileStrings(processedFile)
    tileData = jsonLoadTileData(tileStrings)
    file.close()
    return tileData


def main():
    print("\nCartoon Cartoon Summer Resort Map Viewer\nby TheOnlyZac (v0.4.0)\n")
    argc = len(sys.argv)
    argv = sys.argv
    mode = "default"
    showInvis = False

    # Check if a file was passed as an argument
    if (argc > 1):
        mode = "file"
    
    # Open map data file
    mapFile = None
    (col, row) = 1, 6
    
    if mode == "default":
        mapFile = "maps/episode1/0{}0{}.txt".format(col, row)
    elif mode == "file":
        mapFile = sys.argv[1]

    tileData = openMapFile(mapFile)

    # Init pygame
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Cartoon Cartoon Summer Resort Map Viewer")

    icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    icon.blit(pygame.image.load("tiles/gus.png"), (0, 0))
    convertWhiteToAlpha(icon)
    pygame.display.set_icon(icon)

    grid = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA) # create grid surface with opacity
    showGrid = False

    pygame.mixer.init()
    snapSound = pygame.mixer.Sound("resources/snap.ogg")

    # Main render loop
    running = True
    while running:
        # clear screen and render the current tileData
        screen.fill(bgcolor)
        drawTiles(screen, tileData, showInvis)

        # draw grid over the screen if showGrid is true
        if showGrid:
            for i in list(range(round(screenWidth/32))): # draw gridlines to surface
                pygame.draw.line(grid, (0, 0, 0, 64), (32*i, 0), (32*i, screenHeight))
                for j in list(range(round(screenHeight/32))):
                    pygame.draw.line(grid, (0, 0, 0, 64), (0, 32*j), (screenWidth, 32*j))
            screen.blit(grid, (0,0)) # draw grid surface to screen

        # flip the display
        pygame.display.flip()

        # handle pygame events
        for event in pygame.event.get():
            # handle pygame window closed
            if event.type == pygame.QUIT:
                running = False
            
            # handle keyboard input
            if event.type == pygame.KEYDOWN:
                (oldCol, oldRow) = (col, row)

                # ARROW KEYS: move between maps
                if event.key == pygame.K_LEFT:
                    if col > 1: col -= 1
                # go right
                elif event.key == pygame.K_RIGHT:
                    if col < 6: col += 1
                # go up
                elif event.key == pygame.K_UP:
                    if row > 1: row -= 1
                # go down
                elif event.key == pygame.K_DOWN:
                    if row < 6: row += 1

                # G: show/hide grid
                elif event.key == pygame.K_g:
                    showGrid = not showGrid

                # C: capture snapshot of current map
                elif event.key == pygame.K_c:
                    # play snapshot sound
                    pygame.mixer.Sound.play(snapSound)

                    # make sure snaps folder exists
                    if not os.path.exists("./snaps"):
                        os.mkdir("snaps")
                    mapName = os.path.splitext(os.path.basename(mapFile))[0]
                    
                    # save each snap of the same map with an increasing suffix
                    i = 1
                    while os.path.exists("./snaps/{}_{}.png".format(mapName, i)):
                        i+= 1

                    pygame.image.save(screen, "snaps/{}_{}.png".format(mapName, i))
                
                # V: toggle showing invisible tiles
                elif event.key == pygame.K_v:
                    showInvis = not showInvis

                # open new map data file if the col or row changed
                if mode == "default" and (col, row) != (oldCol, oldRow):
                    mapFile = "maps/episode1/0{}0{}.txt".format(col, row)
                    tileData = openMapFile(mapFile)
    
    print("We hope you enjoyed your stay!")
    return

if __name__ == "__main__":
    main()