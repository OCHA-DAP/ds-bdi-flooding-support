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

# CHIRPS

```python
%load_ext jupyter_black
%load_ext autoreload
%autoreload 2
```

```python
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from ochanticipy import (
    create_country_config,
    CodAB,
    ChirpsDaily,
    GeoBoundingBox,
)

from src import utils
```

```python
country_config = create_country_config("bdi")
cod = CodAB(country_config)
cod.download()
adm2 = cod.load(admin_level=2)
adm0 = adm2.dissolve()
geobb = GeoBoundingBox.from_shape(adm2)
```

```python
chirpsdaily = ChirpsDaily(
    country_config=country_config,
    geo_bounding_box=geobb,
)
```

```python
# chirpsdaily.download()
# chirpsdaily.process()
```

```python
ds = chirpsdaily.load()
```

```python
da = ds["precipitation"]
da_clip = da.rio.clip(adm0.geometry, all_touched=True)
df = da_clip.to_dataframe()
df = df.reset_index().drop(columns="spatial_ref")
total_pixels = len(df.dropna().groupby(["X", "Y"]).size().reset_index())
```

```python
# save as single file to not rely on AnticiPy loading ~15k processed files
save_dir = utils.DATA_DIR / "public" / "processed" / "bdi" / "chirps"
filename = "bdi_chirps_daily_1981_01_01_to_2023_09_30_r0.05_Nm2Sm4Ep31Wp29.nc"
# remove missing_value as it conflicts with with _FillValue
da.encoding.pop("missing_value")
da.to_netcdf(save_dir / filename)
```

```python
fig, ax = plt.subplots(figsize=(8, 8))
adm0.boundary.plot(ax=ax, color="k", linewidth=0.5)
ax.axis("off")
da_clip.mean(dim="T").plot(ax=ax)
```

```python
df["year"] = df["T"].dt.year
df["month"] = df["T"].dt.month
```

```python
df = df[df["year"] != 2023]
```

```python
fig, ax = plt.subplots()
df.groupby(["year", "month"])["precipitation"].mean().reset_index().pivot(
    index="month", columns="year"
).plot(ax=ax, linewidth=0.3)
ax.legend().remove()
ax.set_xlim([1, 12])
ax.set_ylabel("Mean daily precipitation in month (mm)")
ax.set_title("Mean daily precipitation monthly by month, 1981-2022")
```

```python

```

```python
fig, ax = plt.subplots()
mean_by_T = df.groupby("T")["precipitation"].mean().reset_index()
mean_by_T["month"] = mean_by_T["T"].dt.month
count_per_month = mean_by_T.loc[
    mean_by_T.groupby(mean_by_T["T"].dt.year)["precipitation"].idxmax()
]["month"].value_counts()
# count_per_month = df.loc[df.groupby("year")["precipitation"].idxmax()][
#     "month"
# ].value_counts()
count_per_month[6] = 0
count_per_month[7] = 0
count_per_month[8] = 0
count_per_month.sort_index().plot.bar()
ax.set_ylabel("Years in which the rainiest day\nwas in this month")
ax.set_title("Distribution of rainiest day in the year, 1981-2022")
```

```python
df.groupby("T")["precipitation"].mean().reset_index().plot(
    x="T", y="precipitation"
)
```

```python
df_gte50 = df[df["precipitation"] >= 50]
```

```python
df_q = (
    df_gte50.groupby("T")
    .size()
    .reset_index()
    .rename(columns={0: "count_gte50"})
)
```

```python
df_q["frac_gte50"] = df_q["count_gte50"] / total_pixels
```

```python
max_per_year = (
    df_q.groupby(df_q["T"].dt.year)["frac_gte50"]
    .max()
    .sort_values()
    .reset_index()
)

# max_per_year = max_per_year.sort_values("frac_gte50")
max_per_year["rank"] = len(max_per_year) - max_per_year.index
max_per_year["return_period"] = 1 / max_per_year["rank"] * len(max_per_year)
rp3 = np.interp(3, max_per_year["return_period"], max_per_year["frac_gte50"])
max_per_year
```

```python
fig, ax = plt.subplots()
max_per_year.plot(x="return_period", y="frac_gte50", ax=ax)
ax.plot(3, rp3, marker=".")
ax.annotate(f"  3-year return period = {rp3:.2}", [3, rp3], va="center")
ax.set_title("Return period of fraction of Burundi with daily precip > 50 mm")
ax.set_xlabel("Return period (years)")
ax.set_ylabel("Fraction of Burundi")
ax.legend().remove()
```

```python
plot_years = [1986, 2016, 2007]

cmap = plt.get_cmap("viridis")
cmap.set_over("red")
for year in plot_years:
    T = (
        df[df["T"].dt.year == year]
        .groupby("T")["precipitation"]
        .mean()
        .idxmax()
    )
    da_plot = da_clip.sel(T=T)
    fig, ax = plt.subplots(figsize=(8, 8))
    adm0.boundary.plot(ax=ax, color="k", linewidth=0.5)
    ax.axis("off")
    da_plot.plot(ax=ax, vmin=0, vmax=50, cmap=cmap)
    ax.set_title(f"Daily total rainfall on {T.date()}")
    plt.show()
```

```python

```
