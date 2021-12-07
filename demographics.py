from dependencies import *

demographics_df = pd.read_csv('raw/demographics.csv', na_values='X')
education_df = pd.read_csv('raw/education.csv', skiprows=4)
poverty_df = pd.read_csv('raw/poverty.csv', skiprows=4)

class Demographics:
	def population() -> pd.DataFrame:
		"""population estimates by county for 7/1/2020

		Returns:
				pd.DataFrame: county, state, fips, population
		"""

		# 13 represents 7/1/2020 population estimate
		df = demographics_df[demographics_df['YEAR'] == 13]
		df = df[df['AGEGRP'] == 0]

		# df['FIPS'] = str(df['STATE']) + str(df['COUNTY']).zfill(3)
		df['fips'] = df.apply(lambda x: Conversion.state_and_county_fips_to_combined_fips(x['COUNTY'], x['STATE']), axis=1)

		df = df[['fips', 'CTYNAME', 'STNAME', 'TOT_POP']]

		df['CTYNAME'] = df['CTYNAME'].str.replace('(?<=[a-zA-Z]) County', '', regex=True)

		df.rename(columns={'CTYNAME': 'county', 'STNAME': 'state', 'TOT_POP': 'population'}, inplace=True)

		df['fips'] = df['fips'].astype(int)
		df['population'] = df['population'].astype(int)

		return df

	def age():
		df = demographics_df[demographics_df['YEAR'] == 13][['AGEGRP', 'COUNTY', 'STATE', 'TOT_POP']]

		df['fips'] = df.apply(lambda row: Conversion.state_and_county_fips_to_combined_fips(int(row['COUNTY']), int(row['STATE'])), axis=1)
		df['TOT_POP'] = df['TOT_POP'].astype(int)
		df.drop(['COUNTY', 'STATE'], axis=1, inplace=True)

		# age_df = pd.DataFrame()
		# for i in df.groupby('fips'):
			# age_df = pd.concat([age_df, i[1]['TOT_POP'].append(pd.Series(i[0])).reset_index(drop=True)], axis=1)

		age_df = pd.concat([i[1]['TOT_POP'].append(pd.Series(i[0])).reset_index(drop=True) for i in df.groupby('fips')], axis=1)

		age_df = age_df.T.reset_index(drop=True)
		age_df.columns = ['Total Pop', 'Pop Pct 0-4', 'Pop Pct 5-9', 'Pop Pct 10-14', 'Pop Pct 15-19', 'Pop Pct 20-24', 'Pop Pct 25-29', 'Pop Pct 30-34', 'Pop Pct 35-39', 'Pop Pct 40-44',
								'Pop Pct 45-49', 'Pop Pct 50-54', 'Pop Pct 55-59', 'Pop Pct 60-64', 'Pop Pct 65-69', 'Pop Pct 70-74', 'Pop Pct 75-79', 'Pop Pct 80-84', 'Pop Pct 85+', 'fips']

		for col in age_df.columns[1:-1]:
			age_df[col] = age_df[col] / age_df['Total Pop'] * 100

		return age_df

	def poverty():
		"""percentage of people in poverty by county as of 2019

		Returns:
				pd.DataFrame: county, state, fips, poverty
		"""

		df = poverty_df.copy()

		df.drop([i for i in df.columns if 'PCTPOV' not in i and i not in ['FIPStxt', 'State', 'Area_name']], axis=1, inplace=True)
		df.drop('PCTPOV04_2019', axis=1, inplace=True)
		df.rename(columns={'FIPStxt': 'fips', 'State': 'state abbreviation', 'Area_name': 'county'}, inplace=True)

		df['county'] = df['county'].str.replace('(?<=[a-zA-Z]) County', '', regex=True)

		return df

	def education():
		df = education_df.copy()

		df = df[[i for i in df.columns if ('2015-19' in i and 'Percent of' in i) or (i in ['FIPS Code', 'State', 'Area name'])]]

		df.rename(columns={'FIPS Code': 'fips', 'State': 'state abbreviation', 'Area name': 'county'}, inplace=True)
		df['county'] = df['county'].str.replace('(?<=[a-zA-Z]) County', '', regex=True)

		return df

def demographics():
	population = Demographics.population()
	education = Demographics.education()
	poverty = Demographics.poverty()
	age = Demographics.age()

	df = population.merge(education, how='outer', on='fips')
	df = df.merge(poverty, how='outer', on='fips')
	df = df.merge(age, how='outer', on='fips')

	df.drop(['county_x', 'county_y'], axis=1, inplace=True)

	# df['location'] = df.apply(lambda row: Location(fips=row['fips']), axis=1)

	# cols = ['fips', 'state', 'county', 'state abbreviation', 'location', 'population', 'Percent of adults with less than a high school diploma, 2015-19', 'Percent of adults with a high school diploma only, 2015-19', "Percent of adults completing some college or associate's degree, 2015-19", "Percent of adults with a bachelor's degree or higher, 2015-19", 'PCTPOVALL_2019', 'PCTPOV017_2019', 'PCTPOV517_2019']

	# assert set(df.columns) == set(cols)

	# df = df[cols]

	return df

if __name__ == '__main__':
	a = demographics()
	# a = Demographics.age()
	# a = Demographics.poverty()
	print(a.columns)
