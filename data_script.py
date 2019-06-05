import pandas as pd
import requests
import glob
import os
import time
start_time = time.time()
os.chdir('C:/Users/Bruger/Anaconda3/envs/thesis_real/data')

#Iterate all csv files in directory and save to one file
extension = 'csv'
all_filenames = [i for i in glob.glob('routes/*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=True)
combined_csv.to_csv('combined_all.csv')
print("Done combining files")
print("time elapsed: {:.2f}s".format(time.time() - start_time))

#Read combines csv to pandas data frame
df2 = pd.read_csv("combined_all.csv")

print("Done reading combined file")
print("time elapsed: {:.2f}s".format(time.time() - start_time))

#Create empty lists for coordinates
lat = []
lng = []

#Iterate through rows to match addresses with geocoder
for index, a in df2.iterrows():
    payload = {'vejnavn': a['Vejnavn'], 'husnr': a['Husnr'], 'postnr': 5500, 'struktur': 'mini'}
    res = requests.get('https://dawa.aws.dk/adgangsadresser/', params=payload)

    adrs_json = res.json()
    if len(adrs_json) > 0:
        address = adrs_json[0]
        lng.append(address.get('x', None))
        lat.append(address.get('y', None))
    else:
        lng.append(None) #Append coordinates to list variables above
        lat.append(None)
print("Done getting addresses")
print("time elapsed: {:.2f}s".format(time.time() - start_time))

#Append new columns to data frame
df2["lat"] = lat
df2["lng"] = lng

sogn_navn = []
for index, b in df2.iterrows():
    payload = {'x': b['lng'], 'y': b['lat']}
    result = requests.get('https://dawa.aws.dk/sogne/reverse/', params=payload)

    sogn_json = result.json()
    if len(sogn_json) > 0:
        sogn_navn.append(sogn_json.get('navn'))
    else:
        sogn_navn.append(None)  # Append parish to list variables above
print("Done getting sogne")
print("time elapsed: {:.2f}s".format(time.time() - start_time))

df2["sogn"] = sogn_navn

df2.to_csv("combined_geo_all.csv")
print("Done writing results")
print("time elapsed: {:.2f}s".format(time.time() - start_time))


