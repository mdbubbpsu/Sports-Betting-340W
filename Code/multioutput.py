# -*- coding: utf-8 -*-
"""multiOutput.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IxUhBCjWFG2klkORNyP-Yl6dVtAKyD8F
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error 
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
from sklearn.linear_model import Lasso as lasso

df = pd.read_csv('finalDataFrame.csv')

df.columns

df = df.drop(['Unnamed: 0'], axis = 1)
df

df['diff_reb'] = df['home_reb'] - df['away_reb']
df['diff_fg_pct'] = df['home_fg_pct'] - df['away_fg_pct']
df['diff_fg3_pct'] = df['home_fg_pct'] - df['away_fg_pct']
df['diff_w_pct'] = df['home_w_pct'] - df['away_w_pct']
df['diff_pts'] = df['home_pts'] - df['away_pts']
df['diff_ast'] = df['home_ast'] - df['away_ast']
df['diff_pts'] = df['home_pts'] - df['away_pts']
df['diff_tov'] = df['home_tov'] - df['away_tov']

X = df[['home_w_pct', 'home_fg_pct',
        'home_fg3_pct', 'home_ft_pct', 'home_reb', 'home_ast', 'home_stl',
       'home_blk', 'home_tov', 'home_pts', 'away_team_id', 'away_w_pct',
       'away_fg_pct', 'away_fg3_pct', 'away_ft_pct', 'away_reb', 'away_ast',
       'away_stl', 'away_blk', 'away_tov', 'away_pts', 'diff_reb', 
       'diff_fg_pct', 'diff_fg3_pct',
       'diff_w_pct', 'diff_pts', 'diff_ast', 'diff_tov']]
yHome = df['homeTeamPrice']
yAway = df['awayTeamPrice']

print("HERE")

"""## Parson's Correlation on Features"""

#plt.figure(figsize=(30,25))
cor = df.corr()
#sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
#plt.show()

"""## Hometeam Price Feature Investigation"""

#Correlation with home team price variable
cor_target_home = abs(cor["homeTeamPrice"])
cor_target_home.sort_values(ascending=False)

reg = LassoCV()
reg.fit(X, yHome)
print("Best alpha using built-in LassoCV: %f" % reg.alpha_)
print("Best score using built-in LassoCV: %f" %reg.score(X,yHome))
coef = pd.Series(reg.coef_, index = X.columns)

print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")

imp_coef = coef.sort_values()
import matplotlib
#matplotlib.rcParams['figure.figsize'] = (8.0, 10.0)
#imp_coef.plot(kind = "barh")
#plt.title("Feature importance using Lasso Model")

"""## Awayteam Price Investigation"""

#Correlation with away team price variable
cor_target_away = abs(cor["awayTeamPrice"])
cor_target_away.sort_values(ascending=False)

reg = LassoCV()
reg.fit(X, yAway)
print("Best alpha using built-in LassoCV: %f" % reg.alpha_)
print("Best score using built-in LassoCV: %f" %reg.score(X,yAway))
coef = pd.Series(reg.coef_, index = X.columns)

print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")

imp_coef = coef.sort_values()
import matplotlib
#matplotlib.rcParams['figure.figsize'] = (8.0, 10.0)
#imp_coef.plot(kind = "barh")
#plt.title("Feature importance using Lasso Model")

"""## Back to modeling"""

X = df[['home_blk','home_stl','diff_pts','diff_ast','home_ast','away_reb','away_blk']]
y = df[['homeTeamPrice','awayTeamPrice']]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.3, random_state=4)

regr_multirf = MultiOutputRegressor(RandomForestRegressor(n_estimators=100,
                                                          max_depth=30,
                                                          random_state=0))
regr_multirf.fit(X_train, y_train)

y_multirf = regr_multirf.predict(X_test)

regr_multirf.score(X_test, y_test)

y_multirf = pd.DataFrame(y_multirf, columns = ['homeTeamPrice','awayTeamPrice'])

"""## Performance Metrics"""

homeRMSE = math.sqrt(mean_squared_error(y_multirf['homeTeamPrice'], y_test['homeTeamPrice']))

homeRMSE

y_multirf['homeTeamPrice'][:5]
y_multirf

y_test['homeTeamPrice'][:5]
y_test.reset_index()

awayRMSE = math.sqrt(mean_squared_error(y_multirf['awayTeamPrice'], y_test['awayTeamPrice']))

awayRMSE

y_multirf['awayTeamPrice'][:5]

y_test['awayTeamPrice'][:5]

param_grid = {"criterion": ["mse", "mae"],
              "min_samples_split": [10, 20, 40],
              "max_depth": [2, 6, 8],
              "min_samples_leaf": [20, 40, 100],
              "max_leaf_nodes": [5, 20, 100],
              }

## Comment in order to publish in kaggle.

grid_cv_dtm = RandomizedSearchCV(RandomForestRegressor(n_estimators=100,
                                                  max_depth=30,
                                                  random_state=0), param_grid, verbose=10, n_iter=20, cv=5)

grid_cv_dtm.fit(X_train,y_train)


cross_val_score(regr_multirf, X_train, y_train, cv=5)

print("R-Squared::{}".format(grid_cv_dtm.best_score_))
print("Best Hyperparameters::\n{}".format(grid_cv_dtm.best_params_))

