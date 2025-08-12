""" Data cleaning utilities for life expectancy project. """

import argparse
import pandas as pd
from . import OUTPUT_DIR
from life_expectancy.constants import DATA_PATH, DATA_FOLDER, OUTPUT_PATH

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


def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Save DataFrame to CSV."""
    df.to_csv(output_path, index=False)

def main(country: str) -> None:
    """Main function calling the cleaning functions."""
    df = load_data(DATA_PATH)
    cleaned_df = clean_data(df, country)
    output_path = OUTPUT_PATH.format(country=country.lower())
    save_data(cleaned_df, output_path)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")
    parser.add_argument(
        "--country",
        type=str,
        default="PT",
        help="ISO country code to filter on (default: PT)"
    )

    args = parser.parse_args()
    main(args.country.upper())
