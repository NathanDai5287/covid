from dependencies import *

apikeys = [
	'3b42aa44676e4ff79fc173239210208',
	'7c0d1108e46f4fbdb2550629210308',
	'126da76723d547cfa2553630210308',
	'bf924f45ded1401c9ea54801210308',
	'e853b86c76524a2cab954930210308',
	'15b50811ac7b4524a5f195105210308',
	'aa2cdb09ca544e42bb8162048210508',
	'67023c5cd42440c6ae2162616210508'
	'c37d73fdc4b14756b4f162951210508',
	'10f78e63da8e41e5a3355801210608',
]

class Weather:
	api = Api('http://api.worldweatheronline.com/premium/v1/past-weather.ashx')

	def weather(apikey: str, fips: int, latitude: float, longitude: float, start_date: date, end_date: date, frequency: int=24, includelocation: bool=True, **kwargs) -> pd.DataFrame:
		Weather.api['key'] = apikey
		Weather.api['format'] = 'json'

		Weather.api['q'] = '{},{}'.format(latitude, longitude)
		Weather.api['tp'] = frequency
		Weather.api['includelocation'] = 'yes' if includelocation else 'no'

		df_entire_time = pd.DataFrame()
		for start, end in Conversion.time_range_to_monthlong_sections(start_date, end_date):
			Weather.api['date'] = start
			Weather.api['enddate'] = end

			data = Weather.api.call()['data']

			latitude, longitude = data['nearest_area'][0]['latitude'], data['nearest_area'][0]['longitude']

			data = [pd.DataFrame(Weather.clean(day)) for day in data['weather']]

			df = pd.concat(data)

			df_entire_time = df_entire_time.append(df, ignore_index=True)

		df_entire_time['latitude'] = latitude
		df_entire_time['longitude'] = longitude
		df_entire_time['fips'] = fips

		for key, value in kwargs.items():
			df_entire_time[key] = value

		df_entire_time['distance'] = df.apply(lambda row: Conversion.distance(row['latitude'], row['longitude'], row['ideal latitude'], row['ideal longitude']), axis=1)

		return df_entire_time

	def clean(data: dict) -> pd.DataFrame:
		useful = {'date': data['date']}

		select = ['avgtempC', 'maxtempC', 'mintempC', 'sunHour', 'uvIndex']
		useful.update({key: [data[key]] for key in select})

		assert len(data['hourly']) == 1

		data = data['hourly'][0]

		select = ['windspeedKmph', 'humidity', 'pressure', 'precipMM', 'cloudcover']
		useful.update({key: [data[key]] for key in select})

		return useful

def weather(fips: int, latitude: float, longitude: float, start_date: date, end_date: date, frequency: int=24, includelocation: bool=True, **kwargs) -> pd.DataFrame:
	i = 0
	while (True):
		try:
			result = Weather.weather(
				apikeys[i],
				fips,
				latitude,
				longitude,
				start_date,
				end_date,
				frequency=frequency,
				includelocation=includelocation,
				**kwargs
			)

			return result
		except:
			i += 1

			if (i >= len(apikeys)):
				# raise IndexError('No valid API key found')
				print('No valid API key found')
				input('Press Enter to Continue')

				i = 0

if __name__ == '__main__':
	# apikey = apikeys[0]

	fips = 36059

	latitude = 40.74066522
	longitude = -73.58941873

	county = 'Nassau'

	start_date = date(2020, 3, 1)
	# end_date = date(2021, 6, 30)
	end_date = date(2020, 5, 31)

	print(weather(fips, latitude, longitude, start_date, end_date, county=county))
