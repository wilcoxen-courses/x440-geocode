"""
nominatim.py
Spring 2022 PJW

Query Nominatim, the OpenStreetMap geocoding API.

Note that Nominatium often returns several results for known objects
near each address. If only the coordinates are needed, it should be
sufficient to pick any one. However, considerable additional detail
is available in the JSON object for each match.
"""

import requests
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

wgs84 = 4326

#
#  List of addresses to geocode
#

addresses = [
    "1600 pennsylvania ave nw, washington, dc",
    "734 S Crouse Ave, Syracuse, NY",
    "1 Infinite Loop, Cupertino, CA",
    "2700 W Anderson Ln., Austin, TX",
    "440 Terry Ave N, Seattle, WA"
    ]

#
#  Endpoint of the API
#

api = "https://nominatim.openstreetmap.org/search"

#
#  Loop through the addresses and build a list of results. Note
#  that there are usually multiple hits per address. Will need to
#  pick out the correct one by hand.
#

output = []

for a in addresses:

    #  Build the payload, set up a header to identify ourselves, and make
    #  the query

    payload = { 'q':f'<{a}>', 'format':'json' }
    headers = { 'user-agent': 'pai789/1' }

    response = requests.get(api,payload,headers=headers)

    assert response.status_code == 200

    #  Parse the result

    result = response.json()

    #  Print it for reference

    print( json.dumps(result, indent=4) )

    #  Pull out the key information and append it to the list

    for r in result:
        newaddr = {
            'query':a,
            'name':r['display_name'],
            'lat':r['lat'],
            'lon':r['lon']
            }
        output.append(newaddr)

#%%
#
#  Build a dataframe and write it out
#

adds = pd.DataFrame(output)
adds.to_csv('addresses.csv',index=False)

#%%
#
#  Read a US map for reference
#

us = gpd.read_file('locator_map.gpkg',layer='us')
us.to_file('demo.gpkg',layer='us')

#
#  Build a GeoDataFrame of the geocoded points
#

geom = gpd.points_from_xy(adds['lon'], adds['lat'])
geo = gpd.GeoDataFrame(data=adds, geometry=geom, crs=wgs84)
geo = geo.to_crs(us.crs)
geo.to_file('demo.gpkg',layer='addresses')

#
#  Now draw a quick map
#

fig,ax = plt.subplots(dpi=300)
us.boundary.plot(color='black', linewidth=0.4, ax=ax)
geo.plot(color='red', marker='D', markersize=20, ax=ax)
ax.axis('off')
fig.savefig('demo.png')
