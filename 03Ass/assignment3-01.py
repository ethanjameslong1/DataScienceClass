#!usr/bin/python3
import pandas as pd
import numpy as np

# Geometric Mean of the column in dataframe
import scipy
from scipy import stats
import statistics


def combine_files(df1, df2):
    dfAll = pd.concat([df1, df2])
    return dfAll


def print_non_numerics(df):
    non_numeric_df = df.select_dtypes(exclude=["number"])
    for col in non_numeric_df.columns:
        print(f"--- {col} ---")
        print(non_numeric_df[col].value_counts())
        print("\n")


def FixAttributeInfo(attribute, df):
    # get information on attributes
    print("**********************")
    print(attribute)
    print("Possible values - ", df[attribute].unique())
    print("value counts - ")
    print(df[attribute].value_counts())
    print("Max - ", df[attribute].max())
    print("Min - ", df[attribute].min())
    print("Central Tendency")
    print("Mean - ", df[attribute].mean())
    print("Median - ", df[attribute].median())
    print("Geometric mean - ", scipy.stats.gmean(df[attribute]))
    print("Variance Metric")


def AttributeInfo(attribute, df):
    # get information on attributes
    print("**********************")
    print(attribute)
    print("Possible values - ", df[attribute].unique())
    print("value counts - ")
    print(df[attribute].value_counts())
    print("Max - ", df[attribute].max())
    print("Min - ", df[attribute].min())
    print("Central Tendency")
    print("Mean - ", df[attribute].mean())
    print("Median - ", df[attribute].median())
    print("Geometric mean - ", scipy.stats.gmean(df[attribute]))
    print("Variance Metric")
    print("Standard Deviation - ", statistics.stdev(df[attribute]))


df1 = pd.read_csv("data/GlobalLandTemperaturesByCountry.csv")
df2 = pd.read_csv("data/billionaires-by-country-2024.csv")
df1 = df1.rename(columns={"Country": "country"})
dfAll = pd.merge(df1, df2, on="country")
print(df1)
print(df2)
print(dfAll)


AttributeInfo("population_densityMi", dfAll)
FixAttributeInfo("AverageTemperature", dfAll)
print_non_numerics(dfAll)
