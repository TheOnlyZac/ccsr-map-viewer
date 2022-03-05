# Cartoon Cartoon Summer Resort Map Viewer
# by TheOnlyZac

import sys
import json
import re
import pygame

(screenWidth, screenHeight) = (416, 320)
bgcolor = (200, 200, 200)

# Opens map data file and converts the map data to json
def processMapDataFile(data):
    # remove all newlines from file
    data = data.replace("\n", "")

    # swap []s and {}s
    data = data.replace('[', '{')
    data = data.replace(']', '}')

    # iterate over data to convert {}s back to []s for the necessary fields
    s = ""
    depth = 0
    seeking = False
    instring = False
    for i,c in enumerate(data):
        if c == ',':
            s = ""
            continue

        if c == '"':
            instring = not instring

        if seeking and s == "#COND:" and not c in [' ', '{']:
            seeking = False

        s += c
        if not instring:
            s = s.strip()

        if seeking:
            if c == '{':
                if depth == 0:
                    data = data[:i] + '[' + data[i + 1:]
                depth += 1
            if c == '}':
                depth -= 1
                if depth == 0:
                    data = data[:i] + ']' + data[i + 1:]
                    seeking = False
        else:
            if s in ["#location", "#COND", "#message"]:
                depth = 0
                seeking = True

    # iterate over file again and remove all extra whitespace
    json = ""
    instring = False
    for i,c in enumerate(data):
        json += c

        if c == '"':
            instring = not instring

        if not instring:
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
    for i,c in enumerate(data):
        if depth == 0 and c == ',':
            continue
        s += c
        match c:
            case '{':
                depth += 1
            case '}':
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

def renderTileData(screen, tileData):
    # clear screen
    bgcolor = (255, 255, 255) # white
    screen.fill(bgcolor)

    # draw each tile
    for tile in tileData:
        try:
            (x, y, tileWidth, tileHeight) = (tile["#location"][0], tile["#location"][1],
                                            tile["#width"], tile["#height"])
            
            sprite = None
            try:
                sprite = pygame.image.load('tiles/episode1/' + tile["#member"] + '.png')
            except:
                pass

            # if sprite is missing, draw red box and continue
            if sprite == None:
                rect = (16*x, 16*y, tileWidth, tileHeight)
                color = (255, 32, 32) # red
                pygame.draw.rect(screen, color, rect)
                continue
            
            # draw sprite
            if "tile" in tile["#member"] or "Tile" in tile["#member"]:
                for i in list(range(round(tileWidth/32))):
                    for j in list(range(round(tileHeight/32))):
                            screen.blit(sprite, (16*x + i*32, 16*y + j*32))
            else:
                screen.blit(sprite, (16*x - 16, 16*y - 16))
        except:
            continue

def openMapFile(filename):
    # open map data file
    file = open(filename, "r")
    processedFile = processMapDataFile(file.read())
    tileStrings = separateTileStrings(processedFile)
    tileData = jsonLoadTileData(tileStrings)
    file.close()
    return tileData

def main():
    print("Cartoon Cartoon Summer Resort Map Viewer\nby TheOnlyZac (v0.2.0)\n")
    argc = len(sys.argv)
    argv = sys.argv
    mode = "default"

    # Check if a file was passed as an argument
    if (argc > 1):
        mode = "file"
    
    # Open map data file
    mapData = None
    (col, row) = 1, 6
    
    if mode == "default":
        mapData = openMapFile("maps/episode1/0{}0{}.txt".format(col, row))
    elif mode == "file":
        mapData = openMapFile(sys.argv[1])

    # Init pygame
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    grid = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA) # create grid surface with opacity
    showGrid = False

    running = True
    while running:
        # clear screen and render the current mapData
        screen.fill(bgcolor)
        renderTileData(screen, mapData)

        # draw grid over the whole screen
        if showGrid:
            for i in list(range(round(screenWidth/32))): # draw gridlines to surface
                pygame.draw.line(grid, (0, 0, 0, 64), (32*i, 0), (32*i, screenHeight))
                for j in list(range(round(screenHeight/32))):
                    pygame.draw.line(grid, (0, 0, 0, 64), (0, 32*j), (screenWidth, 32*j))
            screen.blit(grid, (0,0)) # draw grid surface to screen

        # flip the display
        pygame.display.flip()

        for event in pygame.event.get():
            # handle pygame window closed
            if event.type == pygame.QUIT:
                running = False
            
            # handle keyboard input
            if event.type == pygame.KEYDOWN:
                (oldCol, oldRow) = (col, row)
                match event.key:
                    case pygame.K_LEFT:
                        if col > 1: col -= 1
                    case pygame.K_RIGHT:
                        if col < 6: col += 1
                    case pygame.K_UP:
                        if row > 1: row -= 1
                    case pygame.K_DOWN:
                        if row < 6: row += 1
                    case pygame.K_g:
                        showGrid = not showGrid

                # open new map data file if default mode and col or row changed
                if mode == "default" and (col, row) != (oldCol, oldRow):
                    mapData = openMapFile("maps/episode1/0{}0{}.txt".format(col, row))
    
    print("We hope you enjoyed your stay!")
    return

if __name__ == "__main__":
    main()