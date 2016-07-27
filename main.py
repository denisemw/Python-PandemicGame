

from drawing import *
from outbreak import *

CityIds = { }
root = Tk()
can = Canvas(root, height=710, width=1000)
im = PhotoImage(file="C:\\Users\\Simon\\Desktop\\assign9\\board.gif")
photo = can.create_image(0,0,anchor=NW, image=im)
can.pack()

# Label everything 
for text_label,(x,y) in CityLocs.items() :
    id = can.create_text(x+5, y-5, text=text_label, font="monospace-7", fill="white", disabledfill="blue", activefill="green", anchor=CENTER)
    CityIds[text_label] = (id, x, y)


def find_id(event) :

    global can
    text_id_tuple = can.find_closest(event.x, event.y)
    if len(text_id_tuple) == 0 :
        print('No city underneath')
        return None
    else :
        id = text_id_tuple[0]
        type_id = can.type(id)
        if type_id != "text" : return 

        city_text = can.itemcget(id, 'text')
        return city_text


def unclick(event) :
    "Other button"
    city = find_id(event)
    if not city : return

    # Get color
    color = get_color(city)

    # Get the normalized co-ordinates from CityLocs
    (nx,ny) = CityLocs[city]

    remove_cube_from_city(city, color, can=can)



def click(event) :
    "When user clicks on map"

    # Clicked on a city
    city = find_id(event)
    if not city : return

    # Get color
    color = get_color(city)

    # Get the normalized co-ordinates from CityLocs
    (nx,ny) = CityLocs[city]

    result = add_cube_to_city(city, color, can=can)
    if result=="outbreak" :
        outbreak(city, color, can)

        
can.bind('<Button-1>', click)
can.bind('<Button-3>', unclick)            


root.mainloop()


