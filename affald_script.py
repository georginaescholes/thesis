from datetime import datetime,date
import pandas as pd
import os
os.chdir('C:/Users/Bruger/Anaconda3/envs/thesis_real/affald')

#read waste weight data into script, skip extra headers and footers, concat
#affald_jan = pd.read_csv("affald_jan.csv", skiprows=6)
affald_feb = pd.read_csv("affald_feb.csv", skiprows=6)
# affald_months = [affald_jan, affald_feb]
# affald_all = pd.concat(affald_months)

#global variable containing list of route names
rute_names = []

#iterate through csv to find route names
for index, a in affald_feb.iterrows():

    rute_name = ''

    if str(a['Registrering']) == 'nan':
        print(a)
        break

    if a['Bil Reg Nr'] == 'DG88 270':
        rute_name = 'Rute 1'
    elif a['Bil Reg Nr'] == 'Ny bil':
        rute_name = 'Rute 2'
    elif a['Bil Reg Nr'] == 'UT91093 - rute3':
        rute_name = 'Rute 3'
    elif a['Bil Reg Nr'] == 'VJ97837':
        rute_name = 'Rute 4'
    else:
        rute_name = 'other'

    #convert date strings to datetime format
    d = datetime.strptime(a['Dato'], '%d-%m-%Y %H:%M')
    if d.isoweekday() == 1:
        rute_name += ' Mandag'
    elif d.isoweekday() == 2:
        rute_name += ' Tirsdag'
    elif d.isoweekday() == 3:
        rute_name += ' Onsdag'
    elif d.isoweekday() == 4:
        rute_name += ' Torsdag'
    else:
        rute_name += ' Fredag'

    if d.isocalendar()[1] % 2 == 0:
        rute_name += ' Lige uger'
    else:
        rute_name += ' Ulige uger'

    rute_names.append(rute_name)

#add empty string to route names column to match index length
rute_names.append('')
affald_feb['rute_name'] = rute_names

affald_feb.to_csv('affald_feb_routes.csv')

