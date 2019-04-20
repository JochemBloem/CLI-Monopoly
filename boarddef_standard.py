class Property:
    
    def __init__(self, propertydef):
        self.properties = propertydef
        self.state = "free"
        self.houses = 0
        self.owner = -1

    def purchase(self, purchaser):
        self.owner = purchaser
        self.state = "owned"

class Draw:

    def __init__(self, cardtype):
        self.properties = {"name": cardtype}
    def action(self):
        # either draw a chance or community chest card
        pass
    pass

class Special:
    # Start, Prison, Free parking or Go to prison
    # There are also several 'pay taxes' cards or whatever on the board,
    # these should be handled here
    def __init__(self, name, value = 0, tax = False):
        self.properties = {"name": name, "value": value, "tax": tax}

boarddef = [
    #Start
    Special("Start"),
    #Mediterranean Avenue
    Property(
        {
            "name": "Mediterranean Avenue",
            "set": "brown",
            "price": 60,
            "houseprice": 50,
            "rent": {
                0: 2,
                1: 10, 
                2: 30, 
                3: 90,
                4: 160,
                5: 250 }
        }),
    #Community Chest
    Draw("Community Chest"),
    #Baltic Avenue
    Property(
        {
            "name": "Baltic Avenue",
            "set": "brown",
            "price": 60,
            "houseprice": 50,
            "rent": {
                0: 4,
                1: 20, 
                2: 60, 
                3: 180,
                4: 320,
                5: 450 }
        }),
    #Income Tax
    Special("Income tax", value = 200, tax=True),
    #Reading Railroad
    Property(
        {
            "name": "Reading Railroad",
            "set": "railroads",
            "price": 200,
            "rent": {
                0: 25,
                1: 50, 
                2: 100, 
                3: 200 }
        }),
    #Oriental Avenue
    Property(
        {
            "name": "Oriental Avenue",
            "set": "lightblue",
            "price": 100,
            "houseprice": 50,
            "rent": {
                0: 6,
                1: 30, 
                2: 90, 
                3: 270,
                4: 400,
                5: 550 }
        }),
    #Chance
    Draw("Chance"),
    #Vermont Avenue
    Property(
        {
            "name": "Vermont Avenue",
            "set": "lightblue",
            "price": 100,
            "houseprice": 50,
            "rent": {
                0: 6,
                1: 30, 
                2: 90, 
                3: 270,
                4: 400,
                5: 550 }
        }),
    #Connecticut Avenue
    Property(
        {
            "name": "Connecticut Avenue",
            "set": "lightblue",
            "price": 120,
            "houseprice": 50,
            "rent": {
                0: 8,
                1: 40, 
                2: 100, 
                3: 300,
                4: 450,
                5: 600 }
        }),
    #Prison
    Special("Prison"),
    #St. Charles Place
    Property(
        {
            "name": "St. Charles Place",
            "set": "pink",
            "price": 120,
            "houseprice": 100,
            "rent": {
                0: 10,
                1: 50, 
                2: 150, 
                3: 450,
                4: 625,
                5: 750 }
        }),
    #Electric Company
    Property(
        {
            "name": "Electric Company",
            "set": "utilities",
            "price": 150
        }),
    #States Avenue
    Property(
        {
            "name": "States Avenue",
            "set": "pink",
            "price": 140,
            "houseprice": 100,
            "rent": {
                0: 10,
                1: 50, 
                2: 150, 
                3: 450,
                4: 625,
                5: 750 }
        }),
    #Virginia Avenue
    Property(
        {
            "name": "Virginia Avenue",
            "set": "pink",
            "price": 160,
            "houseprice": 100,
            "rent": {
                0: 12,
                1: 60, 
                2: 180, 
                3: 500,
                4: 700,
                5: 900 }
        }),
    #Pennsylvania Railroad
    Property(
        {
            "name": "Pennsylvania Railroad",
            "set": "railroads",
            "price": 200,
            "rent": {
                0: 25,
                1: 50, 
                2: 100, 
                3: 200 }
        }),
    #St. James Place
    Property(
        {
            "name": "St. James Place",
            "set": "orange",
            "price": 180,
            "houseprice": 100,
            "rent": {
                0: 14,
                1: 70, 
                2: 200, 
                3: 550,
                4: 750,
                5: 950 }
        }),
    #Community Chest
    Draw("Community Chest"),
    #Tennessee Avenue
    Property(
        {
            "name": "Tennessee Avenue",
            "set": "orange",
            "price": 180,
            "houseprice": 100,
            "rent": {
                0: 14,
                1: 70, 
                2: 200, 
                3: 550,
                4: 750,
                5: 950 }
        }),
    #New York Avenue
    Property(
        {
            "name": "New York Avenue",
            "set": "orange",
            "price": 200,
            "houseprice": 100,
            "rent": {
                0: 16,
                1: 80, 
                2: 220, 
                3: 600,
                4: 800,
                5: 1000 }
        }),
    #Free parking
    Special("Free parking"),
    #Kentucky Avenue
    Property(
        {
            "name": "Kentucky Avenue",
            "set": "red",
            "price": 220,
            "houseprice": 150,
            "rent": {
                0: 18,
                1: 90, 
                2: 250, 
                3: 700,
                4: 875,
                5: 1050 }
        }),
    #Chance
    Draw("Chance"),
    #Indiana Avenue
    Property(
        {
            "name": "Indiana Avenue",
            "set": "red",
            "price": 220,
            "houseprice": 150,
            "rent": {
                0: 18,
                1: 90, 
                2: 250, 
                3: 700,
                4: 875,
                5: 1050 }
        }),
    #Illinois Avenue
    Property(
        {
            "name": "Illinois Avenue",
            "set": "red",
            "price": 240,
            "houseprice": 150,
            "rent": {
                0: 20,
                1: 100, 
                2: 300, 
                3: 750,
                4: 925,
                5: 1100 }
        }),
    #B. & O. Railroad
    Property(
        {
            "name": "B. & O. Railroad",
            "set": "railroads",
            "price": 200,
            "rent": {
                0: 25,
                1: 50, 
                2: 100, 
                3: 200 }
        }),
    #Atlantic Avenue
    Property(
        {
            "name": "Atlantic Avenue",
            "set": "yellow",
            "price": 260,
            "houseprice": 150,
            "rent": {
                0: 22,
                1: 110, 
                2: 330, 
                3: 800,
                4: 975,
                5: 1150 }
        }),
    #Ventnor Avenue
    Property(
        {
            "name": "Ventnor Avenue",
            "set": "yellow",
            "price": 260,
            "houseprice": 150,
            "rent": {
                0: 22,
                1: 110, 
                2: 330, 
                3: 800,
                4: 975,
                5: 1150 }
        }),
    #Water Works
    Property(
        {
            "name": "Water Works",
            "set": "utilities",
            "price": 150
        }),
    #Marvin Gardens
    Property(
        {
            "name": "Marvin Gardens",
            "set": "yellow",
            "price": 280,
            "houseprice": 150,
            "rent": {
                0: 24,
                1: 120, 
                2: 360, 
                3: 850,
                4: 1025,
                5: 1200 }
        }),
    #Go to jail
    Special("Go to prison"),
    #Pacific Avenue
    Property(
        {
            "name": "Pacific Avenue",
            "set": "green",
            "price": 300,
            "houseprice": 200,
            "rent": {
                0: 26,
                1: 130, 
                2: 390, 
                3: 900,
                4: 1100,
                5: 1275 }
        }),
    #North Carolina Avenue
    Property(
        {
            "name": "North Carolina Avenue",
            "set": "green",
            "price": 300,
            "houseprice": 200,
            "rent": {
                0: 26,
                1: 130, 
                2: 390, 
                3: 900,
                4: 1100,
                5: 1275 }
        }),
    #Community Chest
    Draw("Community Chest"),
    #Pennsylvania Avenue
    Property(
        {
            "name": "Pennsylvania Avenue",
            "set": "green",
            "price": 320,
            "houseprice": 200,
            "rent": {
                0: 28,
                1: 150, 
                2: 450, 
                3: 1000,
                4: 1200,
                5: 1400 }
        }),
    #Short Line
    Property(
        {
            "name": "Short Line",
            "set": "railroads",
            "price": 200,
            "rent": {
                0: 25,
                1: 50, 
                2: 100, 
                3: 200 }
        }),
    #Chance
    Draw("Chance"),
    #Park Place
    Property(
        {
            "name": "Park Place",
            "set": "darkblue",
            "price": 350,
            "houseprice": 200,
            "rent": {
                0: 35,
                1: 175, 
                2: 500, 
                3: 1100,
                4: 1300,
                5: 1500 }
        }),
    #Luxury Tax
    Special("Luxury tax", value=100, tax=True),
    #Boardwalk
    Property(
        {
            "name": "Boardwalk",
            "set": "darkblue",
            "price": 400,
            "houseprice": 200,
            "rent": {
                0: 50,
                1: 200, 
                2: 600, 
                3: 1400,
                4: 1700,
                5: 2000 }
        })
]