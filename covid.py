from dependencies import *

class Covid:
	def us_data(start_date: date, end_date: date) -> list[pd.DataFrame]:
		"""returns United States COVID-19 data
		Args:
			start_date (datetime.date): start date
			end_date (datetime.date): end date
		Returns:
			list: list of pandas DataFrames; one DataFrame for each day
		"""

		base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

		data = pd.DataFrame()
		for day in Conversion.days_between(start_date, end_date):
			url = base_url + day.strftime('%m-%d-%Y') + '.csv'

			raw = StringIO(requests.get(url).text)

			df = pd.read_csv(raw)

			try:
				df = df[df['Country_Region'] == 'US']
			except KeyError:
				df = df[df['Country/Region'] == 'US']

			df['date'] = day

			data = data.append(df)

			# track progress
			if (day.day == 1):
				print(day)

		data.set_index('date', inplace=True)

		return Covid.clean(data)

	def clean(df: pd.DataFrame) -> pd.DataFrame:
		df = df[['FIPS', 'Admin2', 'Lat', 'Long_', 'Province_State', 'Confirmed', 'Deaths', 'Recovered', 'Active']]

		df = df[df['Admin2'] != 'Unassigned']

		# remove row from df if FIPS is nan
		df = df[pd.notnull(df['FIPS'])]

		df.rename(columns={'FIPS': 'fips', 'Admin2': 'county', 'Province_State': 'state'}, inplace=True)

		return df

def covid(start_date: date, end_date: date) -> pd.DataFrame:
	return Covid.us_data(start_date, end_date)

if __name__ == '__main__':
	start_date = date(2021, 1, 1)
	end_date = date(2021, 1, 10)

	a = covid(start_date, end_date)

	print(a)
