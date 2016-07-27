
""" Just the City Locations """

"""
CityLocs = [('beijing', 782, 236), ('seoul', 859, 234), ('tokyo', 922, 271), ('shanghai', 787, 295), ('osaka', 919, 326), ('hong kong', 806, 348), ('taipei', 877,342), ('manila', 877, 420), ('sydney', 928, 546), ('jakarta', 761, 462), ('ho chi', 812, 418), ('bankok', 756, 391), ('johannesburg', 513, 518), ('khartoum', 531,401), ('lagos', 441, 403), ('kinshasa', 477, 457), ('sao paulo', 309, 501), ('lima', 172, 485), ('santiago', 197, 563), ('buenos aires', 273, 548), ('bogota', 212, 414), ('miami', 219, 355), ('mexico city', 128, 368), ('los angeles', 63, 337), ('san francisco', 50, 283), ('chicago', 125, 245), ('toronto', 195, 250), ('new york', 267, 245), ('atlanta', 166, 304), ('washington', 249, 302), ('madrid', 374, 283), ('london', 381, 200), ('paris', 438, 242), ('essen', 457, 181), ('milan', 500, 230), ('st petersburg', 529, 169), ('algiers', 442, 322), ('cairo', 506, 343), ('riyahd', 583, 369), ('chennai', 700, 426), ('mumbai2', 643, 391), ('moscow', 579, 209), ('tehran', 628, 256), ('delhi', 696, 296), ('kolkata', 753, 318), ('istanbul', 522, 275), ('baghdad', 584, 302), ('karachi', 642, 320)]


CityLocsDict = { }
for city, x,y in CityLocs :
    CityLocsDict[city] = (x, y)

from pprint import pprint

pprint(CityLocsDict)
"""

CityLocs = {
 'algiers': (442, 322),
 'atlanta': (166, 304),
 'baghdad': (584, 302),
 'bangkok': (756, 391),
 'beijing': (782, 236),
 'bogota': (212, 414),
 'buenos aires': (273, 548),
 'cairo': (506, 343),
 'chennai': (700, 426),
 'chicago': (125, 245),
 'delhi': (696, 296),
 'essen': (457, 181),
 'ho chi mihn city': (812, 418),
 'hong kong': (806, 348),
 'istanbul': (522, 275),
 'jakarta': (761, 462),
 'johannesburg': (513, 518),
 'karachi': (642, 320),
 'khartoum': (531, 401),
 'kinshasa': (477, 457),
 'kolkata': (753, 318),
 'lagos': (441, 403),
 'lima': (172, 485),
 'london': (381, 200),
 'los angeles': (63, 337),
 'madrid': (374, 283),
 'manila': (877, 420),
 'mexico city': (128, 368),
 'miami': (219, 355),
 'milan': (500, 230),
 'moscow': (579, 209),
 'mumbai': (643, 391),
 'new york': (267, 245),
 'osaka': (919, 326),
 'paris': (438, 242),
 'riyadh': (583, 369),
 'san francisco': (50, 283),
 'santiago': (197, 563),
 'sao paulo': (309, 501),
 'seoul': (859, 234),
 'shanghai': (787, 295),
 'st petersburg': (529, 169),
 'sydney': (928, 546),
 'taipei': (877, 342),
 'tehran': (628, 256),
 'tokyo': (922, 271),
 'toronto': (195, 250),
 'washington': (249, 302)}
