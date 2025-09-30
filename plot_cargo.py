# %%
import polars as pl
import matplotlib.pyplot as plt
import numpy as np

import plotly.express as px


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
    profit = cargo_base * amount * distance * max(31, multiplier) * 1 / (2**21)
    return profit


def income_formula_speed(cargo, amount, distance, speed):
    cargo_base = cargo["price_factor"]
    c_days_1 = cargo["single_penalty_length"]
    c_days_2 = cargo["penalty_lowerbound"]
    time = distance / (speed * 3.6 / 100)  # convert speed from km/h to tiles/day
    if time <= c_days_1:
        multiplier = 255
    elif c_days_1 < time <= c_days_1 + c_days_2:
        multiplier = 255 - (time - c_days_1)
    else:
        multiplier = 255 - 2 * (time - c_days_1) + c_days_2
    profit = cargo_base * amount * distance * max(31, multiplier) * 1 / (2**21)
    return profit


def income_formula_speed_mesh(cargo, amount, distance, speed):
    c_days_1 = cargo["single_penalty_length"]
    c_days_2 = cargo["penalty_lowerbound"]
    time = distance / (speed * 3.6 / 100)  # convert speed from km/h to tiles/day
    multiplier = np.ones_like(time) * 255
    mask_1 = (time > c_days_1) & (time <= c_days_1 + c_days_2)
    mask_2 = time > c_days_1 + c_days_2
    multiplier[mask_1] = 255 - (time[mask_1] - c_days_1)
    multiplier[mask_2] = 255 - 2 * (time[mask_2] - c_days_1) + c_days_2
    multiplier[multiplier < 31] = 31
    profit = cargo["price_factor"] * amount * distance * multiplier * 1 / (2**21)
    return profit


cargos = [
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
df = pl.read_csv("data/cargo_stats.csv").unique("id")

# %%
plot_data = []
for cargo in df.iter_rows(named=True):
    if cargo["id"] not in cargos:
        continue
    times = np.arange(1, 500)
    profits = [income_formula_time(cargo, 100, 100, t) for t in times]
    plot_data.append(
        {"Days": times, "Profit": profits, "Cargo": [cargo["id"]] * len(times)}
    )

import pandas as pd

all_data = pd.concat([pd.DataFrame(d) for d in plot_data], ignore_index=True)
fig = px.line(
    all_data, x="Days", y="Profit", color="Cargo", title="Cargo Profit Over Time"
)
fig.show()

# %%
dist = 300
plot_data = []
for cargo in df.iter_rows(named=True):
    if cargo["id"] not in cargos:
        continue
    speed = np.arange(1, 300)
    profits = [income_formula_speed(cargo, 100, dist, t) for t in speed]
    plot_data.append(
        {"Speed": speed, "Profit": profits, "Cargo": [cargo["id"]] * len(speed)}
    )

import pandas as pd

all_data = pd.concat([pd.DataFrame(d) for d in plot_data], ignore_index=True)
fig = px.line(
    all_data,
    x="Speed",
    y="Profit",
    color="Cargo",
    title=f"Cargo Profit over Speed ({dist} tiles)",
)
fig.show()
# %%
# Contour plot distance vs speed
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(
    title="Cargo Profit over Distance and Speed",
    scene=dict(
        xaxis_title="Distance (tiles)",
        yaxis_title="Speed (km/h)",
        zaxis_title="Profit (G)",
    ),
)

cargo_base = 137

cargo = {
    "id": "passengers",
    "price_factor": cargo_base,
    "single_penalty_length": 22,
    "penalty_lowerbound": 0,
}
distance = np.linspace(50, 1000, 50)
speed = np.linspace(1, 300, 50)
D, S = np.meshgrid(distance, speed)
Z = income_formula_speed_mesh(cargo, 100, D, S)
fig.add_trace(
    go.Surface(z=Z, x=D, y=S, name="passengers", showscale=False, opacity=0.7)
)


fig.show()
# %%
# rewrite the plot above using matplotlib contour instead
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fig, ax = plt.subplots(figsize=(10, 6))
contour = ax.contourf(D, S, Z, levels=50, cmap="viridis")
fig.colorbar(contour, ax=ax, label="Profit (G)")
ax.set_xlabel("Distance (tiles)")
ax.set_ylabel("Speed (km/h)")
ax.set_title("Cargo Profit over Distance and Speed")
plt.show()
# %%
