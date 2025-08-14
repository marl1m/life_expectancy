""" Data cleaning utilities for life expectancy project. """

import argparse
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).parents[1]
PACKAGE_DIR = PROJECT_DIR / "life_expectancy"
FIXTURES_DIR = Path(__file__).parent / "fixtures"
OUTPUT_DIR = PACKAGE_DIR / "data"

def load_data(path: str) -> pd.DataFrame:
    """Load data from CSV file."""
    data = pd.read_csv(path, sep="\t")
    return data


def clean_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Clean data and filter by country."""

    df[['unit', 'sex', 'age', 'geo']] = df.iloc[:, 0].str.split(',', expand=True)

    df = df.drop(columns=df.columns[0])

    df_melted = pd.melt(
                    df,
                    id_vars=['unit', 'sex', 'age', 'geo'],
                    var_name='year',
                    value_name='value'
    )

    df_melted.rename(columns={"geo": "region"}, inplace=True)

    df_melted.year = df_melted.year.astype(int)

    df_melted = df_melted[df_melted['value'] != ': ']
    df_melted['value'] = pd.to_numeric(
                            df_melted['value'].str.replace(
                                r'[^0-9.]', '', regex=True), errors='coerce')

    data = df_melted[
        (~df_melted['value'].isna()) &
        (df_melted['region'] == country)
    ]

    data.reset_index(drop=True, inplace=True)

    if "country" in df.columns:
        data = data[data["country"] == country]

    return data


def save_data(df: pd.DataFrame, output_path) -> None:
    """Save DataFrame to CSV."""
    df.to_csv(output_path, index=False)


def run_cleaning(country, raw_data_path, data_path):
    """Calling of all cleaning functions to insert into main."""
    df = load_data(raw_data_path)
    df_clean = clean_data(df, country)
    save_data(df_clean, data_path / f"{country}_life_expectancy.csv")

def main():
    """Main script function where all functions and args are called."""
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")

    parser.add_argument("--country",
                        type=str,
                        default="PT")
    parser.add_argument("--raw-data-path",
                        type=str,
                        default=str(OUTPUT_DIR / "eu_life_expectancy_raw.tsv"))
    parser.add_argument("--data-path",
                        type=Path,
                        default=OUTPUT_DIR)
    args = parser.parse_args()

    run_cleaning(args.country, args.raw_data_path, args.data_path)

if __name__ == "__main__":  # pragma: no cover
    main()
