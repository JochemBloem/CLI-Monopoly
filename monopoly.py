
import random as rnd
import time
import boarddef_standard

#globals
GLOBAL_SPEED = .2
SHORT_SLEEP = 1 * GLOBAL_SPEED
LONG_SLEEP = 2 * GLOBAL_SPEED

class Game:
    def __init__(self):
        confirm = ""
        self.players = []
        self.board = Board(boarddef_standard.boarddef)
        while not confirm == "y":
            confirm = ""
            self.playeramount = getUserInput("How many HUMANS are playing? ", int)
            self.botamount = getUserInput("How many BOTS are playing? ", int)

            clearSpace(5)

            print str(self.playeramount) + " human player" + ("s" if self.playeramount > 1 else "") + " and"
            print str(self.botamount) + " bot" + ("s" if self.botamount > 1 else "") + " are playing"
            while not confirm in ["y", "n"]:
                confirm = raw_input("Confirm? [y/n]: ").lower()

        clearSpace(3)
        self.playerSetup()
    
    def playerSetup(self):
        for i in range(self.playeramount):
            playername = getUserInput("Enter name for human player " + str(i + 1) + ": ", str)
            self.players.append(Player(playername, self, "player", i))
        
        for i in range(self.botamount):
            self.players.append(Player("Bot" + str(i + 1), self, "bot", self.playeramount + i))

        clearSpace(1)
        print "These will be the players:"
        for i in range(len(self.players)):
            print self.players[i].name

    def getAmountInSet(self, player, workingSet):
        player = self.players[player]
        amountInSet = 0
        for prop in player.properties:
            if prop.properties["set"] == workingSet:
                amountInSet+=1

        return amountInSet

    def getTotalInSet(self, workingSet):
        sets = {
            "brown": 2,
            "lightblue": 3,
            "pink": 3,
            "orange": 3,
            "red": 3,
            "yellow": 3,
            "green": 3,
            "darkblue": 2,
            "railroads": 4,
            "utilities": 2
        }

        return sets[workingSet]

    def leaderboard(self):
        clearSpace(1)
        for i, player in enumerate(self.players):
            print str(i) + ": " + player.name + ", with $" + str(player.money) + " and " + str(len(player.properties)) + " properties"
        clearSpace(1)

    def start(self):
        raw_input("Press Enter to start the game! ")
        
        # while there are more than 1 player left, the game is not over
        clearSpace(20)
        while len(self.players) > 1:
            for i in range(len(self.players)):
                player = self.players[i]
                if player.type == "player":
                    #this is a human player, and should therefore be able to make their own decisions
                    print player.name + ", it's your turn!"
                    print "You are currently on " + self.board.getLocationName(player.position) + ", and you have $" + str(player.money) + " left."
                    clearSpace(1)

                    playermove = ".help"
                    success = False
                    move_options = {
                        ".move": player.move,
                        ".build": player.build,
                        ".set": player.sets,
                        ".bail": player.bail,
                        ".help": player.help,
                        ".properties": player.showProperties,
                        ".leaderboard": self.leaderboard
                    }
                    while playermove == ".help" or not success:
                        playermove = getUserInput("Make a move: ", str)
                        try:
                            success = move_options[playermove.lower()]()
                        except KeyError:
                            print "That is not a valid move. Press .help for all options."

                    raw_input("Press enter to end your turn! ")

                else:
                    #this is a bot and their actions are automated
                    print player.name + " is making their move."
                    time.sleep(SHORT_SLEEP)
                    player.move()
                    
                    print player.name + " is done."
                    time.sleep(LONG_SLEEP)
                clearSpace(20)

class Board:

    def __init__(self, boarddef):
        self.squares = boarddef

    def getLocationName(self, location):
        return self.squares[location].properties["name"]
    
    def getLocation(self, location):
        return self.squares[location]

class Player:
    
    def __init__(self, name, game, playerType, index):
        self.name = name
        self.index = index
        self.money = 1500
        self.properties = []
        self.position = 0
        self.type = playerType
        self.game = game

        self.double = False
        self.doublesInArow = 0
        self.inPrison = False

        #botparameters
        self.purchaseThreshold = 500

    def move(self):
        clearSpace(1)
        die1 = rnd.randint(1,6)
        die2 = rnd.randint(1,6)
        total = die1 + die2
        self.position += total

        who = "You" if self.type == "player" else self.name

        print who + " threw a" + ("n " if total in [8, 11] else " ") + str(total) + "! (" + str(die1) + "+" + str(die2) + ")"

        if(self.position >= 40):
            self.position = self.position % 40
            self.money += 200
            print who + " also passed start, and have received $200! (total: $" + str(self.money)

        tile = self.game.board.getLocation(self.position)
        tilename = tile.properties["name"]

        #player get more information in the console about their moves
        if self.type == "player":

            #the tile the player landed on is a Property
            if isinstance(tile, boarddef_standard.Property):
                #the Property is still purchaseable
                owner = self.game.players[tile.owner]
                if tile.state == "free":
                    print tile.properties["name"] + " (" + tile.properties["set"] + ") is still purchaseable for $" + str(tile.properties["price"])
                    confirm = ""
                    while not confirm in ["y", "n"]:
                        confirm = getUserInput("Do you wish to purchase this property? [y/n] ").lower()

                    if confirm == "y":
                        self.purchase(tile)
                #the Property is owned by another player, and the current player has to pay rent
                elif tile.state == "owned":
                    print "You landed on " + tile.properties["name"]
                    print "This property is owned by " + self.game.players[tile.owner].name
                    if tile.properties["set"] == "utilities":
                        rent = total * (4 if game.getAmountInSet(tile.owner, "utilities") == 1 else 10)
                    elif tile.properties["set"] == "railroads":
                        rent = tile.properties["rent"][game.getAmountInSet(tile.owner, "railroads")]
                    else:
                        rent = tile.properties["rent"][tile.houses]
                    print "You owe " + self.game.players[tile.owner].name + " $" + str(rent) + " in rent."
                    print "    (" + self.game.board.getLocationName(self.position) + " currently has " + str(tile.houses) + " houses)"
                    time.sleep(SHORT_SLEEP)
                    self.money -= tile.properties["rent"][tile.houses]
                    self.game.players[tile.owner].money += tile.properties["rent"][tile.houses]
                    if self.money > 0:
                        print "You now have $" + str(self.money)
                    else:
                        print "You cannot afford rent on this property."
                elif tile.state == "mortgaged":
                    pass
        #bots are automated
        else:
            print who + " landed on " + tilename
            time.sleep(SHORT_SLEEP)
            if isinstance(tile, boarddef_standard.Property):
                owner = self.game.players[tile.owner]

                #if this is their own property, do nothing
                if tile.owner == self.index:
                    print tilename + " is already " + self.name + "'s property." 
                    return True

                purchaseable = self.money - tile.properties["price"] > self.purchaseThreshold
                if tile.state == "free" and purchaseable:
                    self.purchase(tile)

                elif tile.state == "owned":
                    if tile.properties["set"] == "utilities":
                        rent = total * (4 if game.getAmountInSet(tile.owner, "utilities") == 1 else 10)
                    elif tile.properties["set"] == "railroads":
                        rent = tile.properties["rent"][game.getAmountInSet(tile.owner, "railroads")]
                    else:
                        rent = tile.properties["rent"][tile.houses]
                    self.money -= rent
                    owner.money += rent
                    print who + " paid $" + str(rent) + " to " + owner.name + " (Total: $" + str(self.money) + ")"

                elif tile.state == "mortgaged":
                    print tilename + " is owned by " + owner + ", but it is mortgaged! Nothing happens."
            
            elif isinstance(tile, boarddef_standard.Draw):
                pass
            
            elif isinstance(tile, boarddef_standard.Special):
                if tile.properties["tax"]:
                    print self.name + " owes the bank $" + str(tile.properties["value"]) + "."
                    self.money -= tile.properties["value"]
                    print self.name + " now has $" + str(self.money)
                elif tile.properties["name"] == "Go to prison":
                    print self.name + " is now in prison!"
                    self.position = 10
                    self.inPrison = True

        return True

    def build(self):
        ownedSets = self.getOwnedSets()
        for workingSet in ownedSets:
            if game.getAmountInSet(self.index, workingset) == len(ownedSets[workingSet]):
                print "You can build on the " + workingSet + " set."
                return True
        print "You need to have a complete set in order to start building houses. \nType .properties to see your current progress."
        return False

    def getOwnedSets(self):
        ownedSets = {}
        for prop in self.properties:
            workingSet = prop.properties["set"]
            if not workingSet in ownedSets:
                ownedSets[workingSet] = [prop]
            else:
                ownedSets[workingSet].append(prop)
        return ownedSets

    def bail(self):
        return True

    def purchase(self, tile):
        tile.purchase(self.index)
        self.money -= tile.properties["price"]
        print ("You" if self.type == "player" else self.name) + " now own" + (" " if self.type == "player" else "s ") + tile.properties["name"] + " (" + tile.properties["set"] + ")!"
        self.properties.append(tile)
        time.sleep(SHORT_SLEEP)

    def help(self):
        clearSpace(1)
        if self.inPrison:
            print "You are currently in prison."
            print "You can buy your way out of prison by typing .bail"
            
        print "You can move your character by typing .move"
        print "You can build on properties by typing .build"
        print "You can see your sets by typing .set"
        print "You can list all your properties by typing .properties"
        print "You can view the leaderboard by typing .leaderboard"
        clearSpace(1)
        return False

    def sets(self):
        ownedSets = self.getOwnedSets()
        
        for key in ownedSets:
            print key + ": " + str(game.getAmountInSet(self.index, key)) + "/" + str(game.getTotalInSet(key))
        return False

    def showProperties(self):
        clearSpace(1)
        print "You own the following properties:"
        
        ownedSets = self.getOwnedSets()
        
        for key in ownedSets:
            print key + ": " + str(len(ownedSets[key])) + "/" + str(game.getTotalInSet(key))
            for prop in ownedSets[key]:
                name = "    " + prop.properties["name"]
                while len(name) < 35:
                    name += " "
                houses = "with " + (str(prop.houses) + " houses " if not prop.houses == 5 else "1 hotel ") if prop.properties["set"] not in ["utilities", "railroads"] else ""
                while len(houses) < 14:
                    houses += " "
                multiplier = (2 if game.getAmountInSet(self.index, prop.properties["set"]) == game.getTotalInSet(prop.properties["set"]) else 1)
                rent = "($" + str(prop.properties["rent"][(prop.houses if prop.properties["set"] not in ["utilities", "railroads"] else game.getAmountInSet(self.index, prop.properties["set"]) )] * multiplier) + ")"
                mortgaged = ("\nMORTGAGED" if prop.state == "mortgaged" else "")
                print name + houses + rent + mortgaged
        clearSpace(1)
        return False

def getInputType(string):
    switcher = {
        "<type 'int'>": "integer",
        "<type 'str'>": "string"
    }
    try:
        return switcher[string]
    except:
        return "Unknown datatype"

def getUserInput(string, inputtype = str):
    userinput = None
    while not isinstance(userinput, inputtype):
        userinput = raw_input(string)
        try:
            userinput = inputtype(userinput)
            return userinput
        except ValueError:
            print "Please enter a valid "+ getInputType(str(inputtype)) +"!"

def clearSpace(lines):
    for _ in range(lines):
        print ""

game = Game()
game.start()
