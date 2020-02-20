import json
from pathlib import Path
from py import bannermod as bm
from py import resultsgrab as rg

# Opens general settings file and stores them in dictionary (gs)
with open(Path(__file__).resolve().parent / 'settings.json', 'r') as confile:
    gs = json.load(confile)

tagline = 'Default Tagline'

ggOut = rg.ggresults()

players = ggOut.getTop8()
characterImg = ggOut.getTop8Chars()

# Default overrides
if gs['ManualTag'] == True:
    tagline = gs['ManualTagText']

if gs['ManualCharacters'] == True:
    for i in range(len(gs['ManualData'])):
        if gs['ManualList'][i] :
            players[i] = gs['ManualData'][i]['name']
            characterImg[i] = gs['ManualData'][i]['character']

# print(tagline)
# print(players)
# print(characterImg)

banner = bm.bannerGen(players, characterImg, tagline)
banner.genImg()