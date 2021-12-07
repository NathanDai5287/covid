from dependencies import *

vaccination_df = pd.read_csv('raw/vaccination.csv', na_values={'UNK'}, parse_dates=['Date'], low_memory=False)

class Vaccination:
	def vaccination():
		variables = ['Series_Complete_Pop_Pct', 'Series_Complete_12PlusPop_Pct', 'Series_Complete_18PlusPop_Pct', 'Series_Complete_65PlusPop_Pct', 'Administered_Dose1_Pop_Pct', 'Administered_Dose1_Recip_12PlusPop_Pct', 'Administered_Dose1_Recip_18PlusPop_Pct', 'Administered_Dose1_Recip_65PlusPop_Pct', 'SVI_CTGY', 'Series_Complete_Pop_Pct_SVI', 'Series_Complete_12PlusPop_Pct_SVI', 'Series_Complete_18PlusPop_Pct_SVI', 'Series_Complete_65PlusPop_Pct_SVI']

		df = vaccination_df[['Date', 'FIPS', 'Recip_County', 'Recip_State'] + variables]

		df.rename(columns={'FIPS': 'fips', 'Date': 'date', 'Recip_County':'county', 'Recip_State': 'state abbreviation'}, inplace=True)

		# df.dropna(inplace=True)
		# df[['Series_Complete_Pop_Pct', 'Series_Complete_12PlusPop_Pct', 'Series_Complete_18PlusPop_Pct', 'Series_Complete_65PlusPop_Pct', 'Administered_Dose1_Pop_Pct', 'Administered_Dose1_Recip_12PlusPop_Pct', 'Administered_Dose1_Recip_18PlusPop_Pct', 'Administered_Dose1_Recip_65PlusPop_Pct']].fillna(0, inplace=True)


		df['fips'] = df['fips'].astype({'fips': int})
		df['date'] = pd.to_datetime(df['date'])

		return df

def vaccination():
	df = Vaccination.vaccination()

	return df

if __name__ == '__main__':
	a = vaccination().head(10)
