from dependencies import *

class Pollution:
	parameters = {'Pb': '14129',
								'CO': '42101',
								'SO2': '42401',
								'NO2': '42602',
								'O3': '44201',
								'PM10': '85101',
								'PM2.5': '88101'}

	def county_air_pollution(parameter: str, start_date: date, end_date: date, state: str, county: str, email='nathandai2000@gmail.com', key='ambergazelle37') -> dict:
		"""finds data on the air pollution of a county in a given time frame

		Args:
				parameter (str): parameter code of air pollutant
				start_date (date): inclusive
				end_date (date): inclusive; must be in the same year as start_date
				state (str): state code
				county (str): county code
				email (str, optional): must register email for API use. Defaults to 'nathandai2000@gmail.com'.
				key (str, optional): will receive key after email is registered. Defaults to 'ambergazelle37'.

		Returns:
				dict: dictionary of all data in url
		"""

		# format dates
		start_date = Conversion.yyyymmdd(start_date)
		end_date = Conversion.yyyymmdd(end_date)

		# url
		url = f'https://aqs.epa.gov/data/api/dailyData/byCounty?email={email}&key={key}&param={parameter}&bdate={start_date}&edate={end_date}&state={state}&county={county}'

		# get data
		try:
			data = json.loads(requests.get(url).text)
		except ConnectionError:
			url = f'https://aqs.epa.gov/data/api/dailyData/byCounty?email=dailiang2000@gmail.com&key=ochrewolf55&param={parameter}&bdate={start_date}&edate={end_date}&state={state}&county={county}'

		# check that it was successful
		assert data['Header'][0]['status'] != 'Failed', url
		# assert data['Data'], url

		if not (data['Data']):
			return pd.DataFrame()

		return Pollution.clean(data)

	def clean(data: dict) -> dict:
		if not (data['Data']):
			data['Data'] = [{}]

		data = data['Data']

		parameter = data[0]['parameter']

		data = [(datapoint['arithmetic_mean'], datapoint['date_local']) for datapoint in data]

		df = pd.DataFrame(data, columns=[parameter, 'date'])

		return df.groupby('date').mean()

	# def chronic()

def pollution(start_date: date, end_date: date, location: pd.Series):
	county_code, state_code = Conversion.location_name_to_aqs_code(location['County'], location['State'])

	one_county_entire_duration_df = pd.DataFrame()

	# while (start_date < end_date): # get data for all days
	for start_date, end_date in Conversion.time_range_to_yearlong_sections(start_date, end_date):
		one_year_multiple_pollutants_df = pd.DataFrame(columns=['date'])
		for parameter, parameter_code in Pollution.parameters.items(): # each parameter
			one_pollutant_df = Pollution.county_air_pollution(parameter_code, start_date, end_date, state_code, county_code)

			if (one_pollutant_df.empty): # if no data was found
				continue

			# merge one_pollutant_df with one_year_multiple_pollutants_df by date
			one_year_multiple_pollutants_df = one_year_multiple_pollutants_df.merge(one_pollutant_df, how='outer', on='date', sort=True)

		one_county_entire_duration_df = one_county_entire_duration_df.append(one_year_multiple_pollutants_df)

	one_county_entire_duration_df['state'] = location['State']
	one_county_entire_duration_df['county'] = location['County']
	one_county_entire_duration_df['fips'] = location['FIPS']

	one_county_entire_duration_df.rename(columns={'Lead (TSP) LC': 'Pb', 'Carbon monoxide': 'CO', 'Sulfur dioxide': 'SO2', 'Nitrogen dioxide (NO2)': 'NO2', 'Ozone': 'O3', 'PM10 - LC': 'PM10', 'PM2.5 - Local Conditions': 'PM2.5'}, inplace=True)

	one_county_entire_duration_df = one_county_entire_duration_df[['state', 'county', 'fips', 'date', 'Pb', 'CO', 'SO2', 'NO2', 'O3', 'PM10', 'PM2.5']]

	print(f'{location["County"]}, {location["State"]} completed')

	return one_county_entire_duration_df

def chronic(years: 10) -> pd.DataFrame:
	pass

if __name__ == '__main__':
	parameter = Pollution.parameters['CO']
	start_date = date(2020, 1, 1)
	end_date = date(2020, 1, 31)
	county_code, state_code = Conversion.location_name_to_aqs_code('San Diego', 'California')

	pollution(start_date, end_date, pd.Series({'County': 'San Diego', 'State': 'California'}))

	# data = Pollution.county_air_pollution(parameter=parameter,
	# 																			start_date=start_date,
	# 																			end_date=end_date,
	# 																			state=state_code,
	# 																			county=county_code)

	# print(data)
