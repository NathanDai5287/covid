from dependencies import *

class Clean(pd.DataFrame):
	pollutants: list= ['lead', 'carbon monoxide', 'sulfur dioxide', 'nitrogen dioxide', 'ozone', 'PM10', 'PM2.5']

	adjacency: dict = json.load(open('docs/county_adjacency.json'), object_hook=lambda x: {int(k): v for k, v in x.items()})

	def __init__(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
		"""calculates different measurments for variables

		Args:
				df (pd.DataFrame): dataframe

		Kwargs:
				contagious (int): number of days to calculate active cases
				average (int): number of days to calculate new cases
		"""

		super().__init__(df)

		# self.df = df
		self.clean()

	# def __repr__(self):
		# return str(self)

	# def to_csv(self, path: str, index=True):
		# self.to_csv(path, index=index)

	def clean(self, contagious=14, average=7):
		self.active_cases(contagious=contagious)
		self.new_cases(average=average)
		self.percentage_new()
		self.vaccination_zeroes()
		# self.interpolate_pollution()

		return self

	def active_cases(self, contagious=14):
		self['active'] = (self['Confirmed'] - self['Deaths']).fillna(0)
		self['active'] = self.groupby('fips')['active'].diff(contagious)
		self.drop('Active', axis=1, inplace=True)

		return self

	def new_cases(self, average=7):
		self['new'] = self.groupby('fips')['Confirmed'].diff(average).shift(-average) / average
		self.loc[self['new'] < 0, 'new'] = np.nan

		return self

	def percentage_new(self):
		self['percentage_new'] = self['new'] / self['active'] * 100

		return self

	def vaccination_zeroes(self):
		vaccine_cols = ['Series_Complete_Pop_Pct', 'Series_Complete_12PlusPop_Pct', 'Series_Complete_18PlusPop_Pct', 'Series_Complete_65PlusPop_Pct', 'Administered_Dose1_Pop_Pct', 'Administered_Dose1_Recip_12PlusPop_Pct', 'Administered_Dose1_Recip_18PlusPop_Pct', 'Administered_Dose1_Recip_65PlusPop_Pct']

		self[vaccine_cols] = self[vaccine_cols].fillna(0)

		return self

	def interpolate_pollution(self) -> pd.DataFrame:
		missing_df = self[self[self.pollutants].isnan().all(axis=1)]
		for _, row in missing_df.iterrows():
			for pollutant in self.pollutants:
				row[pollutant] = np.nanmean([self[(self['fips'] == fips) & (self['date'] == row['date'])][pollutant].values[0] for fips in self.adjacency[row['fips']]])
				print(pollutant, row[pollutant]) if not row[pollutant].isnull() else None

if __name__ == '__main__':
	df = pd.read_csv('data/final/2021-07-31.csv', index_col=0)


	clean = Clean(df)
	clean.clean()

	path = Path(f'data/cleaned/{date.today()}.csv')
	clean.df.to_csv(path, index=False)
