import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#data derived from stooq and WSJ (01-01-2006, 07-31-2026)

xauusd = pd.read_csv("PATH/xauusd_d.csv", skipinitialspace = True)
xauusd["Date"] = pd.to_datetime(xauusd["Date"])
xauusd = xauusd.sort_values("Date").reset_index(drop = True)
xauusd = xauusd.set_index("Date")

xagusd = pd.read_csv("PATH/xagusd_d.csv", skipinitialspace = True)
xagusd["Date"] = pd.to_datetime(xagusd["Date"])
xagusd = xagusd.sort_values("Date").reset_index(drop = True)
xagusd = xagusd.set_index("Date")

dxy = pd.read_csv("PATH/dxy_wsj.csv", skipinitialspace = True)
dxy["Date"] = pd.to_datetime(dxy["Date"])
dxy = dxy.sort_values("Date").reset_index(drop = True)
dxy = dxy.set_index("Date")

print(dxy)
print(xauusd.columns.tolist())
print(xagusd.columns.tolist())
print(dxy.columns.tolist())

xauusd_close = xauusd[["Close"]].rename(columns = {"Close": "gold"})

xagusd_close = xagusd[["Close"]].rename(columns = {"Close": "silver"})

dxy_close = dxy[["Close"]].rename(columns = {"Close": "dxy"})

master = xauusd_close.join([xagusd_close, dxy_close], how = "inner") #keeping only rows that match

master1 = pd.DataFrame.merge(xauusd_close, xagusd_close, left_on = "Date", right_index = True, how = "outer")
master1 = pd.DataFrame.merge(master1, dxy_close, left_on = "Date", right_index = True, how = "outer") #keeping all rows, even without a match

master2 = pd.DataFrame.merge(xauusd_close, xagusd_close, left_index = True, right_index = True, how = "left")
master2 = pd.DataFrame.merge(master2, dxy_close, left_index = True, right_index = True, how = "left") #keeping all rows that have a match with the left dataframe

print(master)
print(master.isnull().sum())
print(master1)
print(master1.isnull().sum())
print(master2)
print(master2.isnull().sum())

master_long = pd.melt(master.reset_index(), id_vars = "Date", var_name = "asset", value_name = "price")

print(master_long)
print(master_long.groupby("asset")["price"].mean())

returns = master.pct_change()

master.insert(3, "gold/silver_ratio", master["gold"] / master["silver"])

print(master)

master.insert(4, "rolling_corr", returns["gold"].rolling(252).corr(returns["dxy"]))

print(master)

returns.insert(3, "ann_vol_gold", returns["gold"].rolling(252).std() * np.sqrt(252))
returns.insert(3, "ann_vol_silver", returns["silver"].rolling(252).std() * np.sqrt(252))
returns.insert(3, "ann_vol_dxy", returns["dxy"].rolling(252).std() * np.sqrt(252))

master.insert(5, "regime", np.where(master["gold/silver_ratio"] > master["gold/silver_ratio"].quantile(0.75), "high", "low"))

fig, ax1 = plt.subplots(figsize = (14, 6))

ax1.plot(master["gold"], label = "Gold", color = "gold")
ax1.set_ylabel("Gold Price (USD)")

ax2 = ax1.twinx()

ax2.plot(master["dxy"], label = "DXY", color = "blue")
ax2.set_ylabel("DXY Index")

ax3 = ax1.twinx()

ax3.spines["right"].set_position(("outward", 60))
ax3.plot(master["silver"], label = "Silver", color = "gray")
ax3.set_ylabel("Silver Price (USD)")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3)

plt.title("Gold, Silver & DXY Price History")
plt.show()

fig1, ax4 = plt.subplots(figsize = (14, 6))

ax4.plot(master["gold/silver_ratio"], label = "gold_silver_ratio", color = "black")
ax4.axhline(y = master["gold/silver_ratio"].mean(), color = "red", linestyle = "--", label = "Mean")

ax4.legend()

plt.title("Gold to Silver Ratio Over Time")
plt.show()

fig1, ax5 = plt.subplots(figsize = (14, 6))

ax5.plot(master["rolling_corr"], label = "gold_dxy_correlation", color = "black")
ax5.axhline(y = 0, color = "red", linestyle = "--", label = "Baseline")

ax5.legend()

plt.title("Gold to DXY (252 days) Rolling Correlation Over Time")
plt.show()

fig1, ax6 = plt.subplots(figsize = (14, 6))

master["gold_return"] = master["gold"].pct_change()
master["dxy_return"] = master["dxy"].pct_change()

high = master[master["regime"] == "high"]
low = master[master["regime"] == "low"]

print(master.columns.tolist())

ax6.scatter(high["dxy_return"], high["gold_return"], label = "high", color = "green")
ax6.scatter(low["dxy_return"], low["gold_return"], label = "low", color = "red")

clean = master[["dxy_return", "gold_return"]].dropna()

coeffs = np.polyfit(clean["dxy_return"], clean["gold_return"], 1)
x_line = np.linspace(clean["dxy_return"].min(), clean["dxy_return"].max(), 100)
y_line = np.polyval(coeffs, x_line)

ax6.plot(x_line, y_line, color = "blue", linewidth = 2, label = "Regression")

ax6.legend()

plt.title("Gold to Silver Ratio Regimes (High/Low)")
plt.show()

print(master.describe())

print(master["regime"].value_counts())

top10 = master[["gold_return", "dxy_return"]].assign(abs_gold = master["gold_return"].abs()).sort_values("abs_gold", ascending= False).head(10).drop(columns = "abs_gold")

print(top10)
