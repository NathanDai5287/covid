from dependencies import *

from pollution import pollution
from covid import covid
from demographics import demographics
from weather import weather
from vaccination import vaccination

class Main:
	def pollution(bpollution: bool) -> pd.DataFrame:
		if (bpollution):

			pollution_df = pd.DataFrame()
			for i, location in counties.iterrows():
				if (isinstance(location['county'], float)): # filters out territories like Guam, American Samoa, etc.
					continue

				try:
					county_df = pollution(start_date, end_date, location)
				except:
					print(f"{location['county']}, {location['state']} failed")

					with open('failed.csv', 'a') as f:
						f.write(
							f"{location['county']}, {location['state']}, {location['fips']}\n"
						)

					continue

				pollution_df = pollution_df.append(county_df)

				if (i % 10 == 0):
					pollution_df.to_csv('data/pollution.csv')
					print(f'{i}/{total}')

			pollution_df['date'] = pd.to_datetime(pollution_df['date'], format='%m/%d/%Y')

			# checkpoints
			pollution_df.to_csv('data/pollution.csv')
			pollution_df.set_index(['date', 'state', 'county'], inplace=True)
			pollution_df.to_csv('data/pollution.csv')

		else:

			pollution_df = pd.read_csv('data/pollution.csv')
			# pollution_df = pd.read_csv('data/pollution.csv', parse_dates=['date'])
			pollution_df['date'] = pd.to_datetime(pollution_df['date'], format='%m/%d/%Y')

		pollution_df.rename(columns={'Lead (TSP) LC': 'lead', 'Carbon monoxide': 'carbon monoxide', 'Sulfur dioxide': 'sulfur dioxide', 'Nitrogen dioxide (NO2)': 'nitrogen dioxide', 'Ozone': 'ozone', 'PM10 - LC': 'PM10', 'PM2.5 - Local Conditions': 'PM2.5'}, inplace=True)

		pollutants = [i for i in pollution_df.columns if i not in {'date', 'state', 'county', 'fips'}]
		# pollution_df[['average ' + i for i in pollutants]] = pollution_df[['fips'] + pollutants].groupby('fips').mean()

		average_df = pollution_df[['fips'] + pollutants].groupby('fips').mean()
		average_df.rename(columns={i: 'average ' + i for i in pollutants}, inplace=True)
		pollution_df = pollution_df.merge(average_df, how='left', on='fips')

		return pollution_df

	def covid(bcovid: bool) -> pd.DataFrame:
		if (bcovid):

			covid_df = covid(start_date, end_date)
			covid_df['date'] = pd.to_datetime(covid_df['date'], format='%m/%d/%Y')

			covid_df.to_csv('data/covid.csv')

			# covid_df.drop(['county', 'state'], axis=1, inplace=True)

		else:

			covid_df = pd.read_csv('data/covid.csv', index_col=0, parse_dates=['date'])
			covid_df.rename(columns={'Lat': 'ideal latitude', 'Long_': 'ideal longitude'}, inplace=True)
			# covid_df.drop(['county', 'state'], axis=1, inplace=True)

		return covid_df

	def demographics(bdemographics: bool) -> pd.DataFrame:
		if (bdemographics):

			demographics_df = demographics()
			demographics_df.to_csv('data/demographics.csv', index=False)

			demographics_df.drop(['county', 'state'], axis=1, inplace=True)

		else:

			demographics_df = pd.read_csv('data/demographics.csv')

			demographics_df.drop(['county', 'state'], axis=1, inplace=True)

		return demographics_df

	def weather(bweather: bool) -> pd.DataFrame:
		if (bweather):

			# weather_df = pd.DataFrame()
			# weather_df = pd.read_pickle('weather.pkl')
			weather_df = pd.read_csv('data/weather.csv', parse_dates=['date'])

			for i, location in counties.iterrows():
				# if (i <= 1476):
					# continue

				# if (location['fips'] in weather_df['fips'].unique() or i == 667):
					# continue

				if (isinstance(location['county'], float)):
					continue

				try:
					one_county_entire_duration_df = weather(
						location['fips'],
						location['latitude'],
						location['longitude'],
						start_date,
						end_date,
						county=location['county'],
						state=location['state'],
					)

					weather_df = weather_df.append(one_county_entire_duration_df)

				except IndexError:
					with open('weather_df.pkl', 'wb') as f:
						pickle.dump(weather_df, f)
					with open('unsuccessful.txt', 'w') as f:
						f.write('First Unsuccessful Location\n')
						f.write(f"{i}, {location['county']}, {location['state']}, {location['fips']}\n")

						weather_df.to_csv('data/weather.csv')
						print(f'{i}/{total}')

					print('Weather Failed')

					break

				if (i % 10 == 0):
					weather_df.to_csv('data/weather.csv')
					print(f'{i}/{total}')

				print(f'{location["county"]}, {location["state"]} completed')

			# checkpoints
			weather_df.to_csv('data/weather.csv')

			cols = weather_df.columns.tolist()
			weather_df = weather_df[[cols[0]] + cols[13:] + cols[1:13]]
			weather_df.to_csv('data/weather.csv')

		else:
			weather_df = pd.read_csv('data/weather.csv', parse_dates=['date'], index_col=0)
			weather_df.drop(['county', 'state'], axis=1, inplace=True)

		copy_df = df[['fips', 'ideal latitude', 'ideal longitude']].copy(deep=True).drop_duplicates(subset=['fips'])
		temp_df = weather_df.copy().drop_duplicates(subset=['fips'])
		temp_df = temp_df.merge(copy_df, on='fips', how='left')
		temp_df['distance'] = temp_df.apply(lambda row: Conversion.distance(row['latitude'], row['longitude'], row['ideal latitude'], row['ideal longitude']), axis=1)
		# temp_df.drop(['date'], axis=1, inplace=True)
		temp_df.drop([i for i in temp_df.columns if i not in ['fips', 'ideal latitude', 'ideal longitude', 'distance']], axis=1, inplace=True)
		weather_df = weather_df.merge(temp_df, on='fips', how='left')
		# weather_df['distance'] = temp_df['distance']
		# weather_df = df.merge(temp_df, on=['date', 'fips'], how='left')

		return weather_df

	def vaccination(bvaccination: bool) -> pd.DataFrame:
		if (bvaccination):
			vaccination_df = vaccination()
			vaccination_df.to_csv('data/vaccination.csv', index=False)

		else:

			vaccination_df = pd.read_csv('data/vaccination.csv', parse_dates=['date'])

		vaccination_df.drop(['county', 'state abbreviation'], axis=1, inplace=True)

		return vaccination_df

load_dotenv('config.txt')

start_date = date(2020, 3, 1)
end_date = date(2021, 6, 30)

# input data in config.txt
# True to get data | False to read data from file
bmap = {'True': True, 'False': False}

bpollution = bmap[os.getenv('bpollution')]
bcovid = bmap[os.getenv('bcovid')]
bdemographics = bmap[os.getenv('bdemographics')]
bweather = bmap[os.getenv('bweather')]
bvaccination = bmap[os.getenv('bvaccination')]

total = len(counties)

df = pd.DataFrame(columns=['fips'])

pollution_df = Main.pollution(bpollution)
df = df.merge(pollution_df, on='fips', how='outer')
del pollution_df
print('Pollution Finished')

covid_df = Main.covid(bcovid)
df.drop(['county', 'state'], axis=1, inplace=True)
df = df.merge(covid_df, on=['date', 'fips'], how='right')
del covid_df
print('COVID-19 Finished')

demographics_df = Main.demographics(bdemographics)
df = df.merge(demographics_df, on='fips', how='left')
del demographics_df
print('Demographics Finished')

weather_df = Main.weather(bweather)
df = df.merge(weather_df, on=['date', 'fips'], how='left')
del weather_df
print('Weather Finished')

vaccination_df = Main.vaccination(bvaccination)
df = df.merge(vaccination_df, on=['date', 'fips'], how='left')
del vaccination_df
print('Vaccination Finished')

path = Path(f'data/final/{date.today()}.csv')
df = Clean(df)

print(df)
print(df.columns)
input('Press Enter to Export')

print('Exporting...')
start = datetime.now()
df.to_csv(path, index=False, chunksize=100000)
df.to_pickle(path.with_suffix('.pkl'))
end = datetime.now()

print(f'Finished in {(end - start).seconds} seconds')
print()
print('File exported to:')
print(path)
