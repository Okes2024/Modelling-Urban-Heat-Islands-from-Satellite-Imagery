Modelling Urban Heat Islands from Satellite Imagery (Synthetic Data)

This project simulates and models Urban Heat Islands (UHI) using synthetic, satellite-like datasets. The synthetic data mimics reflectance bands, spectral indices (NDVI, NDBI, NDWI), albedo, urban density, vegetation, and elevation, with a generated Land Surface Temperature (LST) field that exhibits UHI effects.

Features

Generate synthetic satellite imagery with >200 data points (default: 1600 points on a 40×40 grid).

Includes spectral bands (Blue, Green, Red, NIR, SWIR, TIRBT) and vegetation/urban indices.

Automatically computes NDVI, NDBI, NDWI, albedo, and simulated LST.

Exports datasets in both Excel (.xlsx) and CSV (.csv) formats.

Fully configurable grid size and random seed.

Installation

Clone the repository and install dependencies:

git clone https://github.com/yourusername/Modelling-Urban-Heat-Islands-from-Satellite-Imagery.git
cd Modelling-Urban-Heat-Islands-from-Satellite-Imagery
pip install -r requirements.txt


Dependencies:

Python 3.8+

NumPy

Pandas

OpenPyXL (for Excel export)

Usage

Run the dataset generator script:

python generate_uhi_synthetic_dataset.py --rows 40 --cols 40 --seed 42 --out outputs


Arguments:

--rows: Number of grid rows (default: 40)

--cols: Number of grid columns (default: 40)

--seed: Random seed for reproducibility (default: 42)

--out: Output folder for dataset files (default: outputs)

Example Output

outputs/synthetic_uhi_dataset.xlsx

outputs/synthetic_uhi_dataset.csv

Each dataset contains:

Spatial coordinates (x, y)

Environmental features (elevation, urban_density, vegetation)

Spectral bands (BLUE, GREEN, RED, NIR, SWIR, TIRBT)

Indices (NDVI, NDBI, NDWI, albedo)

Target variable (LST, °C)

Applications

Benchmarking machine learning models for environmental modeling.

Testing geospatial workflows without needing real satellite data.

Exploring UHI effects in controlled synthetic scenarios.

License

MIT License. See LICENSE for details.

Author Name: Okes Imoni
Github: https://github.com/Okes2024
