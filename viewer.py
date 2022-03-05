from sqlite3 import SQLITE_CREATE_TEMP_VIEW
import sys
import json
import re
import pprint
import pygame
import random

# Opens map data file and converts the map data to json
def processMapDataFile(fname):
    # open map data file
    infile = open(fname, "r")
    data = infile.read()
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

# (deprecated) Separates the map data into fields and separator symbols.
def separateTokens(data):
    # process file to separate tokens
    s = ""
    tokens = []
    inquote = False
    for i,c in enumerate(data):
        match c:
            case '[':
                tokens.append(c)
                s = ""
                continue
            case ',' | ':' | ']':
                if inquote:
                    s += c
                    continue

                if len(s) > 0:
                    tokens.append(s)
                if c != ',' and c != ']':
                    tokens.append(c)
                s = ""
            case '"':
                s+= '"'
                inquote = not inquote
            case _:
                s += c

    return tokens

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
        tiles.append(json.loads(tile.__str__()))

    return tiles


def main():
    print("Cartoon Cartoon Summer Resort Map Viewer\nby TheOnlyZac\n")
    argc = len(sys.argv)
    argv = sys.argv

    # Ensure a file was passed as an argument
    if (argc < 2):
        print("Usage: parseDict.py [filename]")
        return
    
    # Open and map data file
    print("Processing map data...")
    processedData = processMapDataFile(sys.argv[1])
    tileDataStrings = separateTileStrings(processedData)
    tiles = jsonLoadTileData(tileDataStrings)

    print("Done.\n")

    # Init pygame
    print("Initializing pygame...")
    (screenWidth, screenHeight) = (416, 320)
    bgcolor = (255, 255, 255)
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.SRCALPHA)
    print("Done.\n")

    print("Rendering map data...")
    # clear screen
    screen.fill(bgcolor)

    # draw each tile
    for tile in tiles:
        try:
            (x, y, tileWidth, tileHeight) = (tile["#location"][0], tile["#location"][1],
                                            tile["#width"], tile["#height"])
            
            sprite = None
            try:
                sprite = pygame.image.load('tiles/episode1/' + tile["#member"] + '.png')
            except:
                pass

            rect = (16*x, 16*y, tileWidth, tileHeight)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            #pygame.draw.rect(screen, color, rect)
            
            if "tile" in tile["#member"] or "Tile" in tile["#member"]:
                for i in list(range(round(tileWidth/32))):
                    for j in list(range(round(tileHeight/32))):
                            screen.blit(sprite, (16*x + i*32, 16*y + j*32))
            else:
                screen.blit(sprite, (16*x - 16, 16*y - 16))
                
        except:
            continue

    # draw grid over the whole screen
    grid = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA) # create grid surface with opacity
    for i in list(range(round(screenWidth/32))): # draw gridlines to surface
        pygame.draw.line(grid, (0, 0, 0, 64), (32*i, 0), (32*i, screenHeight))
        for j in list(range(round(screenHeight/32))):
            pygame.draw.line(grid, (0, 0, 0, 64), (0, 32*j), (screenWidth, 32*j))
    screen.blit(grid, (0,0)) # draw grid surface to screen
            
    pygame.display.flip()
    print("Done.\n")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    print("We hope you enjoyed your stay!")
    return

if __name__ == "__main__":
    main()