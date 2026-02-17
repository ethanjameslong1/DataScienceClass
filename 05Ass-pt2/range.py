import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# I'm using a data set I found on kaggle, the link is below it's called billionaires data by country
# https://www.kaggle.com/datasets/rafsunahmad/billionaires-data-by-country-2024
file = r"billionaires-by-country-2024.csv"
df = pd.read_csv(file)


def popDensityToLandArea(popDens, l):
    return 1000 * popDens / l


df["PopDensetoLand"] = df[["population_densityMi", "Country_land_area"]].apply(
    lambda x: popDensityToLandArea(x.population_densityMi, x.Country_land_area),
    axis=1,
)

drop_pop_dense_to_land = np.where(df["population_densityMi"] > 100)[0]
df.drop(drop_pop_dense_to_land, inplace=True)

plt.scatter(df["PopDensetoLand"], df["BillionairesPerMillionPeople2023"], alpha=0.5)
plt.xlabel("Population Density to Land Area Ratio")
plt.ylabel("Billionaires Per Million People")
plt.title("Scatterplot")
plt.show()
