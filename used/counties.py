import pandas as pd
import requests

df = pd.read_csv('docs/07-01-2021.csv')
df = df[df['Country_Region'] == 'US']

df.sort_values(by='Confirmed', ascending=False, inplace=True)

index_names = df['Out of' in df['Admin2'] or df['Admin2'] == 'Unassigned'].index
df.drop(index_names, inplace=True)

df = df[~df.Admin2.str.contains('Out of', na=False)]
df = df[~df.Admin2.str.contains('Unassigned', na=False)]

counties = df[['Admin2', 'Province_State', 'FIPS']]

counties = counties[~counties.FIPS.isnull()]

counties = counties.astype({'FIPS': int})

# counties.to_csv('docs/counties.csv', index=False)
