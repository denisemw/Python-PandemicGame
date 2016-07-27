
""" Implement the next part of the text-only version of the Pandemic game.  
    This currently can't handle role cards, graphics, epidemics or outbreaks.
"""


n = ""
import sys  # Allow us access to the command-line variables
import random # so we can shuffle
from outbreak import *

##from drawing import *

# Global variables

DEBUG = False  # By default, do not turn on output of variables
ShuffleSeed = 1  # Same seed always, unless we change it
Players = 0       # Number of Players in the game

# Infection Cards
InfectionDrawPile    = [] 
InfectionDiscardPile = []  # black cards
InfectionRateIndicator = None
InfectionRates = []

# Role Cards
AllRoles = ['dispatcher', 'medic', 'operations expert', 'researcher', 
            'scientist']
PlayerRoles = []

from citiesandcolors2 import *  # bring in all Adjacencies and color info

# Player related info
PlayerCards = []  # one sublist for each player
PlayerDeck  = []  # The cards on the board to draw from
PlayerDiscardPile = []   # Where we discard
Locations = []

# The Status of all the diseases
# Will become 'cured' or 'eradicated'
DiseaseStatus = { 'blue': None, 'black':None, 'yellow':None, 'red':None }

# Graphics stuff
Root = None
Can  = None
Im   = None
Photo = None


def init_draw_map () :
   """ Set-up graphics """
   global Root, Can, Im, Photo

   Root = Tk()
   Can = Canvas(Root, height=710, width=1000)
   Im = PhotoImage(file="/home/rts/ista130/Resources/nearfinalboard2.ppm")
   Photo = Can.create_image(0,0,anchor=NW, image=Im)

   draw_cities()

   Can.pack()
   Root.update()

def draw_cities () :
    """ Draw the city text """
    for city, (x,y) in CityLocs.iteritems() :
        Can.create_text(x+5, y-5, text=city, font="monospace-7",
                        fill="white", disabledfill="blue",
                        activefill="green", anchor=CENTER)



# For adding and maybe handling an outbreak
def adding_cube(can, city) :
   status = add_cube_to_city(can, city)
   if status == "outbreak" :
      outbreak(can, city, get_card_color(city))


# Set-Up Functions
# These are the specific 12 step setup functions

def step01 () :
   """Step 1: Place the board in the center of the table within easy
   reach of all the players"""
   global Players, Locations
   if DEBUG: print 'Step 1'
   
   # Get the number of players
   while 1 :
      Players = raw_input("How many players?").strip()
      if not Players.isdigit() :
         print "That's not a number: try again ..."
         continue
      Players = int(Players)
   
      if Players<2 :
         print 'Too few players: min 2, try again ...'
      elif Players > 4 :
         print 'Too many players: max 4, try again ...'
      else :
         break

   # Fill in a few things
   Locations = ["atlanta"] * Players

   # Draw map!
   init_draw_map ()

   # Draw player tokens
   player_colors = ["orange", "cyan", "purple", "white"]
   for player in range(Players) :
      initialize_player_token(Can, player, player_colors[player])

def step02 () :
   """Step 2: Assign the role cards"""
   if DEBUG: print 'Step 2'
   global AllRoles, PlayerRoles
   shuffle(AllRoles)
   PlayerRoles = AllRoles[:Players]   

   if DEBUG: print '..PlayerRoles = '+str(PlayerRoles)

def step03 () :
   """Step 3: Place initial research stations"""
   if DEBUG: print 'Step 3'
   global ResearchStations
   ResearchStations = ['atlanta'] + [None]*5
   if DEBUG: print '..ResearchStations = '+str(ResearchStations)

def step04 () :
   """Step 4: Initialize """
   if DEBUG: print 'Step 4'
   global Outbreaks, InfectionRateIndicator, InfectionRates
   Outbreaks = 0
   InfectionRateIndicator = 0
   InfectionRates = [2,2,2,3,3,4,4]
   Cures = [None, None, None, None]
   if DEBUG: print '..Outbreaks = '+str(Outbreaks)
   if DEBUG: print '..InfectionRateIndicator = '+str(InfectionRateIndicator)
   if DEBUG: print '..InfectionRates = '+str(InfectionRates)
   if DEBUG: print '..Cures = '+str(Cures)

def step05 () :
   """Step 5: Separate out disease cubes"""
   if DEBUG: print 'Step 5'
   global CubesOffBoard, CubesOnBoard
   for city in Cities :
      CubesOnBoard[city] = { 'red':0, 'black':0, 'yellow':0, 'blue':0 }

   if DEBUG: print "..CubesOffBoard = "+str(CubesOffBoard)
   if DEBUG: print "..CubesOnBoard = "+str(CubesOnBoard)

def step06 () :
   """Step 6: Pull out the 6 epidemic cards an set them aside"""
   if DEBUG: print 'Step 6'
   pass

def step07 () :
   """Step 7: Shuffle the remaining Player Cards (with blue backs and deal them
   to the players: 6 - players"""
   if DEBUG: print 'Step 7'
   global Specials, PlayerDeck, PlayerCards
   Specials = [ 'special:airlift' , 'special:forecast', 
                'special:government grant', 'special:one quiet night',
                'special:resilient population' ]
   PlayerDeck = Cities[:] + Specials

   # shuffle the player deck 
   shuffle(PlayerDeck)

   cards_to_each_player = 6 - Players
   PlayerCards = []
   for player in range(Players) :
      single_player_deck = GPlayerDeck(player, Root, [])
      for n in range(cards_to_each_player) :
         card = PlayerDeck.pop()
         single_player_deck.append(card)
      PlayerCards.append(single_player_deck)
   if DEBUG: print '..PlayerCards = '+str(PlayerCards)
   if DEBUG: print '..PlayerDeck = '+str(PlayerDeck)


def step08 () :
   """Divide the remaining Player Cards into a number of different piles
   according to how difficult you'd like to make the game.  Make the piles
   as equal in size as possible"""
   if DEBUG: print 'Step 8'
   global Epidemics
   while 1 :
      gametype = raw_input("Do you want a Intro, Normal or Heroic game?")
      gametype = gametype.strip()   # Get rid of starting and ending spaces
      gametype = gametype.lower()   # Make a "cononical input"
      if gametype=="intro" :
         Epidemics = 4
         break
      elif gametype=="normal":
         Epidemics = 5
         break
      elif gametype=="heroic":
         Epidemics = 6
         break
      else :
         print n+ 'Illegal gametype, try again ...'


def step09 () :
   """Shuffle an epidemic card into each pile.  Stack the
   piles on top of each other to form the Player Draw Pile.
   If the piles aren't exactly the same size, stack them so that the
   larger piles are above the smaller piles.  Put an excess Epidemic
   cards back into the box
   """
   if DEBUG: print 'Step 9'
   global PlayerDeck
   
   # The PlayerDeck contains the rest of the card that have not
   # been dealt out.  These are the cards that have to be divided
   # into some decks.
   
   # Divide up the decks Equally
   which = 0
   separate_decks = []
   for x in range(Epidemics) :
      separate_decks.append([])
   while len(PlayerDeck) != 0 :
      card = PlayerDeck.pop()
      separate_decks[which].append(card)
      which = (which + 1) % Epidemics

   if DEBUG: print 'SeperateDecks', separate_decks

   # Add epidemic to each SeperateDeck and shuffle
   for i in range(Epidemics) :
      separate_decks[i].append("epidemic")
      shuffle(separate_decks[i])

   if DEBUG: print 'SeperateDecks after epidemic and huf', separate_decks

   # FInally, put them all back together
   PlayerDeck = []
   for i in range(Epidemics) :
      PlayerDeck += separate_decks[i]
   if DEBUG: print 'PlayerDeck', PlayerDeck

def step10 () :
   """Step 10: Shuffle the infection cards (with the green backs) and place 
   them face down to form the InfectionDrawPile"""
   if DEBUG: print 'Step 10'
   global InfectionDrawPile, InfectionDiscardPile
   InfectionDrawPile = Cities[:]
   shuffle(InfectionDrawPile)
   InfectionDiscardPile = []
   if DEBUG: print '..InfectionDrawPile = '+str(InfectionDrawPile)
   if DEBUG: print '..InfectionDiscardPile = '+str(InfectionDiscardPile)

def step11 () :
   """Step 11: Put the initial disease cubes on the board"""
   if DEBUG: print 'Step 11'

   # a) Draw 3 cards from the Infection Draw Pile and place them face up
   #     in the Infection Discard Pile.  For each card drawn, add 3 cubes 
   #     to each pictured city
   # b) Draw 3 more cards, but 2 cubes
   # c) Draw 3 more cards, but 1 cube
   for cubes in range(3, 0, -1) :
      for x in range(3) :

         # Move cards from draw to discard
         card = InfectionDrawPile.pop()
         InfectionDiscardPile.append(card)

         # Move appropriate cube on the board
         print ' '+str(card)+":", cubes, get_card_color(card), 'cubes'
         for to_add in range(cubes) :
            adding_cube(Can, card)  # Can't outbreak during set-up

   if DEBUG: print '..InfectionDrawPile = '+str(InfectionDrawPile)
   if DEBUG: print '..InfectionDiscardPile = '+str(InfectionDiscardPile)




def step12 () :
   """ The player who was most recently sick goes first """
   if DEBUG : print 'Step 12'
   # PlayerCards[0] = ['tokyo', "essen", "toronto", "atlanta", "milan", "madrid"]

 


# Mainloop helper functions
# These are functions the mainloop uses 

def draw_card(player) :
   """ Have the given player take a card from the Player Deck (white cards)."""
   # Draw a card

   # Not enough cards
   if len(PlayerDeck)==0 :
      print 'There are no more Player Cards.  PLAYERS LOSE!'
      sys.exit(1)

   card = PlayerDeck.pop()
   print 'Player', player, 'draws the card:', card
   if card == "epidemic" :
      handle_epidemic()
      return

   PlayerCards[player].append(card)
   print 'Player', player,'now has the cards', PlayerCards[player]

   # Possible that we may have too many cards
   handle_too_many_cards(player)
      

def play_infector() :
   """ Have the current player play the infector: I.e., draw the number of Infection cards (based on the current infection rate) and infect those cities. """
   ir = InfectionRates[InfectionRateIndicator]
   print 'The current Infection Rate is', ir
   print 'The cities to infect:'
   for x in range(ir) :
      card = InfectionDrawPile.pop()
      InfectionDiscardPile.append(card)
      
      color = get_card_color(card)
      adding_cube(Can, card)


# Actions Helper
def get_city() :
    """Helper function to get and validate a city."""
    to_city = raw_input()
    if to_city not in Cities :
        print 'That is not a valid city: Try again.'
        return None
    return to_city

def get_color() :
    """Helper function to get and validate a color."""
    color = raw_input()
    if color not in ['black', 'red', 'yellow', 'blue'] :
        print 'That is not a valid color. Try again.'
        return None
    return color


def handle_too_many_cards(player_number) :
    """
    Players have a hand limit of 7 cards.  If the number of cards in hand
    ever exceeds 7 as a result of drawing cards (or performing a share
    knowledge action), the player must immediately discard cards in excess
    to the Player Discard Pile.  Players may play Special Event Cards
    (including any they have just drawn) instead of discarding them, to
    help reduce their hand to 7.
    """
    cards = PlayerCards[player_number]
    while len(cards)>7 :
        print '!!! You are over 7 cards.  Here is your hand:',cards
        print 'You may choose "discard somecity" or "play special:blah"'
        inp = raw_input()
        words = inp.strip().split(" ", 1)
        if len(words)!=2 or words[0] not in ["discard","play"] :
            print "??? Unknown input"
            continue
        # Words okay, and some card to discard
        if words[1] not in cards :
            print "??? You don't have the", words[1],"card."
            continue
        if words[0] == "discard" :
            cards.remove(words[1])
            PlayerDiscardPile.append(words[1])
            continue
        else : # play special
            # TODO: Implement this
            PlayerDiscardPile.append(words[1])
            pass




# Actions
def action_drive(player) :
   """ Perform the drive action for the current player """

   # Get city to drive to 
   inp = raw_input("What city to drive to?")
   where_to = inp.lower().strip()
   current_city = Locations[player]

   if where_to not in Cities :
      print '*** Illegal City', where_to,':aborting drive'
      return False

   # Legal city, is it adjacent?

   elif where_to not in AdjacentCities[current_city] :
      print '*** City', where_to,'not adjacent to', current_city,':aborting drive'
      return False
   # Legal city, adjacent, make the move
   else :
      current_city = where_to
      print '... you have moved to', where_to
      #Locations[player] = current_city
      move_player_token(Locations, Can, player, current_city)
      return True

def action_direct_flight(player) :
    """
    (1) a. Play a card from your hand 
        b. and move your pawn to the pictured city.
    (2) Discard the card to the PlayerDiscardPile
    """
    # Play a card from your deck
    cards = PlayerCards[player]
    while 1 :
        print 'What card do you want to discard and move to that city?',
        city_card = raw_input()
        if city_card not in cards :
           print "You don't have that city card."
           return False
        elif city_card not in Cities :
           print "Not a city card"
           return False
        else :
           cards.remove(city_card)
           break

    # Move to pictured city
    print '...Moving player',player,'pawn to', city_card
    # Locations[player] = city_card
    move_player_token(Locations, Can, player, city_card)
    # Discard the card to the PlayerDiscardPile
    PlayerDiscardPile.append(city_card)
    return True


def action_charter_flight(player_number) :
    """
    (1) a. Play the card corresponding to your pawn's current location
        b.  and move to any city on the board.  
    (2) Discard the card to the PlayerDiscardPile
    """
    # Play a card from your deck
    cards = PlayerCards[player_number]
    current_city = Locations[player_number]
    if current_city not in cards :
        print "??? You can't do a charter flight: You don't have the ",current_city, "card."
        return False
    else :
        print "What city do you want to jump to?",
        to_city = get_city()
        if to_city==None :
            return False
        else :
            print '... Moving player', player_number, 'pawn to', to_city
            #Locations[player_number] = to_city
            move_player_token(Locations, Can, player_number, to_city)

            
            # Discard the card to the PlayerDiscardPile
            cards.remove(current_city)
            PlayerDiscardPile.append(current_city)
            return True


def action_shuttle_flight(player_number) :
    """
    If your pawn is in a city with a Research Station, move it to any
    city with a Research Station.
    """
    city = Locations[player_number]
    if city not in ResearchStations :
        print '??? You are not in a city with a Research Station. '
        return False

    if ResearchStations.count(None)==5 :
        print "??? There's only one research station, you can't shuttle anywhere"
        return False

    # In a city with research station, which one to move to?
    print ResearchStations
    while 1 :
        print 'Which city do you wish to move to?',
        city = get_city()
        if city==None :
            return False
        elif city in ResearchStations :
            break
        else :
            print '??? ', city, " doesn't have a Research Station"
            continue
    # Move
    #Locations[player_number] = city
    move_player_token(Locations, Can, player_number, city)
    print '... Moving player', player_number, 'pawn to', city
    return True



def action_pass(player) :
   """ Perform the pass actions for the current player """
   print '... You passed on this action'
   return True

def action_build_research_station(player_number) :
    """
    (1) a.Play the card corresponding to the city your pawn currently occupies,
        b. then place a Research Station in that city.
    (2) Discard that card to the PlayerDiscardPile. 
    (3) If there aren't any Research Stations left in the supply,
        select one of the Research Stations already in play and transfer
        it to the city your pawn occupies.
    """
    # Play a card from your deck
    cards = PlayerCards[player_number]
    role  = PlayerRoles[player_number]
    current_city = Locations[player_number]
    if current_city not in cards :
        print "??? You can't build a research station: You don't have the ",current_city, "card."
        return False
    elif current_city in ResearchStations :
        print "??? There is already a research station here in", current_city
        return False

    # Assertion: now we can build one
    if None in ResearchStations : # free ResearchStation
        where = ResearchStations.index(None)
        ResearchStations[where] = current_city
    else :
        print '!!! All 6 research stations are on board: You have to move one.'
        print 'Which one will you move to the current city (',current_city,')?'
        print ResearchStations
        move_me = get_city()
        if move_me is None :
            return False
        where = ResearchStations.index(move_me)
        ResearchStations[where] = current_city

    # Discard city card 
    cards.remove(current_city)
    PlayerDiscardPile.append(current_city)

    print '... You have built a research station in', current_city
    return True



def action_discover_cure(player_number) :
    """ One your teams has discovered all cures, you win!
    (1) If your pawn is in a city with a Research Station, discard 5 cards
        of the same color to cure the corresponding disease.  
    (2) Take a Cure marker and place it (vial-side ip) on the Discovered
        Cures area of the board to indicate which disease has been cured.
    (3) Place the spent cards in the PlayerDiscardPile
    """
    current_city = Locations[player_number]
    cards = PlayerCards[player_number]
    if current_city not in ResearchStations :
        print '??? There is no research station here for a cure.'
        return False
    else :
        # Discard 5 cards of the same color
        print 'Which color do you want to cure (you have to discard 5 cards of that color)?'
        color = get_color()
        if color==None :
            print '??? Illegal color'
            return False
        # Count and make sure we have 5 cards of that color
        if DiseaseStatus[color] in ["cured", "eradicated"] :
            print '??? The',color,'disease is already cured.'
            return False
        color_count = 0
        for card in cards :
            if card.startswith("special") : continue
            if get_card_color(card)==color :
                color_count += 1
        if color_count < 5 :
            print "??? You don't have enough", color, "cards."
            return False
        # Assertion: You have enough color cards
        cards_to_discard = []
        count = 0
        while count<5 :
            print 'Card',count+1,' to discard?',
            city = get_city()
            if city==None :
                print '??? bad city'
                continue
            elif city not in cards :
                print '??? that city not in your hand ... try again'
                continue
            elif get_card_color(city) != color :
                print '??? that city is not ', color,' ... try again'
            else :
                cards_to_discard.append(city)
                count += 1
                cards.remove(city)
        # Have 5 cards
        print 'Are these the 5 cards you want to discard? (yes/no)',
        inp = raw_input()
        if inp=="yes" :
            PlayerDiscardPile.extend(cards_to_discard)
            DiseaseStatus[color] = 'cured'
            print '!!! You have cured', color
            if CubesOffBoard[color] == 12 :
                DiseaseStatus[color] = 'eradicated'
                print ' ... and eradicated it!'
            return True
        else :
            cards.extend(cards_to_discard)
            return False


def action_treat_disease(player_number) :
    """Over the course of the game, your team can treat diseases to buy the 
       time neeeded to discover cures.

       (1) Remove a disease cube from the city your pawn occupies.  
          (Each removed cube costs one action).  
       (2) Place the removed cube back into the stock by the side of the board
     
       If players have discovered a cure, instead
       of one cube, remove all cubes of a cured disease in your current
       city for one action.
    """
    current_city = Locations[player_number]
    print 'What color of disease do you wish to treat?',
    color = get_color()
    if color==None :
        print '??? Illegal color'
        return False
    cubes_here = CubesOnBoard[current_city][color]
    if cubes_here == 0 :
        print '??? There are no disease cubes of',color,'here to cure.'
        return False
    
    cubes_to_clean = 1 
    if DiseaseStatus[color] in ["cured", "eradicated"] :
        cubes_to_clean = cubes_here
        
    
    #CubesOnBoard[current_city][color] -= cubes_to_clean
    #CubesOffBoard[color] += cubes_to_clean
    for x in range(cubes_to_clean) :
       remove_cube_from_city(Can, current_city, color)
    print '... You cleaned', cubes_to_clean, color, 'off of', current_city
    return True



def action_share_knowledge(player_number) :
    """
    Transfer a card from one player to another.  Every card transferred
    counts 1 action.  Both your pawn and your fellow player's pawn must
    be in the same city, and you may only transfer the card of the city
    that you are in together.  If either holds more than 7 cards as a 
    result of the transfer, the excess cards must immediately be discarded
    to the Player Discard Pile
    """
    current_city = Locations[player_number]
    # Sanity check, anyone on your city?
    other_players_in_same_city = [] 
    for x in xrange(Players) :
        if x==player_number : continue
        if Locations[x] == current_city :
            other_players_in_same_city.append(x)
    if len(other_players_in_same_city)==0 :
        print '??? There are no other players here in', current_city
        return False
    
    # Which player do you want to trade with?
    print 'Which player number (0-',Players-1,') do you wish to trade with?'

    # Validate player
    other_player = raw_input().strip()
    if not other_player.isdigit() : 
       print '??? Which player?? Aborting...'
       return False
    other_player = int(other_player)
    if other_player>=Players :
       print '??? Not that many players ... Aborting ...'
       return False
    if other_player == player_number :
       print "??? You can't trade with yourself ... Aborting ..."
       return False

    if Locations[other_player] != current_city :
        print '??? Player', other_player, ' not in the same city with you.'
    
    # One of you has to have the city card of interest
    if current_city in PlayerCards[player_number] :
        # Trade from me to you
        PlayerCards[player_number].remove(current_city)
        PlayerCards[other_player].append(current_city)
        print '...', current_city,'moved from player',player_number,'to player', other_player
        handle_too_many_cards(other_player)
        return True
    elif current_city in PlayerCards[other_player] :
        # Trade from you to me
        PlayerCards[other_player].remove(current_city)
        PlayerCards[player_number].append(current_city)
        handle_too_many_cards(player_number)
        print '...', current_city,'moved from player',other_player,'to player',player_number
        return True
    else : 
        print '??? Neither player has the', current_city, 'card to trade'
        return False


def print_main_menu(player, actions) :
   """ Print the main menu for the current player, presenting him
   with the choice of actions he can type.  This main menu is basically
   the same main menu as from assignment 7."""
   
   # Print information about each city
   current_city = Locations[player]
   print PlayerCards[player]

   # Print adjacent cities
   print
   print '# Current City:', current_city
   print '# Adjacent Cities:',
   for city in AdjacentCities[current_city] :
       print city,
   print
   
   # Print the cubes in the city
   if current_city in CubesOnBoard :
      cubes_in_city = CubesOnBoard[current_city]
      for color,number in cubes_in_city.items() :
         if number>0 : print ' ',color,':',number

   print 'What do you want to do?'
   for options in sorted(actions) :
      print options



def handle_epidemic () :
    """
    Whenever a player draws an Epidemic card, 
    1. discard the card into the Player Discard Pile and do the following
       a. Increase the Infection rate:  Move the InfectorRate Indicator
           up by one on the Infection Rate Track on the board
       b. Infect:
           i) Take the bottom card from Infection Draw Pile 
           ii) and add 3 cubes to the city pictured in the on the card,
           iii) then place the card into the Infection Discard Pile.
           NOTE: No city can contain more than 3 cubes of any one
           color.  If the epidemic would cause the city to exceed that
           limit, any excess cubes are returned to the stock and an
           outbreak is triggered.  See rules for Outbreaks on page 7.

          iv) If there are not enough cubes to add to the board during
          an Epidemic, the game immediately ends in defeat for all players.
       c. Increase the intensity of infection
          i) Take the Infection Discard Pile, thoroughly shuffle it,
          ii) then place it on top of the remaining Infection Draw Pile.
              (Don't shuffle these cards into the Infection Draw Pile)
    """
    global InfectionRateIndicator, InfectionDiscardPile, InfectionDrawPile
    print "********* EPIDEMIC! ************"
    # 1. discard the card into the Player Discard Pile 
    #    a. Increase the Infection rate:  Move the InfectorRate Indicator up 1
    PlayerDiscardPile.append("epidemic")
    InfectionRateIndicator += 1

    #    b. Infect!
    #       i) Take *bottom card* from Infection Draw Pile
    #       ii) Add three cubes to the city pictures on the card
    #       iii) then place the card in the Infection Discard Pile
    card = InfectionDrawPile.pop(0)
    for x in range(3) :
       adding_cube(Can, card)
    InfectionDiscardPile.append(card)

    #     iv) If there are not enough cubes to add to the board during
    #         an Epidemic, the game immediately ends in defeat for all players.
    #if status :
    #    GameOver = True
    #    GameOverStatus = status

    #   c. Increase the intensity
    #      i) Take the Infection Discard Pile, throroughly shuffle it
    #      ii) then place it on top of the remaining Infection Draw Pile
    shuffle(InfectionDiscardPile)
    InfectionDrawPile.extend(InfectionDiscardPile) # Add to end
    InfectionDiscardPile = []                      # empty discard


def take_action (player, action_number) :
   """ Have the given player perform a single action (action number given).
   First, this function prints out the current player and action number, 
   as well as the main menu.  Then this function takes input from user
   as to which action to do next. """

   # The actions available
   actions = {'drive':           action_drive, 
              'direct flight':   action_direct_flight, 
              'charter flight':  action_charter_flight, 
              'shuttle flight':  action_shuttle_flight,
              'pass':            action_pass, 
              'build research station': action_build_research_station, 
              'discover cure':   action_discover_cure,
              'treat disease':   action_treat_disease, 
              'share knowledge': action_share_knowledge, 
              'quit': None}

   while 1 :
      print 'Player:', player,'taking action #', action_number
      print_main_menu(player, actions) # Print menu
      
      # Get input
      inp = raw_input('> ').strip().lower()

      if inp not in actions :
         print '**Illegal Action: try again**'
         continue

      if inp == 'quit': 
         sys.exit(1)              
      else :
         # Assertion: action valid .. execute!
         return actions[inp](player)  


def mainloop() :
   """ The main loop of the game """
   global Players
   
   # Main Loop of the Game
   game_over = False
   while not game_over :

      for player in range(Players) :

         # Take 4 actions
         for action_number in range(4) :

            # Some actions may end up being invalid or just showing info
             action_valid = False
             while not action_valid :
                 action_valid = take_action(player, action_number)
         
         # Draw 2 cards
         for cards in range(2) :
            draw_card(player)

         # Play infector
         play_infector() 


if __name__ == "__main__" :

   # The command line 
   options = sys.argv
   if len(options) > 3 :
      print 'usage: assign8.py [DEBUG [seed]]'
      print '   where DEBUG turns on printing of variable'
      print '   where seed sets a seed for the card shuffling'
      sys.exit(1)
   elif len(options) == 3 :
      if options[2]=="None" : 
         DoNotShuffle = True
      else :
         ShuffleSeed = int(options[2])
      if "DEBUG"==options[1] :
         DEBUG = True

   elif len(options)== 2:
      if "DEBUG"==options[1] :
         DEBUG = True

   # Set the random number sequence
   random.seed(ShuffleSeed)

   # Set-up then main loop!
   step01()
   step02()
   step03()
   step04()
   step05()
   step06()
   step07()
   step08()
   step09()
   step10()
   step11()
   step12()

   mainloop()

