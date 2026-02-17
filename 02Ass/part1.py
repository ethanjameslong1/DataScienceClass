#!usr/bin/python3

# Data set is the hate-crimes dataset from course materials

import pandas as pd
import scipy
from scipy import stats
import statistics

file = r"hate-crimes/hate_crimes.csv"
df = pd.read_csv(file, encoding="ISO-8859-1")
print(df)


def AttributeInfo(attribute):
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


def FixAttributeInfo(attribute):
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
    # print("Standard Deviation - ", statistics.stdev(df[attribute]))


# for col in df.columns:
#     print("Column: ", col)
#     print(df[col].dtype)

print(AttributeInfo("median_household_income"))
print(AttributeInfo("share_unemployed_seasonal"))
print(AttributeInfo("share_population_in_metro_areas"))
print(AttributeInfo("share_population_with_high_school_degree"))
print(FixAttributeInfo("share_non_citizen"))
print(AttributeInfo("share_white_poverty"))
print(AttributeInfo("gini_index"))
print(AttributeInfo("share_non_white"))
print(AttributeInfo("share_voters_voted_trump"))
print(FixAttributeInfo("hate_crimes_per_100k_splc"))
print(FixAttributeInfo("avg_hatecrimes_per_100k_fbi"))
