# AutoBanner
Autobanner is software designed to automatically create results banners for tournaments using a smashgg api. 

# Author
Timothy Yabuki

# Installation
Requirements:
* Python 3.0+ must be installed on your machine
* The following python libraries must be installed on your machine
  * PIL
  * GraphQLClient
* You must have acces to a smashgg authentification token to use this program
  * You can get acces to a smashgg authentification token [here](https://developer.smash.gg/docs/authentication/)
  * A JSON file named "tokens.json" containing one field named "smashgg" paired with your smashgg token must be created in the autobanner directory.
  
# Usage
The program will automatically create a results banner on runtime based on parameters given to it in the settings.json and graphicConfig.json files. graphicConfig is used to arrange the locations of various graphical elements on screen (x,y position of player names, character image x,y position, ect.). Settings.json is used to determine factors that might change between renders. I'll go through some of them here.

* slug - Refers to the tournament slug. This is a value generated from the url from the tournament. For example (tournament/reveille-s-revenge/event/reveille-s-revenge)
  * Caution: the slug is not directly pulled from the tournament url. The program may fail if "events" in the url is not replaced with "event"
* outputfilename - Refers to the name of the file for output. 
* InputBG - Refers to the name of the file in the imgs directory that the program uses as the base image to draw on.
* HeaderText - Refers to the text fed into the "header" field of the banner.
* ManualTag - Current should always be set to true. Will eventually determine whether the program should automatically generate a tagline based on date and entrants, or if it should be manually determined in settings.
* ManualTagText - If ManualTag is true, ManualTagText will be used for the tagline field of the banner.
* ManualCharacters - Used to determine if any players or character images will be manually determined.
* ManualList - Used to determine which players or characters will be overwriten by manual data. The 0 index of the array is for first place, the 7th index of the array is for the second 7th place finisher.
* ManualData - Used to overwrite smashgg data if so desired. 
