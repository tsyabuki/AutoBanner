import json
from statistics import mode, StatisticsError
from pathlib import Path
from graphqlclient import GraphQLClient

class ggresults:
    def __init__(self):
        # Opens general settings file and stores them in dictionary (gs)
        with open(Path(__file__).resolve().parents[1] / 'settings.json', 'r') as confile:
            gs = json.load(confile)
        # Gets smashgg dev token from tokens.json
        with open(Path(__file__).resolve().parents[1] / 'tokens.json', 'r') as confile:
            tk = json.load(confile)
        # Gets all smashgg characterIDs from characterIDs.json
        with open(Path(__file__).resolve().parent / 'characterIDs.json', 'r') as confile:
            self.cid = json.load(confile)

        self.TOKEN = tk['smashgg']
        self.slug = gs['Slug']
        self.players = []
        self.entrantIDs = []
        self.selections = [[],[],[],[],[],[],[],[]]
        self.commonSelections = []
        self.characterImgs = []

        # Connect with smashgg API w/ token
        self.client = GraphQLClient('https://api.smash.gg/gql/alpha')
        self.client.inject_token('Bearer ' + self.TOKEN)

    def getTop8(self):
        '''
        Finds the top 8 players and outputs them in format [1st, 2nd, 3rd, 4th, 5th(1), 5th(2), 7th(1), 7th(2)]
        '''
        result = self.client.execute(
        '''
        query EventStandings($slug: String!, $page: Int!, $perPage: Int!) {
            event(slug: $slug) {
            name
            standings(query: {
                perPage: $perPage,
                page: $page
            }){
                nodes {
                entrant {
                  	id,
                    participants {
                    player {
                        gamerTag
                    }
                    }
                }
                }
            }
            }
        }
        ''',
        {
            "slug": self.slug,
            "page": 1,
            "perPage": 8
        })

        dict_result = json.loads(result)

        if 'errors' in dict_result:
            print('ERROR: ' + dict_result['errors'][0]['message'])
        else:
            for x in dict_result['data']['event']['standings']['nodes']: # Loops through all found players
                self.players.append(x['entrant']['participants'][0]['player']['gamerTag'])
                self.entrantIDs.append(x['entrant']['id'])

        return self.players

    def getTop8Chars(self):
        '''
        Gets the characters of the top 8 players from most played in all sets
        '''
        result = self.client.execute(
        '''
       query EventSets($slug: String!, $page: Int!, $perPage: Int!, $entrantIDs: [ID!]) {
            event(slug: $slug) {
                id
                name
                sets(
                page: $page
                perPage: $perPage
                sortType: STANDARD
                filters:{
                    entrantIds: $entrantIDs
                }) 
                    {
                pageInfo {
                    total
                }
                nodes {
                    games {
                    selections {
                        entrantId
                        selectionValue
                    }
                    }
                }
                }
            }
        }
        ''',
        {
            "slug": self.slug,
            "page": 1,
            "perPage": 100,
            "entrantIDs": self.entrantIDs
        })

        dict_result = json.loads(result)

        if 'errors' in dict_result:
            print('ERROR: ' + dict_result['errors'][0]['message'])
        else:
            for x in dict_result['data']['event']['sets']['nodes']: # Loops through all found sets
                # print(x)
                if x['games'] != None and x['games'] != "null": #If "Games" exist
                    for y in x['games']: # Check each "game"
                        for z in y['selections']: # Check each character pick per game
                            for w in range(8): # Create a list of each played character per player
                                if(z['entrantId'] == self.entrantIDs[w]):
                                    self.selections[w].append(z['selectionValue'])

        for v in range(8): # Find the most common selection from each player
            if len(self.selections[v]) != 0:
                try:
                    self.commonSelections.append(mode(self.selections[v]))
                except StatisticsError: 
                    self.commonSelections.append(self.selections[v][0])
            else: # If no selections are found, 0 is appended
                self.commonSelections.append(0)

        for t in range(len(self.commonSelections)): # If no selection was found (0 was appended), replace character with scizor
            if self.commonSelections[t] == 0:
                self.characterImgs.append('scizor.png')
            else:
                self.characterImgs.append(self.cid[str(self.commonSelections[t])])
            
        return self.characterImgs

