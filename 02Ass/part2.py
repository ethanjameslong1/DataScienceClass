#!usr/bin/python3

# URL FOR DATASET: https://www.kaggle.com/datasets/samuelotiattakorah/agriculture-crop-yield?resource=download

# Data set is Agriculture Crop Yield from Kaggle.com, 1000000 samplse useful for prediciting crop yield based on various variables

import pandas as pd
import numpy as np
import time


def reduce_mem_usage(df, verbose=True):
    numerics = ["int8", "int16", "int32", "int64", "float32", "float64"]
    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            prevType = col_type
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                    newType = "int8"
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                    newType = "int16"
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                    newType = "int32"
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
                    newType = "int64"
            else:
                if (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)
                    newType = "float32"
                else:
                    df[col] = df[col].astype(np.float64)
                    newType = "float64"
            if verbose and (newType != prevType):
                print(col, " was ", prevType, " changed to ", newType)
    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    if verbose:
        print(
            "Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)".format(
                end_mem, 100 * (start_mem - end_mem) / start_mem
            )
        )
    return df


file = r"crop_yield.csv"
req_cols = [
    "Rainfall_mm",
    "Temperature_Celsius",
    "Days_to_Harvest",
    "Yield_tons_per_hectare",
]
chunk_size = 100000
stats = {col: {"min": np.inf, "max": -np.inf, "sum": 0, "count": 0} for col in req_cols}
df_it = chunk_iterator = pd.read_csv(file, usecols=req_cols, chunksize=chunk_size)

for i, chunk in enumerate(chunk_iterator):
    chunk = reduce_mem_usage(chunk, verbose=True)
    for col in req_cols:
        curren_min = chunk[col].min()
        if curren_min < stats[col]["min"]:
            stats[col]["min"] = curren_min
        curren_max = chunk[col].max()
        if curren_max > stats[col]["max"]:
            stats[col]["max"] = curren_max
        stats[col]["sum"] += chunk[col].sum()
        stats[col]["count"] = chunk[col].count()
print("-" * 60)
print(f"{'Column':<25} | {'Min':<10} | {'Max':<10} | {'Mean':<10}")
print("-" * 60)

for col in req_cols:
    final_mean = stats[col]["sum"] / stats[col]["count"]
    print(
        f"{col:<25} | {stats[col]['min']:<10.2f} | {stats[col]['max']:<10.2f} | {final_mean:<10.2f}"
    )

print("-" * 60)
