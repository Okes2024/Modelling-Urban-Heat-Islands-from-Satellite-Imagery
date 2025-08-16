#!/usr/bin/env python3
"""
generate_uhi_synthetic_dataset.py

Creates a synthetic "satellite-like" dataset for modelling Urban Heat Islands (UHI)
and saves it to Excel and CSV. Defaults to a 40x40 grid (> 200 points).

Usage:
    python generate_uhi_synthetic_dataset.py --rows 40 --cols 40 --seed 42 --out outputs

Outputs:
    - outputs/synthetic_uhi_dataset.xlsx
    - outputs/synthetic_uhi_dataset.csv
"""

import os
import math
import argparse
import numpy as np
import pandas as pd

def generate_synthetic_satellite_data(rows: int = 40, cols: int = 40, seed: int = 42):
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, cols)
    y = np.linspace(0, 1, rows)
    xx, yy = np.meshgrid(x, y)

    # --- Topography & urban/vegetation structure ---
    elevation = 0.2 * yy + 0.1 * np.sin(2 * np.pi * xx) * np.cos(2 * np.pi * yy)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    # Two urban centers (radial basis functions)
    def rbf(cx, cy, scale):
        return np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (scale ** 2))))

    urban_density = 0.9 * rbf(0.45, 0.55, 0.12) + 0.7 * rbf(0.75, 0.3, 0.1)
    urban_density += 0.05 * rng.normal(size=urban_density.shape)
    urban_density = np.clip((urban_density - urban_density.min()) / (urban_density.max() - urban_density.min()), 0, 1)

    # Vegetation inversely related to urban + small topo influence
    vegetation = np.clip(1 - 0.8 * urban_density + 0.1 * (1 - elevation) + 0.05 * rng.normal(size=urban_density.shape), 0, 1)

    # --- "Reflectance" bands (0..1) ---
    BLUE  = np.clip(0.2 + 0.2 * 0 + 0.1 * rng.normal(size=(rows, cols)), 0, 1)
    GREEN = np.clip(0.25 + 0.5 * vegetation - 0.1 * urban_density + 0.1 * rng.normal(size=(rows, cols)), 0, 1)
    RED   = np.clip(0.3 + 0.25 * urban_density - 0.3 * vegetation + 0.1 * rng.normal(size=(rows, cols)), 0, 1)
    NIR   = np.clip(0.35 + 0.5 * vegetation - 0.15 * urban_density + 0.1 * rng.normal(size=(rows, cols)), 0, 1)
    SWIR  = np.clip(0.4 + 0.4 * urban_density - 0.2 * vegetation + 0.1 * rng.normal(size=(rows, cols)), 0, 1)
    TIRBT = np.clip(0.6 + 0.25 * urban_density - 0.1 * vegetation + 0.05 * rng.normal(size=(rows, cols)), 0, 1)

    eps = 1e-6
    NDVI = (NIR - RED) / (NIR + RED + eps)
    NDBI = (SWIR - NIR) / (SWIR + NIR + eps)
    NDWI = (GREEN - NIR) / (GREEN + NIR + eps)

    # Simple broadband albedo proxy
    albedo = np.clip(0.1*BLUE + 0.3*GREEN + 0.3*RED + 0.2*NIR + 0.1*SWIR, 0, 1)

    # --- Land Surface Temperature (synthetic °C) ---
    # Add a seasonal factor for variety
    doy = int(rng.integers(1, 366))
    seasonal = 0.5 + 0.4 * math.sin(2 * math.pi * (doy / 365.0 - 0.25))

    base_lst = 26 + 10 * seasonal - 3.0 * elevation
    LST = (
        base_lst
        + 8.0 * urban_density
        + 5.0 * NDBI
        - 7.0 * NDVI
        - 2.5 * albedo
        + 1.5 * TIRBT
        + rng.normal(0, 0.8, size=(rows, cols))
    )

    df = pd.DataFrame({
        "x": xx.ravel(),
        "y": yy.ravel(),
        "elevation": elevation.ravel(),
        "urban_density": urban_density.ravel(),
        "vegetation": vegetation.ravel(),
        "BLUE": BLUE.ravel(),
        "GREEN": GREEN.ravel(),
        "RED": RED.ravel(),
        "NIR": NIR.ravel(),
        "SWIR": SWIR.ravel(),
        "TIRBT": TIRBT.ravel(),
        "NDVI": NDVI.ravel(),
        "NDBI": NDBI.ravel(),
        "NDWI": NDWI.ravel(),
        "albedo": albedo.ravel(),
        "LST": LST.ravel(),
    })
    meta = {"rows": rows, "cols": cols, "doy": doy, "n_samples": int(rows*cols)}
    return df, meta

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic UHI dataset and save to Excel/CSV.")
    parser.add_argument("--rows", type=int, default=40, help="Grid rows (> 10).")
    parser.add_argument("--cols", type=int, default=40, help="Grid cols (> 10).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--out", type=str, default="outputs", help="Output folder.")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    df, meta = generate_synthetic_satellite_data(args.rows, args.cols, args.seed)

    # Ensure > 200 samples
    if meta["n_samples"] <= 200:
        raise ValueError(f"Dataset too small: {meta['n_samples']} samples. Increase --rows/--cols.")

    xlsx_path = os.path.join(args.out, "synthetic_uhi_dataset.xlsx")
    csv_path  = os.path.join(args.out, "synthetic_uhi_dataset.csv")

    # Save
    df.to_excel(xlsx_path, index=False)
    df.to_csv(csv_path, index=False)

    print(f"Saved Excel: {xlsx_path}")
    print(f"Saved CSV  : {csv_path}")
    print(f"Meta       : {meta}")

if __name__ == "__main__":
    main()
