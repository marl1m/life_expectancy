""" Data cleaning utilities for life expectancy project. """

import argparse
import pandas as pd

DATA_PATH = "./life_expectancy/data/eu_life_expectancy_raw.tsv"
OUTPUT_DIR = "./life_expectancy/data/{country}_life_expectancy.csv"

def clean_data(path, country = 'PT'):

    """
    Loads and cleans a TSV file containing life expectancy data.

    Steps:
    1. Reads a tab-separated file from the given path.
    2. Splits the first column into four columns: 'unit', 'sex', 'age', and 'geo'.
    3. Converts wide-format year columns into a long-format 'year'-'value' structure.
    4. Renames 'geo' to 'region'.
    5. Converts 'year' to int and 'value' to float, coercing invalid entries to NaN.
    6. Filters rows to keep only valid numerical values and data for Portugal ('PT').
    7. Drops the first column, resets the index, and exports the result to CSV.
    
    The cleaned CSV is saved to: './data/pt_life_expectancy.csv'

    Args:
        path (str): Path to the TSV file to be processed.

    Returns:
        pandas.DataFrame: Cleaned and filtered DF containing life expectancy data for Portugal.
        
    """

    # i
    df = pd.read_csv(path, sep="\t")

    # ii
    df[['unit', 'sex', 'age', 'geo']] = df.iloc[:, 0].str.split(',', expand=True)

    df = df.drop(columns=df.columns[0])

    df_melted = pd.melt(
                    df,
                    id_vars=['unit', 'sex', 'age', 'geo'],
                    var_name='year',
                    value_name='value'
    )

    df_melted.rename(columns={"geo": "region"}, inplace=True)

    # iii to v
    df_melted.year.astype(int)
    # df_melted['value'] = pd.to_numeric(df_melted['value'], errors='coerce')


    df_melted = df_melted[df_melted['value'] != ': ']
    df_melted['value'] = pd.to_numeric(
                            df_melted['value'].str.replace(
                                r'[^0-9.]', '', regex=True), errors='coerce')

    data = df_melted[
        (~df_melted['value'].isna()) &
        (df_melted['region'] == country)
    ]

    # vi
    data.reset_index(drop=True, inplace=True)

    output_path = OUTPUT_DIR.format(country=country.lower())
    data.to_csv(output_path, index=False)

    return data

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")
    parser.add_argument(
        "--country",
        type=str,
        default="PT",
        help="ISO country code to filter on (default: PT)"
    )

    args = parser.parse_args()
    clean_data(DATA_PATH, country=args.country.upper())
