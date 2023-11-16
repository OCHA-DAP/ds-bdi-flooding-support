---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.15.2
  kernelspec:
    display_name: ds-aa-bdi-flooding
    language: python
    name: ds-aa-bdi-flooding
---

# Lake level

```python
%load_ext jupyter_black
%load_ext autoreload
%autoreload 2
```

```python
import matplotlib.pyplot as plt
import numpy as np

from src import utils
```

```python
LEVEL = "water_surface_height_above_reference_datum"
```

```python
ds = utils.load_lake_level()
ds
```

```python
df = ds[LEVEL].to_dataframe().reset_index()
```

```python
df["month"] = df["time"].dt.month
df["year"] = df["time"].dt.year
df["day_of_year"] = df["time"].dt.dayofyear
```

```python
df.plot(x="time", y=LEVEL)
```

```python
df.pivot_table(
    index="day_of_year",
    columns="year",
    values=LEVEL,
).interpolate().plot()
```

```python
max_per_year = (
    df.groupby("year")[LEVEL].max().sort_values().to_frame().reset_index()
)
max_per_year["rank"] = len(max_per_year) - max_per_year.index
max_per_year["return_period"] = 1 / max_per_year["rank"] * len(max_per_year)
max_per_year
```

```python
rp3 = np.interp(3, max_per_year["return_period"], max_per_year[LEVEL])
```

```python
rp3
```

```python
fig, ax = plt.subplots()
max_per_year.plot(x="return_period", y=LEVEL, ax=ax)
ax.plot(3, rp3, marker=".")
ax.annotate(f"  3-year return period = {rp3}m", [3, rp3], va="center")
ax.set_xlabel("Return period (years)")
ax.set_ylabel("Water level (m)\n(measured above reference datum)")
ax.set_title("Return period for water level in Lake Tanganyika, since 1992")
ax.legend().remove()
```

```python

```

```python

```
