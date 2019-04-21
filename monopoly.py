
import random as rnd
import time
import boarddef_standard

#globals
GLOBAL_SPEED = .2
SHORT_SLEEP = 1 * GLOBAL_SPEED
LONG_SLEEP = 2 * GLOBAL_SPEED
SMALL_RELATIVE = 50

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
                        ".bail": player.bail,
                        ".help": player.help,
                        ".trade": player.trade,
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

        print who + " landed on " + tilename

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
                        rent = total * (4 if self.game.getAmountInSet(tile.owner, "utilities") == 1 else 10)
                    elif tile.properties["set"] == "railroads":
                        rent = tile.properties["rent"][self.game.getAmountInSet(tile.owner, "railroads")]
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
        #bots are automated
        else:
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
                        rent = total * (4 if self.game.getAmountInSet(tile.owner, "utilities") == 1 else 10)
                    elif tile.properties["set"] == "railroads":
                        rent = tile.properties["rent"][self.game.getAmountInSet(tile.owner, "railroads")]
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
            if self.game.getAmountInSet(self.index, workingSet) == len(ownedSets[workingSet]):
                print "You can build on the " + workingSet + " set."
                return True
        print "You need to have a complete set in order to start building houses. \nType .properties to see your current progress."
        return False

    def trade(self):
        target = ""
        while not target == ".quit":
            target = getUserInput("Who do you want to trade with? ").lower()
            if target == ".quit":
                return False
            for player in self.game.players:
                if player.name.lower() == target:
                    clearSpace()
                    print "You are trading with " + player.name

                    #List all properties of the two trading parties
                    props = [["Money: (max: $" + str(self.money) + ")"],["Money: (max: $" + str(player.money) + ")"]]
                    for i, player in enumerate([self, player]):
                        for prop in player.properties:
                            props[i].append( prop.properties["name"] + " (" + prop.properties["set"] + ")" )

                    displayList(props[0], props[1], "Your properties:", player.name + "'s properties:")
                    
                    has = self.getTradingItems(True, len(self.properties) + 1, self)
                    if has == "quit":
                        return False
                    wants = self.getTradingItems(False, len(player.properties) + 1, player)
                    if wants == "quit":
                        return False

                    # review the deal
                    clearSpace()
                    props = [[],[]]
                    for i, workingList in enumerate([has, wants]):
                        for prop in workingList:
                            part1 = prop.properties["name"] + " " if not prop.state == "money" else ""
                            part2 = "(" + prop.properties["set"] + ")" if not prop.state == "money" else "$" + str(prop.value)
                            props[i].append(part1 + part2)
                    displayList(props[0], props[1], self.name + " gives to " + player.name + ":", player.name + " gives to " + self.name + ":")
                    clearSpace(1)
                    
                    if getUserConfirm("Do you wish to propose this trade deal to " + player.name + "? [y/n] "):
                        # propose the deal
                        print "Deal proposed"
                        time.sleep(SHORT_SLEEP)
                        if player.proposeDeal(self, has, wants):
                            print player.name + " has accepted the deal."
                            # proceed with the deal
                            clearSpace(2)
                            for prop in has:
                                if prop.state == "money":
                                    player.money += prop.value
                                    self.money -= prop.value                             
                                else: 
                                    player.properties.append(prop)
                                    self.properties.remove(prop)
                                    print player.name + " gains " + prop.properties["name"]
                            for prop in wants:
                                if prop.state == "money":
                                    self.money += prop.value
                                    player.money -= prop.value
                                else: 
                                    self.properties.append(prop)
                                    player.properties.remove(prop)
                                    print self.name + " gains " + prop.properties["name"]
                            
                            print player.name + " now has $" + str(self.money)
                            print self.name + " now has $" + str(player.money)
                            clearSpace(1)

                        else:
                            print player.name + " has rejected the deal."

                    else:
                        print "The trade deal has been aborted."
                        time.sleep(SHORT_SLEEP)

                    return False
            print "That player could not be found. Try again or type .quit to stop trading."
        return False

    def getTradingItems(self, has, maxProperties, who):
        clearSpace(2)
        print "Type .next to go to the next player or .quit to quit" if has else "Type .next to review the trade deal or .quit to quit"
        clearSpace(1)
        text = "Add an item to " + ("YOUR" if has else "THEIR") + " side of the deal: "
        item = ""
        items = []
        while not item in [".next", ".quit"]:
            item = getUserInput(text)
            if item == ".next":
                return items
            if item == ".quit":
                return "quit"
            try:
                item = int(item)
                if item > maxProperties:
                    print "That value exceeds " + ("your" if has else "their") + " amount of properties. Choose a lower value."
                    continue
                else:
                    # if the item is money, show a popup to ask for how much
                    if item == 1:
                        correct = False
                        amount = 0
                        while not correct:
                            amount = getUserInput(indent() + "How much? $", int)
                            if amount <= who.money and amount >= 0:
                                correct = True
                            elif amount > who.money: 
                                print indent() + who.name + " cannot pay more than they currently have! ($" + str(who.money) + ")"
                            elif amount < 0:
                                print indent() + "You cannot enter a value below 0!"
                        
                        money = boarddef_standard.Property(None)
                        money.state = "money"
                        money.value = amount
                        items.append(money)
                    else:
                        item -= 2 # return the value to the correct property indices
                        desired = who.properties[item]
                        if not desired in items:
                            items.append(desired)
                            print "Added " + desired.properties["name"] + " to " + ("your" if has else "their") + " side of the trade deal"
                        else:
                            print desired.properties["name"] + " is already present in the deal. Choose another property or type .next to " + ("go to their side of the deal" if has else "review the deal")
            except ValueError:
                print "Please enter a valid integer. See above list for available properties and their indices."
            clearSpace(1)

    def proposeDeal(self, target, theirs, ours):
        valuation = 0

        combo = [ours, theirs]

        for i, player in enumerate([self, target]):
            for prop in combo[i]:
                valuation += self.evaluate(player, prop, (True if player == target else False), combo[i])

        return valuation > 0

    def evaluate(self, target, prop, positive, restOfDeal):
        # get a base value (the price of the property, or the amount of money)
        if prop.state == "money":
            base = prop.value
        else: 
            base = prop.properties["price"]

        # calculate the relative value
        
        # gain value for each property of the same set already in possession by the target
        #   gain a lot of value for this property being the last to complete a set
        relative = 0
        if not prop.state == "money":
            propset = prop.properties["set"]
            for prop2 in target.properties:
                if prop2.properties["set"] == propset:
                    relative += SMALL_RELATIVE
            

        # return as a positive value if positive == True else return as a negative value
        value = base + relative

        value *= ( 1 if positive else -1 )

        return value

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
        print "You can trade with other players by typing .trade"
        print "You can list all your properties by typing .properties"
        print "You can view the leaderboard by typing .leaderboard"
        clearSpace(1)
        return False

    def showProperties(self):
        clearSpace(1)
        print "You own the following properties:"
        
        ownedSets = self.getOwnedSets()
        
        for key in ownedSets:
            print key + ": " + str(len(ownedSets[key])) + "/" + str(self.game.getTotalInSet(key))
            for prop in ownedSets[key]:
                name = indent() + prop.properties["name"]
                while len(name) < 35:
                    name += " "
                houses = "with " + (str(prop.houses) + " houses " if not prop.houses == 5 else "1 hotel ") if prop.properties["set"] not in ["utilities", "railroads"] else ""
                while len(houses) < 14:
                    houses += " "
                multiplier = (2 if self.game.getAmountInSet(self.index, prop.properties["set"]) == self.game.getTotalInSet(prop.properties["set"]) else 1)
                rent = "($" + str(prop.properties["rent"][(prop.houses if prop.properties["set"] not in ["utilities", "railroads"] else self.game.getAmountInSet(self.index, prop.properties["set"]) )] * multiplier) + ")"
                mortgaged = ("\nMORTGAGED" if prop.state == "mortgaged" else "")
                print name + houses + rent + mortgaged
        clearSpace(1)
        return False

def createSegment(length, text = ""):
        segment = text
        while len(segment) < length:
            segment += " "
        return segment

def indent(amount = 1):
    string = ""
    for _ in range(amount):
        string += "    "
    return string

def displayList(list1, list2, header1 = "", header2 = ""):
    mostitems = max(len(list1), len(list2))
    line = createSegment(text=header1, length=45) + createSegment(text=header2, length=45)
    print line
    clearSpace(1)
    for i in range(mostitems):
        line = ""
        for l in [list1, list2]:
            try:
                line += createSegment(45, str(i + 1) + ": " + l[i])
            except IndexError:
                line += createSegment(45)
        print line 
    clearSpace(1)


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

def getUserConfirm(string):
    answer = ""
    while not answer in ["y", "n"]:
        answer = getUserInput(string).lower()
    return answer == "y"

def clearSpace(lines = 20):
    for _ in range(lines):
        print ""

game = Game()
game.start()
