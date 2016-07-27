
# All the adjacency information and color information

# Cities and color information
Cities = [
  # black cities
  'moscow', 'tehran', 'delhi', 'kolkata', 'chennai', 'mumbai', 
  'cairo', 'riyadh', 'algiers', 'istanbul', 'baghdad', 'karachi',
  # red cities
  'beijing', 'shanghai','hong kong', 'bangkok', 'jakarta', 'sydney',
  'manila', 'ho chi mihn city', 'taipei', 'osaka', 'tokyo', 'seoul',
  # blue cities
  'san francisco', 'chicago', 'atlanta', 'washington', 'toronto', 'new york', 
  'london', 'madrid', 'paris',  'essen', 'milan', 'st petersburg',
  # yellow cities
  'los angeles', 'mexico city', 'miami', 'bogota', 'lima', 'buenos aires',
  'sao paulo', 'lagos', 'kinshasa', 'johannesburg', 'khartoum', 'santiago'
]

CityColors = {
  'black': [
        'moscow', 'tehran', 'delhi', 'kolkata', 'chennai', 'mumbai', 
        'cairo', 'riyadh', 'algiers', 'istanbul', 'baghdad', 'karachi'],
  'red' : [
        'beijing', 'shanghai','hong kong', 'bangkok', 'jakarta', 'sydney',
        'manila', 'ho chi mihn city', 'taipei', 'osaka', 'tokyo', 'seoul'],
  'blue' : [
        'san francisco', 'chicago', 'atlanta', 'washington', 'toronto','paris',
        'new york', 'london', 'madrid', 'essen', 'milan', 'st petersburg'],
  'yellow': [
        'los angeles', 'mexico city', 'miami', 'bogota', 'lima','buenos aires',
        'sao paulo', 'lagos', 'kinshasa', 'johannesburg','khartoum','santiago']

}

AdjacentCities = { 
  # black cities
  'moscow' : ['tehran', 'istanbul', 'st petersburg'],
  'tehran' : [ 'moscow', 'baghdad', 'karachi', 'delhi'],
  'delhi'  : [ 'tehran', 'karachi', 'mumbai', 'chennai', 'kolkata'],
  'kolkata': [ 'delhi', 'chennai', 'bangkok', 'hong kong'],
  'chennai': [ 'mumbai', 'delhi', 'kolkata', 'jakarta', 'bangkok' ],
  'mumbai' : [ 'karachi', 'delhi', 'chennai'],
  'cairo'  : [ 'algiers', 'istanbul', 'baghdad', 'riyadh', 'khartoum' ],
  'riyadh' : [ 'cairo', 'baghdad', 'karachi' ],
  'algiers': [ 'madrid', 'paris', 'istanbul', 'cairo' ],
  'istanbul':[ 'algiers', 'milan', 'st petersburg', 'moscow', 'baghdad', 'cairo'],
  'baghdad': [ 'istanbul', 'cairo', 'riyadh', 'karachi', 'tehran'],
  'karachi': [ 'riyadh', 'baghdad', 'tehran', 'delhi', 'mumbai'],
  # red cities
  'beijing': [ 'seoul', 'shanghai'],
  'shanghai':[ 'beijing', 'seoul', 'tokyo', 'taipei', 'hong kong'],
  'hong kong':['kolkata', 'shanghai','taipei','manila','ho chi mihn city','bangkok'],
  'bangkok': [ 'chennai', 'kolkata', 'hong kong', 'ho chi mihn city', 'jakarta'],
  'jakarta': [ 'chennai', 'bangkok', 'ho chi mihn city', 'sydney'],
  'sydney':  [ 'jakarta', 'manila', 'los angeles'],
  'manila':  [ 'sydney', 'ho chi mihn city', 'hong kong', 'taipei', 'san francisco'],
  'ho chi mihn city': ['jakarta', 'bangkok', 'hong kong', 'manila'],
  'taipei':  [ 'hong kong', 'shanghai', 'osaka', 'manila'],
  'osaka' :  [ 'taipei', 'tokyo' ],
  'tokyo' :  [ 'shanghai', 'seoul', 'osaka', 'san francisco' ],
  'seoul' :  [ 'beijing', 'shanghai', 'tokyo' ],
  # blue cities
  'san francisco': ['tokyo', 'manila', 'los angeles', 'chicago'],
  'chicago' : [ 'san francisco', 'los angeles', 'mexico city', 'atlanta', 'toronto'],
  'atlanta' : [ 'chicago', 'washington', 'miami' ],
  'washington':[ 'miami', 'atlanta', 'toronto', 'new york'],
  'toronto': ['chicago', 'new york', 'washington'],
  'new york': [ 'toronto', 'washington', 'london', 'madrid'],
  'london': [ 'new york', 'madrid', 'paris', 'essen'],
  'madrid': [ 'sao paulo', 'new york', 'london', 'paris', 'algiers'],
  'paris':  [ 'madrid', 'london', 'essen', 'milan', 'algiers'],
  'essen' : [ 'london', 'paris', 'milan', 'st petersburg'],
  'milan' : [ 'paris', 'essen', 'istanbul' ],
  'st petersburg' : ['essen', 'istanbul', 'moscow'],
  # yellow cities
  'los angeles' : ['sydney', 'san francisco', 'chicago', 'mexico city'],
  'mexico city': ['los angeles', 'chicago', 'miami', 'lima', 'bogota'],
  'miami': [ 'atlanta', 'washington', 'mexico city', 'bogota' ],
  'bogota' : [ 'mexico city', 'miami', 'lima', 'buenos aires', 'sao paulo'],
  'lima' : ['mexico city', 'bogota', 'santiago' ],
  'buenos aires' : ['bogota', 'sao paulo'],
  'sao paulo' : ['buenos aires', 'bogota', 'madrid', 'lagos'],
  'lagos' : [ 'sao paulo', 'kinshasa', 'khartoum'],
  'kinshasa' : ['lagos', 'khartoum', 'johannesburg'],
  'johannesburg': ['kinshasa', 'khartoum'],
  'khartoum' : [ 'cairo', 'lagos', 'kinshasa', 'johannesburg' ],
  'santiago' : [ 'lima' ],
}

CubesOnBoard = { }
for city in Cities :
    CubesOnBoard[city] = { 'red':0, 'black':0, 'yellow':0, 'blue':0 }
# print CubesOnBoard

CubesOffBoard = { 'red': 24, 'blue':24, 'black':24, 'yellow':24 }
DoNotShuffle = False

# Generic helper functions
# These are all helper functions that are used all over the game

import random

def shuffle(deck) :
   """ Shuffle the given deck:  this has the side effect of changing
       the given deck list"""
   global DoNotShuffle
   if DoNotShuffle : return

   shuffled_deck = []
   for x in range(len(deck), 0, -1) :
      shuffled_deck.append(deck.pop(random.randint(0,x-1)))
   deck[:] = shuffled_deck

def get_card_color(city) :
   """ Return the card color of the given city """
   for color, cities in CityColors.items() :
      if city in cities :
         return color

 

      
