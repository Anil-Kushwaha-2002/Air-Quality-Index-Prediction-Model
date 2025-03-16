# -*- coding: utf-8 -*-
"""AQI Prediction Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kO4ofWJZRvv3IrxVPR75K25dOxJ3uQeL

# **Air Quality Index (AQI) Prediction Model using Python**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sns
from warnings import filterwarnings
from sklearn.ensemble import RandomForestRegressor
filterwarnings('ignore')

"""**Load Dataset in Google Colab**"""

from google.colab import files
print("Please upload files :")  # air quality data.csv "
uploaded = files.upload()

# Load dataset (change 'air quality data.csv' to actual file name)
df = pd.read_csv("air quality data.csv")

# Display first 5 rows
df.head()

"""**Explore the Data and Data Preprocessing**"""

# Shape - rows and cols!
df.shape

# to know the duplicate values
df.duplicated().sum()

# Check data structure
print(df.info())

# to know the duplicate values
df.duplicated().sum()

# Check for missing values
print(df.isnull().sum())

# Drop the rows where 'AQI' has missing values
df.dropna(subset=['AQI'], inplace = True)

df.isnull().sum().sort_values(ascending=False)

df.shape

# Statistical summary
print(df.describe())

# Summary of Statistics in the dataset
df.describe().T

# Percentage of the null values
null_values_percentage = (df.isnull().sum()/df.isnull().count()*100).sort_values(ascending=False)
null_values_percentage

# Select relevant features (excluding target variable)
X = df[['PM2.5', 'CO', 'NO2', 'SO2', 'O3']]  # Modify based on dataset
y = df['AQI']  # Target variable

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training set size:", X_train.shape)
print("Testing set size:", X_test.shape)

"""# **Visualizing Predictions**"""

# Bivariate
sns.set_theme(style="darkgrid")
graph = sns.catplot(x="City", kind='count', data=df, height=5, aspect=3)
graph.set_xticklabels(rotation=90)

sns.set_theme(style="darkgrid")
graph = sns.catplot(x="City", kind='count', data=df, col="AQI_Bucket", col_wrap=2,
                    height=3.5, aspect=3)
graph.set_xticklabels(rotation=90)

graph3 = sns.catplot(x='City', y='O3', kind='box', data=df, height=5, aspect=3)
graph3.set_xticklabels(rotation=90)

sns.displot(df, x='AQI', color='purple', kde=True, bins=30, height=5, aspect=1.5)
plt.xlabel("AQI Value")
plt.ylabel("Frequency")
plt.title("AQI Distribution from 2015 to 2020")
plt.show()

#  AQI_Bucket

from matplotlib import pyplot as plt
import seaborn as sns
df.groupby('AQI_Bucket').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

# Increase figure size for better visualization
plt.figure(figsize=(12, 6))

# List of pollutants to visualize
pollutants = ['Xylene', 'PM10', 'NH3', 'Toluene', 'Benzene', 'NOx', 'O3', 'PM2.5', 'SO2', 'CO', 'AQI']

# Loop to plot histogram for each pollutant
for col in pollutants:
    plt.figure(figsize=(10, 5))
    plt.hist(df[col], bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.title(f'Distribution of {col}')
    plt.show()

# TO check the null values
df.isnull().sum().sort_values(ascending=False)

df.describe().loc['mean']

df = df.replace({
    "PM2.5":{np.nan:67.476613},
    "PM10":{np.nan:118.454435},
    "NO": {np.nan:17.622421},
    "NO2": {np.nan:28.978391},
    "NOx": {np.nan:32.289012},
    "NH3": {np.nan:23.848366},
    "CO":  {np.nan:2.345267},
    "SO2": {np.nan:34.912885},
    "O3": {np.nan:38.320547},
    "Benzene": {np.nan:3.458668},
    "Toluene": {np.nan:9.525714},
    "Xylene": {np.nan:3.588683}
})

df.isnull().sum()

df.head()

sns.boxplot(data=df[['NO', 'NO2', 'NOx', 'NH3']])

# IQR Method - Q3 Q1
def replace_outliers(df):
    for column in df.select_dtypes(include=['number']).columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lb = Q1 - 1.5 * IQR
        ub = Q3 + 1.5 * IQR
        df[column] = df[column].apply(
            lambda x: Q1 if x < lb else (Q3 if x > ub else x)
        )
    return df

# Drop non-numeric columns before calculating correlation
df1 = df.select_dtypes(include=['number'])

df = replace_outliers(df)

df.describe().T

df1 = df.drop(columns=['City'])

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
df1 = df.select_dtypes(include=['number'])  # Ensure df1 is defined

# Compute correlation matrix
correlation_matrix = df1.corr()

# Plot heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Air Quality Parameters", fontsize=14)
plt.show()

"""# **Data Modeling**
**Split Data into Training & Testing Sets**
"""

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

df.drop(['Date', 'City'], axis = 1, inplace=True)
df.head()

# # Scaling - Standard Scaler
# from sklearn.preprocessing import StandardScaler

# df1 = StandardScaler().fit_transform(df)
# df1


# Drop categorical columns before applying scaling
df.drop(columns=['AQI_Bucket'], axis=1, inplace=True, errors='ignore')

# Apply StandardScaler to the remaining numeric columns
df1 = StandardScaler().fit_transform(df)

# Convert to DataFrame
df_scaled = pd.DataFrame(df1, columns=df.columns)

df = pd.DataFrame(df1, columns=df.columns)
df.head()

# Verify the columns to ensure 'Date' and 'City' have been removed
print(df.columns)

X = df.drop(columns=['AQI'])  # Features
X.head()

# Feature & Target Selection
X = df[['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3',
       'Benzene', 'Toluene', 'Xylene']]
y = df['AQI']

# Define features (independent variables) and target (dependent variable)
X = df.drop(columns=['AQI'])  # Features
y = df['AQI']  # Target variable

# Display first 5 rows of features
X.head()

# Split dataset (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print dataset shapes
print("Shape of X_train:", X_train.shape)
print("Shape of X_test:", X_test.shape)
print("Shape of y_train:", y_train.shape)
print("Shape of y_test:", y_test.shape)

print("X_train columns:", X_train.columns)
print("X_test columns:", X_test.columns)

# Drop rows with missing values in X_train and X_test
X_train = X_train.dropna()
y_train = y_train[X_train.index]  # Align the target variable
X_test = X_test.dropna()
y_test = y_test[X_test.index]  # Align the target variable

# Verify that there are no missing values left
print(X_train.isnull().sum().sum())
print(X_test.isnull().sum().sum())

"""## **(1) Linear Regression**"""

# Linear Regression Model
LR = LinearRegression()
LR.fit(X_train, y_train)

# Predicting the values:
train_pred = LR.predict(X_train) # Predicting train
test_pred = LR.predict(X_test) # Predicting test

# Evaluation for Linear Regression
RMSE_train = (np.sqrt(mean_squared_error(y_train, train_pred)))
RMSE_test = (np.sqrt(mean_squared_error(y_test, test_pred)))
print('RMSE Train Data = ', str(RMSE_train))
print('RMSE Test Data = ', str(RMSE_test))
print('_'* 60)
print('R Squared value for Train = ', LR.score(X_train, y_train))
print('R Squared value on Test = ', LR.score(X_test, y_test))

"""## **(2) K-Nearest Neighbors (KNN)**"""

# KNN
knn = KNeighborsRegressor()
knn.fit(X_train, y_train)

# Predicting the values:
train_pred = knn.predict(X_train) # Predicting train
test_pred = knn.predict(X_test) # Predicting test

# Evaluation for KNN
RMSE_train = (np.sqrt(mean_squared_error(y_train, train_pred)))
RMSE_test = (np.sqrt(mean_squared_error(y_test, test_pred)))
print('RMSE Train Data = ', str(RMSE_train))
print('RMSE Test Data = ', str(RMSE_test))
print('_'* 60)
print('R Squared value for Train = ', knn.score(X_train, y_train))
print('R Squared value on Test = ', knn.score(X_test, y_test))

"""## **(3) Decision Tree Regressor**"""

# Decision Tree
dtr = DecisionTreeRegressor()
dtr.fit(X_train, y_train)

# Predicting the values:
train_pred = dtr.predict(X_train) # Predicting train
test_pred = dtr.predict(X_test) # Predicting test

# Evaluation for Decision Tree Regressor
RMSE_train = (np.sqrt(mean_squared_error(y_train, train_pred)))
RMSE_test = (np.sqrt(mean_squared_error(y_test, test_pred)))
print('RMSE Train Data = ', str(RMSE_train))
print('RMSE Test Data = ', str(RMSE_test))
print('_'* 60)
print('R Squared value for Train = ', dtr.score(X_train, y_train))
print('R Squared value on Test = ', dtr.score(X_test, y_test))

"""## **(4) Random Forest Regressor**

"""

# Random Forest Regressor
rfr = RandomForestRegressor()
rfr.fit(X_train, y_train)

# Predicting the values:
train_pred = rfr.predict(X_train) # Predicting train
test_pred = rfr.predict(X_test) # Predicting test

# Evaluation for Randome Forest Regressor
RMSE_train = (np.sqrt(mean_squared_error(y_train, train_pred)))
RMSE_test = (np.sqrt(mean_squared_error(y_test, test_pred)))
print('RMSE Train Data = ', str(RMSE_train))
print('RMSE Test Data = ', str(RMSE_test))
print('_'* 60)
print('R Squared value for Train = ', rfr.score(X_train, y_train))
print('R Squared value on Test = ', rfr.score(X_test, y_test))