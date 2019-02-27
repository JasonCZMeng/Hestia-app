from craigslist import CraigslistHousing

SITE = 'vancouver'
AREA = 'bnc'
CATEGORY = 'roo'

MIN_PRICE = 750
MAX_PRICE = 1000
HAS_IMAGE = True

LIMIT = 50

# collect data
cl_h = CraigslistHousing(site=SITE, area=AREA, category=CATEGORY,
                         filters={'min_price': MIN_PRICE, 'max_price': MAX_PRICE,
                                  'private_room': True, 'has_image': HAS_IMAGE})

# store collected data in temporary storage (a list)

listings = []

for result in cl_h.get_results(sort_by='newest', geotagged=True, limit=LIMIT):
    # only get fresh postings
    if result.get('repost_of') is None:
        listing = {
            'name': result.get('name'),
            'price': result.get('price'),
            'url': result.get('url'),
            'lat': result.get('geotag')[0],
            'lon': result.get('geotag')[1],
            'address': result.get('where')
        }
        listings.append(listing)

# filter collected data against specific geographical points
# get points from https://boundingbox.klokantech.com/

my_new_west = [-122.91671, 49.199793, -122.905336, 49.205746]
my_lougheed = [-122.90098, 49.243321, -122.888314, 49.250336]
filter_boxes = [my_new_west, my_lougheed]


def in_box(lat, lon, boxes):
    for box in boxes:
        lat_in = box[1] < lat < box[3]
        lon_in = box[0] < lon < box[2]
        if lat_in and lon_in:
            return True
    return False


filtered_listings = list(filter(lambda l: in_box(l.get('lat'), l.get('lon'), filter_boxes),
                                listings))

print(filtered_listings)
# the above might not output anything because our bounding boxes (gps filters) are small
# print(listings)

print("Your listings have been processed")
