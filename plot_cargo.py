# %%
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import plotly.express as px
import plotly.io as pio

# %% 
def income_formula_time(cargo, amount, distance, time):
    cargo_base = cargo["price_factor"]
    c_days_1 = cargo["single_penalty_length"]
    c_days_2 = cargo["penalty_lowerbound"]
    if time <= c_days_1:
        multiplier = 255
    elif c_days_1 < time <= c_days_1 + c_days_2:
        multiplier = 255 - (time - c_days_1)
    else:
        multiplier = 255 - 2 * (time - c_days_1) + c_days_2
    profit = cargo_base * amount * distance * max(31, multiplier) * 1/(2**21)
    return profit
    

cargos=[
    "passengers",
    "alcohol",
    "mail",
    "chemicals",
    "coal",
    "goods",
    "engineering_supplies",
    "farm_supplies",
    "fish",
    "fruits",
    "iron_ore",
    "food",
    "kaolin",
    "livestock",
    "milk",
    "sand",
    "scrap_metal",
    "steel",
]





# %% 
df = pl.read_csv("cargo_stats.csv")

#%% 
plot_data = []
for cargo in df.iter_rows(named=True):
    if cargo["id"] not in cargos:
        continue
    times = np.arange(1, 500)
    profits = [income_formula_time(cargo, 100, 100, t) for t in times]
    plot_data.append({
        "Days": times,
        "Profit": profits,
        "Cargo": [cargo["id"]]*len(times)
    })

import pandas as pd
all_data = pd.concat([pd.DataFrame(d) for d in plot_data], ignore_index=True)
fig = px.line(all_data, x="Days", y="Profit", color="Cargo", title="Cargo Profit Over Time")
fig.show()

#%% 
plot_data = []
for cargo in df.iter_rows(named=True):
    if cargo["id"] not in cargos:
        continue
    speed = np.arange(1, 500)
    profits = [income_formula_time(cargo, 100, 100, t) for t in speed]
    plot_data.append({
        "Speed": speed,
        "Profit": profits,
        "Cargo": [cargo["id"]]*len(speed)
    })

import pandas as pd
all_data = pd.concat([pd.DataFrame(d) for d in plot_data], ignore_index=True)
fig = px.line(all_data, x="Days", y="Profit", color="Cargo", title="Cargo Profit Over Time")
fig.show()