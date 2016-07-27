
""" Allows us to draw """


try:
    # python 2
    from Tkinter import *
except:
    pass
try:
    # python 3
    from tkinter import *
except:
    pass
# Which city we are current updating
from citiesandcolors import *
from citylocs import CityLocs

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
    print(nx, ny, city, color)
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








    
