""" Data cleaning utilities for life expectancy project. """

import argparse
import pandas as pd
from pathlib import Path

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

'''
def main(country = "PT") -> None:
    """Main function calling the cleaning functions."""
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")

    parser.add_argument(
        "--country",
        type=str,
        default="PT",
        help="ISO country code to filter on (default: PT)"
    )

    parser.add_argument(
        "--raw-data-path",
        type=str,
        default= str(OUTPUT_DIR / "eu_life_expectancy_raw.tsv"),
        help="Path to the raw data file"
    )
    
    parser.add_argument(
        "--data-path",
        type=Path,
        default=OUTPUT_DIR,
        help="Path to the data folder"
    )

    args = parser.parse_args()
    df = load_data(args.raw_data_path)
    df_clean = clean_data(df, args.country)
    save_data(df_clean, args.data_path / f"{args.country}_life_expectancy.csv")
'''

def run_funcs(country, raw_data_path, data_path):
    
    df = load_data(raw_data_path)
    df_clean = clean_data(df, country)
    save_data(df_clean, data_path / f"{country}_life_expectancy.csv")

def main():
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")
    
    parser.add_argument("--country", type=str, default="PT")
    parser.add_argument("--raw-data-path", type=str, default=str(OUTPUT_DIR / "eu_life_expectancy_raw.tsv"))
    parser.add_argument("--data-path", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    
    run_funcs(args.country, args.raw_data_path, args.data_path)



if __name__ == "__main__":  # pragma: no cover
    main()
