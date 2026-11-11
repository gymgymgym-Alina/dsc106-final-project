# One number, thirty answers

DSC 106 final project. An explorable explanation about why a global average
temperature target says very little about any particular city.

Live page: https://gymgymgym-Alina.github.io/dsc106-final-project/

Team: TBD

## Dataset

CMIP6 monthly surface air temperature (`tas`, table `Amon`) from the Pangeo
CMIP6 archive on Google Cloud, sampled at the nearest grid point to each of 30
cities and averaged to annual means.

- 30 cities, 24 countries
- 4 models: CanESM5, GFDL-ESM4, IPSL-CM6A-LR, MRI-ESM2-0
- 3 experiments: historical (1950 to 2014), ssp126 and ssp585 (2015 to 2100)
- `warming_c` is each city's anomaly against its own 1981 to 2010 mean

## Structure

- `index.html` page structure and copy
- `main.js` all D3 visualization code
- `style.css` styles and the light and dark color tokens
- `data/city_temps.csv` the data the page loads
- `data/world_countries.json` GeoJSON basemap
- `notebooks/check_daily.py` tests whether daily `tasmax` is reachable, for the
  threshold-days idea that is still a stretch goal

## Local preview

    python3 -m http.server 8000

Then open http://localhost:8000 . Opening `index.html` directly will not work,
because the browser blocks the data fetch over `file://`.
