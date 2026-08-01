import numpy as np
import pandas as pd
import pandas_datareader as pdr

#data derived from FRED on 07/30/2026

two = pdr.data.DataReader("DGS2", "fred", "2020-01-01", "2025-07-29")

five = pdr.data.DataReader("DGS5", "fred", "2020-01-01", "2025-07-29")

ten = pdr.data.DataReader("DGS10", "fred", "2020-01-01", "2025-07-29")

twenty = pdr.data.DataReader("DGS20", "fred", "2020-01-01", "2025-07-29")

thirty = pdr.data.DataReader("DGS30", "fred", "2020-01-01", "2025-07-29")

yields = pd.concat([two, five, ten, twenty, thirty], axis = 1).rename(columns = {"DGS2": "2y","DGS5": "5y","DGS10": "10y","DGS20": "20y","DGS30": "30y"})

yields = yields.ffill().bfill()

print(yields)

yields_change = yields.diff()

print(yields_change)

highest_changes = {}

for tenure in yields_change.columns:

    top_five = np.abs(yields_change[tenure]).sort_values(ascending = False).head()
    highest_changes[tenure] = yields_change[tenure].loc[top_five.index]

print(highest_changes)

spreads = pd.DataFrame({

    "2s10s": yields["10y"] - yields ["2y"],
    "5s30s": yields["30y"] - yields ["5y"]

})

result_two_ten = spreads[spreads["2s10s"] < 0]
result_five_thirty = spreads[spreads["5s30s"] < 0]

print(result_two_ten, result_five_thirty)

descriptive_stats = ["mean", "std", "min", "max"]

print("Yields descrpitive statistics\n", yields.describe().loc[descriptive_stats].to_string())

print("Spreads descriptive statistics\n", spreads.describe().loc[descriptive_stats].to_string(),"\nDays inverted 2s10s:", (spreads["2s10s"] < 0).sum(),"\nDays inverted 5s30s:", (spreads["5s30s"] < 0).sum())
