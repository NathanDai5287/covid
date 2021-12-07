from dependencies import *

from datetime import date
import pandas as pd

location_to_code = pd.read_csv('conversions/location_to_code.csv')
county_to_fips = pd.read_csv('conversions/county_to_fips.csv')
state_to_abbreviation = pd.read_csv('conversions/state_to_abbreviation.csv')

class Conversion:
	def yyyymmdd(day: date):
		return day.strftime('%Y%m%d')

	def location_name_to_aqs_code(county: str, state: str) -> tuple[str, str]:
		"""converts a location to a code for AQS

		Args:
				county (str): the county name
				state (str): the state name

		Returns:
				tuple[str, str]: (county code, state code)
		"""

		state = state.title()
		county = county.title()

		grouped = location_to_code.groupby(['State Name', 'County Name'])

		try:
			row = grouped.get_group((state, county))
		except KeyError:
			county = get_close_matches(county, location_to_code[location_to_code['State Name'] == state]['County Name'].tolist())[0]
			row = grouped.get_group((state, county))

		assert len(row) == 1

		codes = tuple(map(str, row[['County Code', 'State Code']].values[0]))

		return codes[0].zfill(3), codes[1].zfill(2)

	def state_name_to_abbreviation(state: str) -> str:
		return state_to_abbreviation[state_to_abbreviation['State'] == state]['Abbreviation'].values[0]

	def abbreviation_to_state_name(abbreviation: str) -> str:
		try:
			assert abbreviation is not None
			assert len(abbreviation) == 2
			assert not abbreviation.isdigit()
			assert abbreviation != 'DC'
			assert abbreviation != 'PR'
		except AssertionError:
			return None

		return state_to_abbreviation[state_to_abbreviation['Abbreviation'] == abbreviation]['State'].values[0]

	def county_name_to_fips_code(county: str, state: str) -> int:
		state = Conversion.state_name_to_abbreviation(state.title())
		county = county.title()

		grouped = county_to_fips.groupby(['State', 'County'])

		row = grouped.get_group((state, county))

		assert len(row) == 1

		return row['FIPS'].values[0]

	def fips_code_to_county_and_state_abbreviation(fips: int) -> tuple[str, str]:
		"""convert from fips to county and state abbreviation

		Args:
				fips (int): fips code

		Returns:
				tuple[str, str]: county, state abbreviation
		"""

		row = county_to_fips[county_to_fips['FIPS'] == fips][['County', 'State']].values

		try:
			assert len(row) == 1, 'Error matching FIPS to county'
		except AssertionError:
			return (None, None)

		return tuple(row[0])

	def time_range_to_yearlong_sections(start_date: date, end_date: date) -> list[tuple[date, date]]:
		for year in range(start_date.year, end_date.year + 1):
			first = date(year, 1, 1)
			if (first < start_date):
				first = start_date

			second = date(year, 12, 31)
			if (second > end_date):
				second = end_date

			yield (first, second)

	def time_range_to_monthlong_sections(start_date: date, end_date: date) -> list[tuple[date, date]]:
		assert start_date.day == 1 and (end_date + timedelta(days=1)).day == 1

		beginning = start_date
		while (beginning < end_date):
			yield (beginning, (end := beginning + relativedelta(months=1)) - timedelta(days=1))

			beginning = end

	def date_to_str_weather(day: date) -> str:
		return day.strftime('%Y-%m-%d')

	def days_between(start: date, end: date) -> list[date]:
		for day in range(int((end - start).days) + 1):
			yield start + timedelta(day)

	def state_and_county_fips_to_combined_fips(county: int, state: int) -> int:
		# return int(str(state) + str(county).zfill(3))
		return state * 1000 + county

	def distance(lata: float, lona: float, latb: float, lonb: float) -> float:
		"""distance between two coordinates of latitude and longitude in kilometers

		Args:
				lata (float): latitude of first point
				lona (float): longitude of first point
				latb (float): latitude of second point
				lonb (float): longitude of second point

		Returns:
				float: distance in kilometers
		"""

		radius = 6371 # radius of earth in km

		dLat = np.radians(latb - lata)
		dLon = np.radians(lonb - lona)

		lata = np.radians(lata)
		latb = np.radians(latb)

		a = np.sin(dLat / 2) ** 2 + np.cos(lata) * np.cos(latb) * np.sin(dLon / 2) ** 2
		c = 2 * np.arcsin(np.sqrt(a))

		return radius * c


if __name__ == '__main__':
	# print(
		# Conversion.county_name_to_fips_code('San Diego', 'California')
	# )

	# print(Conversion.fips_code_to_county_and_state_abbreviation(10001))

	# for start, end in Conversion.time_range_to_yearlong_sections(date(2016, 11, 15), date(2018, 1, 15)):
		# print(start, end)

	print([i for i in Conversion.time_range_to_monthlong_sections(date(2020, 3, 1), date(2021, 6, 30))])
