import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# I'm using a data set I found on kaggle, the link is below it's called billionaires data by country
# https://www.kaggle.com/datasets/rafsunahmad/billionaires-data-by-country-2024
df = pd.read_csv("billionaires-by-country-2024.csv")

print(f"Dataset Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head())

# Boxplot
plt.figure(figsize=(10, 5))
sns.boxplot(x=df["BillionairesRichestNetWorth2023"])
plt.title("Original Boxplot (With Outliers)")
plt.show()

# Scatter Plot
plt.figure(figsize=(12, 6))
plt.scatter(
    df["population_densityMi"], df["BillionairesRichestNetWorth2023"], alpha=0.5
)
plt.xlabel("Population Density (Mi)")
plt.ylabel("Billionaire Networth ($B)")
plt.title("Original Scatter Plot (With Outliers)")
plt.show()

drop_net_worth = np.where(df["BillionairesRichestNetWorth2023"] > 30)[0]
drop_density = np.where(df["population_densityMi"] > 10000)[0]
all_drop_indices = np.unique(np.concatenate((drop_net_worth, drop_density)))

df.drop(all_drop_indices, inplace=True)
plt.figure(figsize=(10, 5))
sns.boxplot(x=df["BillionairesRichestNetWorth2023"])
plt.title("Cleaned Boxplot: Outliers Removed")
plt.show()

plt.figure(figsize=(12, 6))
plt.scatter(
    df["population_densityMi"],
    df["BillionairesRichestNetWorth2023"],
)
plt.xlabel("Population Density (Mi)")
plt.ylabel("Billionaire Networth ($B)")
plt.title("Cleaned Scatter Plot: Outliers Removed")
plt.show()
