"""Constants for life expectancy project."""

# Base data directory
DATA_FOLDER = "/Users/marlim/dd_lp_foundations_assignments/assignments/life_expectancy/data"
#"./life_expectancy/data/eu_life_expectancy_raw.tsv"

# Input file path
DATA_PATH = DATA_FOLDER / "eu_life_expectancy_raw.tsv"

# Output file pattern (format with .format(country=...))
OUTPUT_PATH = DATA_FOLDER / "{country}_life_expectancy.csv"
#"./life_expectancy/data/{country}_life_expectancy.csv"
