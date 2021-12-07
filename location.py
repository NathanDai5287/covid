from dependencies import *

class Location:
	def __init__(self, **kwargs):
		"""
		kwargs: (all in title case)
			county (str): name of county without trailing " County"
			state (str): name of state
			abbreviation (str): 2 letter abbreviation of state
			fips (int): fips as int without leading zeros
		"""

		for key, value in kwargs.items():
			setattr(self, key, value)

		if (hasattr(self, 'fips')):
			county, abbreviation = Conversion.fips_code_to_county_and_state_abbreviation(self.fips)
			state = Conversion.abbreviation_to_state_name(abbreviation)

			self.county = county
			self.state = state
			self.abbreviation = abbreviation

		elif (hasattr(self, 'county') and ((babbreviation := hasattr(self, 'abbreviation')) or hasattr(self, 'state'))):
			if (babbreviation):
				state = Conversion.abbreviation_to_state_name(self.abbreviation)
				abbreviation = self.abbreviation
			else:
				state = self.state
				abbreviation = Conversion.state_name_to_abbreviation(self.state)

			fips = Conversion.county_name_to_fips_code(self.county, state)

			self.fips = fips
			self.county = self.county
			self.state = state
			self.abbreviation = abbreviation

		else:
			raise ValueError('Location must have either (fips) or (county and (state or abbreviation))')

	def __repr__(self):
		return f'{self.county}, {self.state} ({self.fips})'

	def __eq__(self, other: object):
		return self.fips == other.fips

if __name__ == '__main__':
	location = Location(county='San Diego', fips=6073)

	print(location.county)
	print(location.state)
	print(location.abbreviation)
	print(location.fips)
