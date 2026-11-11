"""Decide whether daily tasmax is reachable in time. Run: python3 notebooks/check_daily.py"""
import time
import pandas as pd

MODELS = ["CanESM5", "GFDL-ESM4", "IPSL-CM6A-LR", "MRI-ESM2-0",
          "MPI-ESM1-2-LR", "NorESM2-LM"]
EXPERIMENTS = ["historical", "ssp126", "ssp585"]
CITY = (32.72, -117.16)

cat = pd.read_csv("https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv")

day = cat[(cat.table_id == "day") & (cat.variable_id == "tasmax")
          & (cat.member_id == "r1i1p1f1")
          & (cat.source_id.isin(MODELS))
          & (cat.experiment_id.isin(EXPERIMENTS))]

print("STEP 1: which model and scenario combinations exist")
if day.empty:
    print("  none. Option D is dead with these models.")
    raise SystemExit
table = day.pivot_table(index="source_id", columns="experiment_id",
                        values="zstore", aggfunc="count").fillna(0).astype(int)
print(table.to_string())

complete = [m for m in table.index if (table.loc[m] > 0).all()]
print("\n  models with all three:", complete or "NONE")
if not complete:
    print("  Option D needs a different model set or fewer scenarios.")
    raise SystemExit

print("\nSTEP 2: timing one model, one scenario, one city, ten years")
import gcsfs
import xarray as xr

model = complete[0]
zstore = day[(day.source_id == model) & (day.experiment_id == "ssp585")].zstore.iloc[-1]
fs = gcsfs.GCSFileSystem(token="anon")

t0 = time.time()
ds = xr.open_zarr(fs.get_mapper(zstore), consolidated=True)
print(f"  opened {model} in {time.time() - t0:.1f}s")
print("  chunks:", {k: v for k, v in ds.tasmax.chunksizes.items()})

lat, lon = CITY
if float(ds.lon.min()) >= 0:
    lon = lon % 360

t0 = time.time()
pt = (ds.tasmax.sel(lat=lat, lon=lon, method="nearest")
        .sel(time=slice("2090", "2099")).load() - 273.15)
dt = time.time() - t0
print(f"  pulled {pt.size} daily values in {dt:.1f}s")
print(f"  days above 35C per year: {(pt > 35).groupby('time.year').sum().values}")

full = dt * (86 / 10) * len(complete) * 2 * 30 / 60
print(f"\nSTEP 3: rough estimate for 30 cities, {len(complete)} models, 2 scenarios, 1950 to 2100")
print(f"  about {full:.0f} minutes if it scales linearly")
print("  under 60: do it. 60 to 180: one model only. over 180: drop Option D.")
