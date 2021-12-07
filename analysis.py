from dependencies import *

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from xgboost import plot_tree, plot_importance

from final_data import final_df as df

independents = df.columns.tolist()
dependent = 'percentage_new'

df.dropna(subset=independents + [dependent], inplace=True)
df.drop(df[(df[dependent] < 0) | (df[dependent] > 10)].index, inplace=True)
