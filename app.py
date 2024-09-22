import numpy as np
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata

# Define your API key and endpoint
API_KEY = 'cf240851b8734d99add194144240802'
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

# Define grid points (cities with lat/lon for each state)
grid_points = {
    # Alabama
    'Birmingham': (33.5200, -86.8025),
    'Montgomery': (32.3668, -86.29997),
    'Huntsville': (34.7304, -86.5861),
    'Mobile': (30.6954, -88.0399),
    # Arizona
    'Phoenix': (33.4484, -112.0740),
    'Tucson': (32.2226, -110.9747),
    'Mesa': (33.4152, -111.8315),
    'Chandler': (33.3062, -111.8413),
    # Arkansas
    'Little Rock': (34.7465, -92.2896),
    'Fort Smith': (35.3859, -94.3985),
    'Fayetteville': (36.0822, -94.1574),
    'Jonesboro': (35.8423, -90.7081),
    # California
    'Los Angeles': (34.0522, -118.2437),
    'San Diego': (32.7157, -117.1611),
    'San Jose': (37.3382, -121.8863),
    'San Francisco': (37.7749, -122.4194),
    # Colorado
    'Denver': (39.7392, -104.9903),
    'Colorado Springs': (38.8339, -104.8214),
    'Aurora': (39.7294, -104.8319),
    'Fort Collins': (40.5853, -105.0844),
    # Connecticut
    'Hartford': (41.7658, -72.6734),
    'New Haven': (41.3083, -72.9279),
    'Bridgeport': (41.1865, -73.1952),
    'Stamford': (41.0534, -73.5387),
    # Delaware
    'Wilmington': (39.7392, -75.5398),
    'Dover': (39.1582, -75.5244),
    'Newark': (39.6837, -75.7493),
    'Middletown': (39.4413, -75.7162),
    # Florida
    'Miami': (25.7617, -80.1918),
    'Orlando': (28.5383, -81.3792),
    'Tampa': (27.9506, -82.4572),
    'Jacksonville': (30.3322, -81.6557),
    # Georgia
    'Atlanta': (33.4484, -84.3915),
    'Savannah': (32.0836, -81.0998),
    'Augusta': (33.4735, -82.0105),
    'Columbus': (32.4609, -84.9877),
    # Idaho
    'Boise': (43.6150, -116.2023),
    'Meridian': (43.6120, -116.3915),
    'Nampa': (43.5407, -116.5639),
    'Idaho Falls': (43.4916, -112.0339),
    # Illinois
    'Chicago': (41.8781, -87.6298),
    'Aurora': (41.7606, -88.3201),
    'Naperville': (41.7854, -88.1472),
    'Rockford': (42.2711, -89.0937),
    # Indiana
    'Indianapolis': (39.7684, -86.1581),
    'Fort Wayne': (41.0793, -85.1394),
    'Evansville': (37.9748, -87.5552),
    'South Bend': (41.6764, -86.2510),
    # Iowa
    'Des Moines': (41.5868, -93.6250),
    'Cedar Rapids': (41.9779, -91.6656),
    'Davenport': (41.5735, -90.5770),
    'Sioux City': (42.4935, -96.4003),
    # Kansas
    'Wichita': (37.6872, -97.3308),
    'Overland Park': (38.9822, -94.6708),
    'Kansas City': (39.0997, -94.5786),
    'Topeka': (39.0483, -95.6772),
    # Kentucky
    'Louisville': (38.2542, -85.7594),
    'Lexington': (38.0406, -84.5037),
    'Bowling Green': (36.9685, -86.4419),
    'Covington': (39.0834, -84.5088),
    # Louisiana
    'New Orleans': (29.9511, -90.0715),
    'Baton Rouge': (30.4443, -91.1896),
    'Shreveport': (32.5251, -93.7502),
    'Lafayette': (30.2241, -92.0198),
    # Maine
    'Portland': (43.6615, -70.2553),
    'Bangor': (44.8012, -68.7778),
    'Augusta': (44.3106, -69.7795),
    'Lewiston': (44.1009, -70.2148),
    # Maryland
    'Baltimore': (39.2992, -76.6099),
    'Columbia': (39.1732, -76.8464),
    'Silver Spring': (38.9906, -77.0292),
    'Germantown': (39.1710, -77.2719),
    # Massachusetts
    'Boston': (42.3601, -71.0589),
    'Worcester': (42.2626, -71.8023),
    'Springfield': (42.1015, -72.5898),
    'Cambridge': (42.3736, -71.1097),
    # Michigan
    'Detroit': (42.3314, -83.0458),
    'Grand Rapids': (42.9634, -85.6681),
    'Ann Arbor': (42.2808, -83.7430),
    'Lansing': (42.7335, -84.5555),
    # Minnesota
    'Minneapolis': (44.9833, -93.2669),
    'Saint Paul': (44.9442, -93.0931),
    'Rochester': (44.0121, -92.4802),
    'Duluth': (46.7867, -92.1005),
    # Mississippi
    'Jackson': (32.2988, -90.1848),
    'Gulfport': (30.3674, -89.0928),
    'Southaven': (34.9895, -90.0126),
    'Hattiesburg': (31.3271, -89.2905),
    # Missouri
    'Kansas City': (39.0997, -94.5786),
    'Saint Louis': (38.6270, -90.1994),
    'Springfield': (37.2153, -93.2982),
    'Columbia': (38.9519, -92.3341),
    # Montana
    'Billings': (45.7833, -108.5007),
    'Missoula': (46.8584, -113.9939),
    'Great Falls': (47.4946, -111.2833),
    'Bozeman': (45.6760, -111.0429),
    # Nebraska
    'Omaha': (41.2565, -95.9345),
    'Lincoln': (40.8136, -96.7026),
    'Bellevue': (41.1542, -95.8906),
    'Grand Island': (40.9250, -98.3420),
    # Nevada
    'Las Vegas': (36.1699, -115.1398),
    'Reno': (39.5294, -119.8128),
    'Henderson': (36.0395, -114.9817),
    'North Las Vegas': (36.1989, -115.1175),
    # New Hampshire
    'Manchester': (42.9956, -71.4548),
    'Nashua': (42.7655, -71.4676),
    'Concord': (43.2081, -71.5376),
    'Derry': (42.8859, -71.3037),
    # New Jersey
    'Newark': (40.7357, -74.1724),
    'Jersey City': (40.7178, -74.0431),
    'Paterson': (40.9176, -74.1718),
    'Elizabeth': (40.6639, -74.2243),
    # New Mexico
    'Albuquerque': (35.0844, -106.6504),
    'Santa Fe': (35.6869, -105.9378),
    'Las Cruces': (32.3199, -106.7637),
    'Rio Rancho': (35.2339, -106.6631),
    # New York
    'Albany': (42.6526, -73.7562),
    'Buffalo': (42.8864, -78.8784),
    'Rochester': (43.1566, -77.6088),
    'Syracuse': (43.0481, -76.1474),
    # North Carolina
    'Charlotte': (35.2271, -80.8431),
    'Raleigh': (35.7796, -78.6382),
    'Greensboro': (36.0726, -79.7910),
    'Durham': (35.9940, -78.8986),
    # North Dakota
    'Fargo': (46.8772, -96.7898),
    'Bismarck': (46.8083, -100.7837),
    'Grand Forks': (47.9239, -97.0582),
    'Minot': (48.2320, -101.2954),
    # Ohio
    'Columbus': (39.9612, -82.9988),
    'Cleveland': (41.4995, -81.6954),
    'Cincinnati': (39.1031, -84.5120),
    'Toledo': (41.6528, -83.5379),
    # Oklahoma
    'Oklahoma City': (35.4676, -97.5164),
    'Tulsa': (36.1539, -95.9928),
    'Norman': (35.2226, -97.4396),
    'Broken Arrow': (36.0609, -95.7860),
    # Oregon
    'Portland': (45.5155, -122.6793),
    'Salem': (44.9429, -123.0351),
    'Eugene': (44.0521, -123.0868),
    'Gresham': (45.5023, -122.4318),
    # Pennsylvania
    'Philadelphia': (39.9526, -75.1652),
    'Pittsburgh': (40.4406, -79.9959),
    'Allentown': (40.6084, -75.4909),
    'Erie': (42.1292, -80.0851),
    # Rhode Island
    'Providence': (41.8240, -71.4128),
    'Warwick': (41.7001, -71.4162),
    'Cranston': (41.7803, -71.4371),
    'Pawtucket': (41.8787, -71.3825),
    # South Carolina
    'Columbia': (34.0007, -81.0348),
    'Charleston': (32.7765, -79.9320),
    'North Charleston': (32.8546, -80.0169),
    'Mount Pleasant': (32.7957, -79.8282),
    # South Dakota
    'Sioux Falls': (43.5446, -96.7319),
    'Rapid City': (44.0805, -103.2310),
    'Aberdeen': (45.4647, -98.4869),
    'Brookings': (44.3010, -96.8076),
    # Tennessee
    'Nashville': (36.1627, -86.7816),
    'Memphis': (35.1495, -90.0490),
    'Knoxville': (35.9606, -83.9207),
    'Chattanooga': (35.0456, -85.3097),
    # Texas
    'Houston': (29.7604, -95.3698),
    'San Antonio': (29.4241, -98.4936),
    'Dallas': (32.7767, -96.7970),
    'Austin': (30.2672, -97.7431),
    # Utah
    'Salt Lake City': (40.7608, -111.8910),
    'West Valley City': (40.6916, -112.0011),
    'Provo': (40.2338, -111.6585),
    'West Jordan': (40.6097, -111.9385),
    # Vermont
    'Burlington': (44.4759, -73.2121),
    'Essex': (44.4934, -73.0967),
    'South Burlington': (44.4609, -73.2070),
    'Rutland': (43.5975, -72.9722),
    # Virginia
    'Virginia Beach': (36.8529, -75.9780),
    'Norfolk': (36.8508, -76.2859),
    'Chesapeake': (36.7682, -76.2875),
    'Richmond': (37.5407, -77.4360),
    # Washington
    'Seattle': (47.6062, -122.3321),
    'Spokane': (47.6586, -117.4260),
    'Tacoma': (47.2529, -122.4443),
    'Vancouver': (45.6387, -122.6615),
    # West Virginia
    'Charleston': (38.3498, -81.6326),
    'Huntington': (38.4192, -82.4452),
    'Morgantown': (39.6295, -79.9559),
    'Parkersburg': (39.2668, -81.5619),
    # Wisconsin
    'Milwaukee': (43.0389, -87.9065),
    'Madison': (43.0731, -89.4012),
    'Green Bay': (44.5192, -88.0194),
    'Kenosha': (42.5847, -87.8216),
    # Wyoming
    'Cheyenne': (41.1400, -104.8202),
    'Casper': (42.8485, -106.3300),
    'Laramie': (41.3112, -105.5911),
    'Gillette': (44.2916, -105.5022),
     'Toronto': (43.6510, -79.3470),
'Vancouver': (49.2827, -123.1207),
'Montreal': (45.5017, -73.5673),
'Calgary': (51.0447, -114.0719),
'Edmonton': (53.5461, -113.4938),
'Ottawa': (45.4215, -75.6972),
'Quebec City': (46.8139, -71.2082),
'Winnipeg': (49.8951, -97.1384),
'Halifax': (44.6488, -63.5752),
'Victoria': (48.4284, -123.3656),
'Kitchener': (43.4516, -80.4925),
'London': (42.9834, -81.2330),
'Richmond': (49.1666, -123.1335),
'Burnaby': (49.2488, -122.9806),
'Surrey': (49.1044, -122.8011),
'Markham': (43.8561, -79.3370),
'Guelph': (43.5501, -80.2482),
'Cambridge': (43.2001, -80.2432),
'Ajax': (43.8505, -79.0222),
'Whitby': (43.8835, -78.9415),
    'San Diego': (32.7157, -117.1611),
'Los Angeles': (34.0522, -118.2437),
'Santa Barbara': (34.4208, -119.6982),
'Cannon Beach': (45.8915, -123.9614),
'Seaside': (45.9866, -123.9295),
'Portland': (45.5128, -122.6793),  # Close to beach towns
'Seattle': (47.6062, -122.3321),
'Tacoma': (47.2529, -122.4443),
'Vancouver': (45.6387, -122.6615),
'Astoria': (46.1879, -123.8312),
    'Eureka': (40.8021, -124.1638),
'Bodega Bay': (38.3130, -123.0502),
'Big Sur': (36.2704, -121.8083),
    'La Push Beach': (47.5779, -124.6287),
'Rockaway Beach': (45.5887, -123.9702),
'Coos Bay': (43.3663, -124.2179),
'Gold Beach': (42.4075, -124.4051),
'Crescent City': (41.7550, -124.2005),
'Lompoc': (34.6391, -120.4579),
    'Key West': (24.5551, -81.7824),
'McAllen': (26.2034, -98.2300),
    'Stella Maris Airport': (23.3275, -75.0214),
'Andros Town': (25.0663, -77.8990),
'La Paz': (24.1426, -110.3126),
'Chihuahua': (28.6325, -106.0691),
'Monterrey': (25.6866, -100.3161),
'Hermosillo': (29.0720, -110.9559),
'Guaymas': (27.9256, -110.9003),
'Manzanillo': (19.0510, -104.3196),
    'Bahia Tortugas': (24.2144, -112.0160),
'San Carlos': (30.1619, -110.9451),
'Monticello': (37.8781, -109.3420),
'Montrose': (38.4794, -107.8783),
'Green River': (38.9931, -110.1627),
    'Sioux Falls': (43.5490, -96.7003),
'Rapid City': (44.0805, -103.2310),
'Pierre': (44.3682, -100.3516),
'Fargo': (46.8772, -96.7898),
'Bismarck': (46.8083, -100.7837),
'Grand Forks': (47.9253, -97.0377),
'Seattle': (47.6062, -122.3321),
'Spokane': (47.6586, -117.4260),
'Tacoma': (47.2529, -122.4443),
'Las Vegas': (36.1699, -115.1398),
'Reno': (39.5294, -119.8138),
'Carson City': (39.1638, -119.7674),
'Las Vegas': (36.1699, -115.1398),
'Reno': (39.5294, -119.8138),
'Carson City': (39.1638, -119.7674),
'Denver': (39.7392, -104.9903),
'Colorado Springs': (38.8339, -104.8214),
'Aurora': (39.7294, -104.8319),
'Billings': (45.7833, -108.5007),
'Missoula': (46.8586, -113.9870),
'Great Falls': (47.5002, -111.3008),
'Boise': (43.6150, -116.2023),
'Idaho Falls': (43.4916, -112.0334),
'Moscow': (46.7304, -116.9963),
'Salt Lake City': (40.7608, -111.8910),
'Provo': (40.2338, -111.6584),
'Ogden': (41.2215, -111.9738),
    'Isla Guadalupe Airport': (29.0343, -118.2190),
    'Edgartown': (41.3884, -70.5187),
    'Nantucket': (41.2835, -70.0995),
    'Weed': (41.4200, -122.3923),
    'Longview': (46.1381, -122.9346),
    'Medicine Hat': (50.0413, -110.6766),






}

# Function to fetch temperature data
def fetch_temperatures(cities):
    temps = {}
    for city, (lat, lon) in cities.items():
        response = requests.get(f'{BASE_URL}?key={API_KEY}&q={lat},{lon}')
        if response.status_code == 200:
            data = response.json()
            temps[city] = data['current']['temp_f']
    return temps

# Fetch the temperatures
temperatures = fetch_temperatures(grid_points)

# Prepare data for the map
lats = [grid_points[city][0] for city in grid_points]
lons = [grid_points[city][1] for city in grid_points]
temps = [temperatures[city] for city in grid_points]

# Create grid data
grid_lat, grid_lon = np.mgrid[min(lats):max(lats):100j, min(lons):max(lons):100j]
grid_temps = griddata((lats, lons), temps, (grid_lat, grid_lon), method='cubic')

# Set up the map
plt.figure(figsize=(12, 8))
map = Basemap(projection='lcc', resolution='h', lat_0=37.5, lon_0=-96, width=5E6, height=3E6)
map.shadedrelief()

# Draw states and boundaries
map.drawcoastlines()
map.drawcountries()
map.drawstates()

# Plot the temperature data
contour = map.contourf(grid_lon, grid_lat, grid_temps, cmap='coolwarm', latlon=True)

# Add a color bar
plt.colorbar(contour, orientation='horizontal', pad=0.05, label='Temperature (°F)')

# Show the map
plt.title('Temperature Map of Selected US Cities')
plt.show()
