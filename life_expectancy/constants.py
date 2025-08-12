"""Constants for life expectancy project."""

from pathlib import Path

# Base data directory
BASE_DIR = Path("/Users/marlim/dd_lp_foundations_assignments/assignments/life_expectancy/data")
#"./life_expectancy/data/eu_life_expectancy_raw.tsv"

# Input file path
DATA_PATH = BASE_DIR / "eu_life_expectancy_raw.tsv"

# Output file pattern (format with .format(country=...))
OUTPUT_PATH = BASE_DIR / "{country}_life_expectancy.csv"
#"./life_expectancy/data/{country}_life_expectancy.csv"
