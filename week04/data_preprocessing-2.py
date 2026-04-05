# -*- coding: utf-8 -*-

# Import necessary libraries
import numpy as np
import pandas as pd

# Load the housing dataset (make sure housing.csv is in the same folder)
housing = pd.read_csv('housing.csv')

# -------------------------------
# Create test set using stratified sampling
# -------------------------------
from sklearn.model_selection import train_test_split

# Create income categories based on median income
housing["income_cat"] = pd.cut(
    housing["median_income"],
    bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
    labels=[1, 2, 3, 4, 5]
)

# Split the dataset into training and test sets (80% train, 20% test)
# Stratified sampling ensures similar income distribution in both sets
strat_train_set, strat_test_set = train_test_split(
    housing,
    test_size=0.2,
    stratify=housing["income_cat"],
    random_state=42
)

# Remove the temporary income category column from both sets
for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

# -------------------------------
# Prepare training data
# -------------------------------

# Separate features and target (median_house_value)
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

# -------------------------------
# Data cleaning (handling missing values)
# -------------------------------

# Find rows with missing values
null_rows_idx = housing.isnull().any(axis=1)

# Show some rows with missing values (for checking)
housing.loc[null_rows_idx].head()

from sklearn.impute import SimpleImputer

# Create imputer to fill missing values using median
imputer = SimpleImputer(strategy="median")

# Select only numerical columns
housing_num = housing.select_dtypes(include=[np.number])

# Fit the imputer to the numerical data
imputer.fit(housing_num)

# Print calculated median values (for verification)
print(imputer.statistics_)
print(housing_num.median().values)

# Replace missing values using the learned medians
X = imputer.transform(housing_num)

# Convert back to DataFrame
housing_tr = pd.DataFrame(
    X,
    columns=housing_num.columns,
    index=housing_num.index
)

# -------------------------------
# Remove outliers
# -------------------------------

from sklearn.ensemble import IsolationForest

# Detect outliers using Isolation Forest
isolation_forest = IsolationForest(random_state=42)
outlier_pred = isolation_forest.fit_predict(X)

# Keep only normal data points (label = 1)
housing = housing.iloc[outlier_pred == 1]
housing_labels = housing_labels.iloc[outlier_pred == 1]

# -------------------------------
# Handle categorical data
# -------------------------------

# Select categorical column
housing_cat = housing[["ocean_proximity"]]

from sklearn.preprocessing import OrdinalEncoder

# Convert categorical values into numbers
ordinal_encoder = OrdinalEncoder()
housing_cat_encoded = ordinal_encoder.fit_transform(housing_cat)

# Show first few encoded values
print(housing_cat_encoded[:8])

# Show category mapping
print(ordinal_encoder.categories_)