import pandas as pd

file = "Mod4-Support-Files/hate_crimes.csv"
df = pd.read_csv(file, encoding="ISO-8859-1")

# print("name of columns", df.columns)
# for c in df.columns:
#     print(df[c].dtype)
# print(df.info)

# VAR
dfTrump = df.filter(["share_voters_voted_trump"])
print("variance Share Voters Voted Trump = ", dfTrump.var())
dfNonWhite = df.filter(["share_non_white"])
print("variance Non-White= ", dfNonWhite.var())
dfHS = df.filter(["share_population_with_high_school_degree"])
print("variance HS Degree = ", dfHS.var())

# CO-Var
dfTrumpNonWhite = df.filter(["share_voters_voted_trump", "share_non_white"])
print("covariance Trump - Non White = ")
print(dfTrumpNonWhite.cov())
print("***********")
tex = "Negative covariance! This means that the two variables move opposite eachother, more non-white people mean less trump voters."
print(tex)


dfTrumpHSDegree = df.filter(
    ["share_voters_voted_trump", "share_population_with_high_school_degree"]
)
print("covariance Trump - HS Degree = ")
print(dfTrumpHSDegree.cov())
print("***********")
tex = "Negative covariance! This means that the two variables move opposite eachother, more HS graduates mean less trump voters. This difference is more subtle than the previous trump - nonwhite one."
print(tex)

dfNonWhiteHSDegree = df.filter(
    ["share_non_white", "share_population_with_high_school_degree"]
)
print("covariance Non White - HS Degree = ")
print(dfNonWhiteHSDegree.cov())
print("***********")
tex = "Negative covariance again. As the non-white population increases the amount of high school graduates decreases"
print(tex)

# Correlation
print("correlation Trump - Non White = ")
print(dfTrumpNonWhite.corr())
print("***********")
tex = "A negative and pretty strong correlation implies that non-white people are noticably less likely to vote for trump"
print(tex)

print("correlation Trump HS Degree = ")
print(dfTrumpHSDegree.corr())
print("***********")
tex = "A negative but very weak correlation implies very little about the relationship."
print(tex)

print("correlation Non White HS Degree = ")
print(dfNonWhiteHSDegree.corr())
print("***********")
tex = "A negative and pretty strong correlation seems to imply that larger non-white populations tend to have lower graduation rates."
print(tex)


"""
python3 mod4VarCovarCorr.py
name of columns Index(['state',
'median_household_income',
'share_unemployed_seasonal',
'share_population_in_metro_areas',
'share_population_with_high_school_degree',
'share_non_citizen',
'share_white_poverty',
'gini_index',
'share_non_white',
'share_voters_voted_trump',
'hate_crimes_per_100k_splc',
'avg_hatecrimes_per_100k_fbi']
object                                                                                                                            │
int64                                                                                                                             │
float64                                                                                                                           │
float64                                                                                                                           │
float64                                                                                                                           │
float64                                                                                                                           │
float64                                                                                                                           │
float64                                                                                                                           │
float64                                                                                                                           │
float64                                                                                                                           │
float64                                                                                                                           │
float64  
"""
