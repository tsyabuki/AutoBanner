import json
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

class bannerGen:
    def __init__(self, playerIn, characterImgIn, tagLineIn):
        # Find relevant directories
        self.imgDir = Path(__file__).resolve().parents[1] / 'imgs'
        self.fontDir = Path(__file__).resolve().parents[1] / 'fonts'
        self.outDir = Path(__file__).resolve().parents[1] / 'output'



        # Open graphical configuration settings and store them in dictionary (gcs)
        with open(Path(__file__).resolve().parents[1] / 'graphicConfig.json', 'r') as confile:
            gcs = json.load(confile)

        # Opens general settings file and stores them in dictionary (gs)
        with open(Path(__file__).resolve().parents[1] / 'settings.json', 'r') as confile:
            self.gs = json.load(confile)

        # Variables from other scripts
        self.outputFilename = self.gs['OutputFilename']
        self.players = playerIn
        self.characters = characterImgIn
        # Player character X and Y image positions
        self.charx = gcs['charX']
        self.chary = gcs['charY']

        # Player name variables
        self.nameFont = ImageFont.truetype(str(self.fontDir / gcs['playerFontName']), gcs['playerFontSize'])
        self.nameX = gcs['nameX']
        self.nameY = gcs['nameY']
        self.nameW = gcs['nameW']
        self.nameH = gcs['nameH']

        # Header variables
        self.headerText = self.gs['HeaderText']
        self.headerFont = ImageFont.truetype(str(self.fontDir / gcs['headerFontName']), gcs['headerFontSize'])
        self.headerX = gcs['headerX']
        self.headerY = gcs['headerY']
        self.headerW = gcs['headerW']
        self.headerH = gcs['headerH']

        # Tagline variables
        self.tagText = tagLineIn
        self.tagFont = ImageFont.truetype(str(self.fontDir / gcs['tagFontName']), gcs['tagFontSize'])
        self.tagX = gcs['tagX']
        self.tagY = gcs['tagY']
        self.tagW = gcs['tagW']
        self.tagH = gcs['tagH']

        self.tagsToCaps = gcs['tagsToCaps']

    def genImg(self):
        # Establishes images
        bannerBg = Image.open(self.imgDir / self.gs['InputBG'])
        charImg = [] # charImg is a list containing all the images for the top 8
        for i in self.characters:
            charImg.append(Image.open(self.imgDir / i))

        # Sets up draw
        imgOut = bannerBg.copy()
        imgDraw = ImageDraw.Draw(imgOut)

        # Draws header and tagline
        if self.headerW == 0 and self.headerH == 0: # If width and height values exist, center the text
            imgDraw.text((self.headerX, self.headerY), self.headerText, font=self.headerFont)
        else: 
            w, h = imgDraw.textsize(self.headerText, font=self.headerFont) # Creates temporary coordinates to center the text based on width and height values
            imgDraw.text((self.headerX + (self.headerW-w)/2, self.headerY + (self.headerH-h)/2), self.headerText, font=self.headerFont)

        if self.tagW == 0 and self.tagH == 0: # If width and height values exist, center the text
            imgDraw.text((self.tagX, self.tagY), self.tagText, font=self.tagFont)
        else: 
            w, h = imgDraw.textsize(self.tagText, font=self.tagFont) # Creates temporary coordinates to center the text based on width and height values
            imgDraw.text((self.tagX + (self.tagW-w)/2, self.tagY + (self.tagH-h)/2), self.tagText, font=self.tagFont)

        # Draws player names and characters
        for j in range(8):
            imgOut.paste(charImg[j], (self.charx[j], self.chary[j]), charImg[j])
            if self.tagsToCaps: # Capitalizes tags if boolean
                self.players[j] = self.players[j].upper() 
            if self.nameW[j] == 0 and self.nameH[j] == 0: # If width and height values exist, center the text
                imgDraw.text((self.nameX[j], self.nameY[j]), self.players[j], font=self.nameFont)
            else: 
                w, h = imgDraw.textsize(self.players[j], font=self.nameFont) # Creates temporary coordinates to center the text based on width and height values
                imgDraw.text((self.nameX[j] + (self.nameW[j]-w)/2, self.nameY[j] + (self.nameH[j]-h)/2), self.players[j], font=self.nameFont)

        # Save image
        imgOut.save(self.outDir / self.outputFilename)