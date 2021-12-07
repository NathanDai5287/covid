import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dependencies import *

import statsmodels.api as sm
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from xgboost import plot_tree, plot_importance

from colorama import init
from termcolor import colored

init()

from final_data import final_df as df

df = df.drop(df.columns[68:72], axis=1)
df['SVI_CTGY'].replace({'Low': 0, 'Low-Mod': 1, 'Mod-High': 2, 'High': 3}, inplace=True)
df['Pop Pct 0-29'] = df['Pop Pct 0-4'] + df['Pop Pct 5-9'] + df['Pop Pct 10-14'] + df['Pop Pct 15-19'] + df['Pop Pct 20-24'] + df['Pop Pct 25-29']
df['Pop Pct 60+'] = df['Pop Pct 60-64'] + df['Pop Pct 65-69'] + df['Pop Pct 70-74'] + df['Pop Pct 75-79'] + df['Pop Pct 80-84'] + df['Pop Pct 85+']
df['Percent of adults with a high school diploma or less'] = df['Percent of adults with less than a high school diploma, 2015-19'] + df['Percent of adults with a high school diploma only, 2015-19']
df.drop(['Pop Pct 0-4', 'Pop Pct 5-9', 'Pop Pct 10-14', 'Pop Pct 15-19',
			 'Pop Pct 20-24', 'Pop Pct 25-29', 'Pop Pct 30-34', 'Pop Pct 35-39',
			 'Pop Pct 40-44', 'Pop Pct 45-49', 'Pop Pct 50-54', 'Pop Pct 55-59',
			 'Pop Pct 60-64', 'Pop Pct 65-69', 'Pop Pct 70-74', 'Pop Pct 75-79',
			 'Pop Pct 80-84', 'Pop Pct 85+', 'Recovered', 'Percent of adults with less than a high school diploma, 2015-19', 'Percent of adults with a high school diploma only, 2015-19'], axis=1, inplace=True)
to_be_removed = ['date', 'fips', 'county', 'ideal latitude_x', 'ideal longitude_x', 'state',
								 'Confirmed', 'Deaths', 'population', 'Total Pop', 'state abbreviation',
								 'latitude', 'longitude', 'ideal latitude_y', 'ideal longitude_y',
								 'distance', 'Series_Complete_Pop_Pct_SVI', 'Series_Complete_12PlusPop_Pct_SVI',
								 'Series_Complete_18PlusPop_Pct_SVI', 'Series_Complete_65PlusPop_Pct_SVI',
								 'active', 'new', 'percentage_new', 'Series_Complete_12PlusPop_Pct',
								 'sunHour', 'carbon monoxide', 'mintempC',  'pressure',
								 'sulfur dioxide', 'cloudcover', 'sulfur dioxide',
								 'nitrogen dioxide', 'precipMM', 'Series_Complete_65PlusPop_Pct',
								 'Administered_Dose1_Pop_Pct', 'uvIndex', 'ozone',
								 'PCTPOV517_2019', 'maxtempC', 'lead', 'Administered_Dose1_Recip_18PlusPop_Pct',
								 'Series_Complete_Pop_Pct', 'PCTPOV017_2019',
								 "Percent of adults completing some college or associate's degree, 2015-19",
								 'Administered_Dose1_Recip_65PlusPop_Pct', 'Administered_Dose1_Recip_12PlusPop_Pct',
								 'PM10', 'humidity', 'avgtempC', "Percent of adults with a bachelor's degree or higher, 2015-19",
								 'Pop Pct 0-29', 'windspeedKmph']

independents = [col for col in df.columns if col not in to_be_removed]
# independents = df.columns.tolist()
dependent = 'percentage_new'
# dependent = 'Confirmed'

df.dropna(subset=independents + [dependent], inplace=True)
df.drop(df[(df[dependent] < 0) | (df[dependent] > 10)].index, inplace=True)

x = sm.add_constant(df[independents], prepend=False)
# x = df[independents]
y = df[dependent]

model = XGBRegressor(n_estimators=18, max_depth=10, n_jobs=-1)
scores = cross_val_score(model, x, y, cv=20)

print(colored(str(round(scores.mean() * 100, 2)) + '%', "green") + colored(' accuracy with a standard deviation of ', 'cyan') + colored(str(round(scores.std() * 100, 2)) + '%', "green"))

# model.fit(x, y, enable_categorical=True)
model.fit(x, y)

plot_importance(model)

plt.show()

# find the optimal parameters
	
# param_grid = {
# 	'max_depth': [10, 15, 20],
# 	'learning_rate': [0.1, 0.5, 1],
# 	'gamma': [0, 0.25, 1],
# 	'reg_lambda': [0, 1, 10],
# 	'scale_pos_weight': [1, 3, 5]
# }

# optimal_params = GridSearchCV(
# 	estimator=XGBRegressor(seed=42),
# 	param_grid=param_grid,
# 	# scoring='neg_mean_squared_error',
# 	scoring='roc_auc',
# 	verbose=2,
# 	n_jobs=-1,
# 	cv=20,
# )

# print(optimal_params)
