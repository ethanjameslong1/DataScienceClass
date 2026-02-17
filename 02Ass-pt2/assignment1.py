#!usr/bin/python3
import pandas as pd
import numpy as np

file = "hate-crimes/hate_crimes.csv"
df = pd.read_csv(file, encoding="ISO-8859-1")
print(f"Data Loaded Successfully. Total rows: {df.shape[0]}\n")

n_total = df.shape[0]

# A1: Share population with high school degree > 0.85
df_A1 = df[df["share_population_with_high_school_degree"] > 0.85]
p_A1 = df_A1.shape[0] / n_total

# A2: Share voters voted trump < 0.5
df_A2 = df[df["share_voters_voted_trump"] < 0.5]
p_A2 = df_A2.shape[0] / n_total

# A3: Share non citizen > Median
median_non_citizen = df["share_non_citizen"].median()
print(f"Median for 'share_non_citizen': {median_non_citizen}")

df_A3 = df[df["share_non_citizen"] > median_non_citizen]
p_A3 = df_A3.shape[0] / n_total

print("Marginal Probabilities")
print("P(A1) HS Degree:", p_A1)
print("P(A2) Trump:", p_A2)
print("P(A3) Non-Citizen:", p_A3)
print("\n\n")

# P(A1 v A2)
# Formula: P(A1) + P(A2) - P(A1 and A2)
df_A1_and_A2 = df[
    (df["share_population_with_high_school_degree"] > 0.85)
    & (df["share_voters_voted_trump"] < 0.5)
]
p_A1_and_A2 = df_A1_and_A2.shape[0] / n_total

p_A1_or_A2 = p_A1 + p_A2 - p_A1_and_A2

# P(A1 AND A3)
df_A1_and_A3 = df[
    (df["share_population_with_high_school_degree"] > 0.85)
    & (df["share_non_citizen"] > median_non_citizen)
]
p_A1_and_A3 = df_A1_and_A3.shape[0] / n_total

print("P(A1 v A2) [Union]: ", p_A1_or_A2)
print("P(A1, A3)  [Intersection]: ", p_A1_and_A3)
print("\n")


# Compute P(A2 | A1, A3)
# Formula: P(A2 and A1 and A3) / P(A1 and A3)

df_A1_A2_A3 = df[
    (df["share_population_with_high_school_degree"] > 0.85)
    & (df["share_voters_voted_trump"] < 0.5)
    & (df["share_non_citizen"] > median_non_citizen)
]
p_A1_A2_A3 = df_A1_A2_A3.shape[0] / n_total

if p_A1_and_A3 == 0:
    p_A2_given_A1_A3 = 0
else:
    p_A2_given_A1_A3 = p_A1_A2_A3 / p_A1_and_A3

print("P(A2 | A1, A3): ", p_A2_given_A1_A3)
print("\n")


# Compute P(A1, A3 | A2) using Bayes
# Formula: ( P(A2 | A1, A3) * P(A1, A3) ) / P(A2)
if p_A2 == 0:
    p_A1_A3_given_A2 = 0
else:
    p_A1_A3_given_A2 = (p_A2_given_A1_A3 * p_A1_and_A3) / p_A2

print("P(A1, A3 | A2): ", p_A1_A3_given_A2)
