import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dependencies import *

path = Path('data/covid.csv')

covid_df = pd.read_csv(path)
df = covid_df[['fips', 'Lat', 'Long_']].groupby('fips').mean()

counties = counties.merge(df, on='fips', how='left')
counties.rename(columns={'Lat': 'latitude', 'Long_': 'longitude'}, inplace=True)

counties.to_csv('data/newcounties.csv', index=False)
