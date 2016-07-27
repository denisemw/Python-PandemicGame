
""" Put together the "outbreak" aspect of Python """

from citiesandcolors2 import *
import sys
import time

Outbreaks = 0 


from Tkinter import *
# Which city we are current updating
from citiesandcolors2 import *
from citylocs import CityLocs
from time import sleep

# A place to remember all the IDs of the canvas objects
CubeIds = { }
CubeTextIds = { }
for city in Cities :
    CubeTextIds[city] = {'red':None, 'blue':None, 'black':None, 'yellow':None }
    CubeIds[city] = {'red':None, 'blue':None, 'black':None, 'yellow':None }


def space_to_draw_cube(city, color) :
    """ FInd the x,y of the city, then find where I would draw a cube of 
    the appropriate color"""
    (x,y) = CityLocs[city]
    ColorOffsets = {'red':(0,0),'blue': (15,0),'black':(0,15),'yellow':(15,15)}
    return (x + ColorOffsets[color][0], y + ColorOffsets[color][1])
    

def draw_cube_on_board(can, city, color) :
    """ If there is no cube of that color on the city"""

    (nx, ny) = space_to_draw_cube(city, color) 
    # print nx, ny, city, color
    size = 15

    # Draw all disease cubes tokens, saving the ids in the list
    if CubeIds[city][color] == None :
        # draw the appropriate color square with the a number in there
        id = can.create_rectangle(nx, ny, nx+size, ny+size, fill=color)
        CubeIds[city][color] = id
        
        # create a text thingee to print there
        fill_color = 'white'
        if color=='yellow' : fill_color = 'black' 
        text_id = can.create_text(nx, ny, text="7777777", font="monospace-6", 
                                  fill=fill_color, anchor = NW)
        CubeTextIds[city][color] = text_id

    # Assertion: the color background is there, and a text thingee is installed
    
    # Just output the number
    text_id = CubeTextIds[city][color]
    can.itemconfigure(text_id, text=str(CubesOnBoard[city][color]))


def undraw_cube_on_board(can, city, color) :
    """Undraw the cube and color """

    id = CubeIds[city][color]
    CubeIds[city][color] = None
    can.delete(id)
    text_id = CubeTextIds[city][color]
    CubeTextIds[city][color] = None
    can.delete(text_id)

    

def add_cube_to_city(can, city, color=None) :
    """Attempt to add a cube of the given color (if the color is None, 
    it uses the cube color of the given city) to the given city.  If the 
    given city already has three cubes, this returns the string "outbreak" 
    indicating we couldn't add the cube to the given city because there 
    was an outbreak.  If the cube was successfully added, then this 
    returns the string "success" indicating we successfully moved a cube 
    from off board onto the city.  It's also possible, when trying to 
    take a cube from off the board, that we run out.  In that case, we 
    should return the string "nocubes".  We assume that color and city 
    are legal.
    """

    # Get color
    if color==None : color = get_card_color(city)
    
    if CubesOffBoard[color] == 0 :
        print '*** No more cubes of',color,":aborting ... "
        print "PLAYERS LOSE!"
        sys.exit(1)
        return 'nocubes'
    elif CubesOnBoard[city][color] == 3 :
        print "*** Outbreak!"
        return "outbreak"
    else :
        print '...moving',color,'cube to',city
        CubesOffBoard[color] -= 1
        CubesOnBoard[city][color] += 1
        if can : draw_cube_on_board(can, city, color) 
        return 'success'
            

def remove_cube_from_city(can, city, color=None) :
    
    # Get color
    if color==None : color = get_color(city)
    
    if CubesOnBoard[city][color] == 0 :
        print '*** No more cubes of',color,'on',city,':aborting'
        return 'nocubes'
    else :
        print '...moving',color,'cube offboard'
        CubesOffBoard[color] += 1
        CubesOnBoard[city][color] -= 1

        # Either update or undraw
        if CubesOnBoard[city][color] == 0 :
            if can != None : 
                undraw_cube_on_board(can, city, color)
        else :
            if can != None : 
                draw_cube_on_board(can, city, color)

        return 'success'


def outbreak (can, current_city, color) :
    """The given city has outbroken.  We perform the outbreak, infecting 
    cities around us (potentially again and again).  Once a city has had an
    outbreak, then the city will not outbreak again this turn. If we run 
    out of cubes, we return False indicating the game is over.  Otherwise 
    we return True after having performed multiple outbreaks.
    """
    global Outbreaks

    Outbreaks += 1

    # Initialize the work queues: there are cities to infect.  Once a 
    # city has had an outbreak, you don't reinfect it, so we need to keep
    # track of all cities that HAVE ALREADY outbroken so they won't
    # outbreak again.

    # To start, the current city was just about to outbreak (that's what
    # started the process!).  All of its neighbors need to be infected!
    cities_to_infect = list(AdjacentCities[current_city])
    cities_already_outbroken = [current_city]

    print 'cities_to_infect', cities_to_infect
    print 'cities_broke', cities_already_outbroken 
    
    # Note that this is color cube that gets tossed around:
    # During a particular instance of an outbreak ONLY THIS COLOR
    # cube is moving on the board.
    
    # Continue until all need cities have been infected
    while len(cities_to_infect) != 0 :
        
        # Get a city and infect it: 
        city_to_infect = cities_to_infect.pop()
        print 'city to infect', city_to_infect
        status = add_cube_to_city(can, city_to_infect, color)
        
        if status == "outbreak" :
            
            # Watch the number of them!
            Outbreaks += 1
            if Outbreaks ==8 : 
                print 'Too many outbreaks .. . Players Lose!'
                sys.exit(1)

            # If there's an outbreak, all adjacent cities 
            # THAT HAVE NOT HAD an outbreak, get scheduled for a cube  
            adjacent_cities = list(AdjacentCities[city_to_infect])
            for city in adjacent_cities :
                if city not in cities_already_outbroken :
                    cities_to_infect.append(city)
            
            cities_already_outbroken.append(city_to_infect)

        elif status == "nocubes" :
            return False

        elif status == "success" :
            # Cube was added, everything okay, no further things to do
            pass

        else :
            print "Unknown return code?"
            sys.exit(1)

    # Successfully outbroke without game ending
    return True

LocationsId = { }
def initialize_player_token(can, player, color) :
    x0, y0 = CityLocs["atlanta"]
    x = x0-5+player*10
    y = y0-5
    LocationsId[player] = can.create_oval(x,y,x+10, y+10, fill=color)

def move_player_token(Locations, can, player, to_city) :
    """Move player token from city to another"""
    from_city = Locations[player]
    player_id = LocationsId[player]
    x0,y0 = CityLocs[to_city]
    x = x0-5+player*10
    y = y0-5
    can.coords(player_id, x,y, x+10, y+10)
    Locations[player] = to_city
    can.update()

class GPlayerDeck(object) :
    def __init__(self, player, root, initial_cards) :
        self.cards = initial_cards
        self.root = root
        self.player = player 

        self.top = Toplevel(root)
        self.top.title = "Player "+str(player)
                       
        self.cards   = []
        self.buttons = []
        self.extend(initial_cards)

    def pop(self, which=-1) :
        """Remove the top card and return it"""
        card = self.cards.pop(which)
        button = self.button.pop(which)
        button.destroy()
        return card

    def append(self, card) :
        """Plop a card on top of the deck"""
        self.cards.append(card)
        color = get_card_color(card)
        if color==None : color = "orange"
        text_color = "white"
        if color=="yellow" : text_color = "black"
        button = Button(self.top, text=card, bg=color, foreground=text_color)
        button.pack()
        self.buttons.append(button)

    def remove(self, card) :
        """Remove a particular card from the deck."""
        where = self.cards.index(card)
        self.cards.pop(where)
        button = self.buttons[where]
        self.buttons.pop(where)
        button.destroy()

    def extend(self, cards) :
        """Add a bunch of cards in"""
        for x in cards :
            self.cards.append(x)
            color = get_card_color(x)
            if color==None : color = "orange"
            text_color = "white"
            if color=="yellow" : text_color = "black"
            button = Button(self.top, text=x, bg=color, fg=text_color)
            button.pack()
            self.buttons.append(button)

    def __str__(self) :
        """ stringize just the list"""
        return str(self.cards) 

    def __len__(self) :
        return len(self.cards)

    def __contains__(self, item) :
        return item in self.cards

if __name__=="__main__" :

    # 3 blue on Atlanta
    for x in range(3) :
        add_cube_to_city("atlanta", "blue")
        
    # 2 blue on Chicago
    for x in range(2) :
        add_cube_to_city("chicago", "blue")

    # 2 yellow cubes on Miami
    for x in range(2) :
        add_cube_to_city("chicago", "yellow")


    print outbreak("atlanta", "blue")
    time.sleep(1)
    print outbreak("atlanta", "blue")
    time.sleep(1)
    print outbreak("atlanta", "blue")
    time.sleep(1)
    print outbreak("atlanta", "blue")
    time.sleep(1)
