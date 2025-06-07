import argparse
import json
import os
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import Point

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

QUERY = """
[out:json][timeout:180];
area["name"="Noord-Holland"]["admin_level"="4"]->.searchArea;
(
  node["generator:source"="solar"](area.searchArea);
  way["generator:source"="solar"](area.searchArea);
  relation["generator:source"="solar"](area.searchArea);
);
out center;
"""

def fetch_overpass() -> gpd.GeoDataFrame:
    """Query Overpass API and return GeoDataFrame of solar features."""
    response = requests.post(OVERPASS_URL, data={"data": QUERY})
    response.raise_for_status()
    data = response.json()

    elements = data.get("elements", [])
    records = []
    for el in elements:
        if "lon" in el and "lat" in el:
            lon, lat = el["lon"], el["lat"]
        elif "center" in el:
            lon, lat = el["center"]["lon"], el["center"]["lat"]
        else:
            continue
        records.append({
            "osm_id": el.get("id"),
            "lon": lon,
            "lat": lat
        })

    gdf = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy([r["lon"] for r in records], [r["lat"] for r in records]), crs="EPSG:4326")
    return gdf

def load_bag_subset(bag_path: Path, bounds) -> gpd.GeoDataFrame:
    """Load subset of BAG data within given bounds."""
    minx, miny, maxx, maxy = bounds
    return gpd.read_file(bag_path, bbox=(minx, miny, maxx, maxy))

def spatial_join(solar_gdf: gpd.GeoDataFrame, bag_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    bag_gdf = bag_gdf.to_crs("EPSG:4326")
    joined = gpd.sjoin(solar_gdf, bag_gdf, how="inner", predicate="within")
    return joined

def main():
    parser = argparse.ArgumentParser(description="Fetch solar panel locations and join with BAG data")
    parser.add_argument("--bag_path", required=True, help="Path to bag.gpkg")
    parser.add_argument("--output", default="output.csv", help="Output CSV path")
    args = parser.parse_args()

    solar_gdf = fetch_overpass()
    bag_gdf = load_bag_subset(Path(args.bag_path), solar_gdf.total_bounds)
    joined = spatial_join(solar_gdf, bag_gdf)

    cols = {
        "objectnummer": "Objectnummer",
        "straatnaam": "Street",
        "huisnummer": "Housenumber",
        "postcode": "Postal code",
        "woonplaats": "City",
        "gebruiksdoel": "Gebruiksdoel",
        "functie": "Functie",
    }
    out_df = joined[list(cols.keys()) + ["lon", "lat"]].rename(columns=cols)
    out_df["Country"] = "Netherlands"
    out_df["Company name"] = ""
    out_df["Google Maps URL"] = out_df.apply(lambda row: f"https://maps.google.com/?q={row['lat']},{row['lon']}", axis=1)
    out_df = out_df[[
        "Objectnummer", "Street", "Housenumber", "Postal code", "City", "Country",
        "Gebruiksdoel", "Functie", "Company name", "Google Maps URL", "lon", "lat"
    ]]

    out_df.to_csv(args.output, index=False)
    print(f"Saved {len(out_df)} records to {args.output}")

if __name__ == "__main__":
    main()
