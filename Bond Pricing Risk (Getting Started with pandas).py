import numpy as np

#data derived from Bloomberg after market close on 07/30/2026

bonds = np.array([[1, 1000, 0, 0.0402],[2, 1000, 0.0425, 0.0427],[5, 1000, 0.0438, 0.0441],[10, 1000, 0.0438, 0.0468],[30, 1000, 0.05, 0.052]])

maturities = np.array([1, 2, 5, 10, 30])
face_values = np.array([1000, 1000, 1000, 1000, 1000])
coupon_rates = np.array([0, 0.0425, 0.0438, 0.0438, 0.05])
yields = np.array([0.0402, 0.0427, 0.0441, 0.0468, 0.052])

pv = ((face_values * coupon_rates) / yields) * (1 - (1 / (1 + yields) ** maturities)) + (face_values / ((1 + yields) ** maturities))
print(pv)

yields_change_up = yields + 0.0001
dv01_up = ((face_values * coupon_rates) / yields_change_up) * (1 - (1 / (1 + yields_change_up) ** maturities)) + (face_values / ((1 + yields_change_up) ** maturities))

yields_change_down = yields - 0.0001
dv01_down = ((face_values * coupon_rates) / yields_change_down) * (1 - (1 / (1 + yields_change_down) ** maturities)) + (face_values / ((1 + yields_change_down) ** maturities))

dv01_change = np.column_stack([dv01_down, dv01_up])
print(dv01_change)

dv01 = np.abs(dv01_down - dv01_up) / 2
print(dv01)

modified_duration = dv01 / (pv * 0.0001)
print(modified_duration)

macaulay = modified_duration * (1 + yields)
print(macaulay)

summary = np.column_stack([maturities, pv, dv01, modified_duration, macaulay])

np.set_printoptions(precision=4, suppress=True)

print(f"{'Maturity':>10} {'Price':>10} {'DV01':>10} {'Mod Dur':>10} {'Mac Dur':>10}")
print("-" * 52)
for row in summary:
    print(f"{row[0]:>10.0f} {row[1]:>10.4f} {row[2]:>10.4f} {row[3]:>10.4f} {row[4]:>10.4f}")
