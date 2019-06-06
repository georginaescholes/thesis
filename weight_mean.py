import pandas as pd

#read all monthly waste amounts into script
waste_jan_df = pd.read_csv('affald/affald_jan_routes.csv', dtype={'Netto (kg)': float})
waste_feb_df = pd.read_csv('affald/affald_feb_routes.csv', dtype={'Netto (kg)': float})

#calculate mean weights per month
mn_jan = waste_jan_df.groupby('rute_name')['Netto (kg)'].mean()
mn_feb = waste_feb_df.groupby('rute_name')['Netto (kg)'].mean()

routes = pd.read_csv('data/combined_geo_all.csv')

#join monthly mean columns to route data
result = routes.merge(mn_jan,left_on='RuteLabel', right_on='rute_name')\
    .merge(mn_feb,left_on='RuteLabel',right_on='rute_name')

print(result.isna().sum())

#find number of waste containers per route
result['count'] = \
    result.groupby('RuteLabel', as_index=False)['RuteLabel'].transform(lambda s: s.count())

#calculate average weight of containers per route
result['jan_p_e'] = result['Netto (kg)_x']/result['count']
result['feb_p_e'] = result['Netto (kg)_y']/result['count']
result.jan_p_e = result.jan_p_e.round(1)
result.feb_p_e = result.feb_p_e.round(1)

#drop invalid rows, i.e. rows without coordinates
result_clean = result.dropna(subset=['lat', 'lng'])
result_clean.rename(columns={'Netto (kg)_x':'jan_mean','Netto (kg)_y':'feb_mean'}, inplace=True)

result_clean.to_csv('mean_months.csv')

