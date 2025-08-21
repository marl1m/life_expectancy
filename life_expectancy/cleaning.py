""" Data cleaning utilities for life expectancy project. """

import argparse
from pathlib import Path
import pandas as pd
from pandas.errors import EmptyDataError

PROJECT_DIR = Path(__file__).parents[1]
PACKAGE_DIR = PROJECT_DIR / "life_expectancy"
FIXTURES_DIR = Path(__file__).parent / "tests/fixtures"
OUTPUT_DIR = PACKAGE_DIR / "data"

def load_data(path: str | Path, sep: str = "\t") -> pd.DataFrame:
    """
    Load a text, CSV, or Excel data file into a DataFrame.

    Parameters
    ----------
    path : str or Path
        File path to the raw data file (.txt, .csv, .xlsx, .tsv).
    sep : str, optional
        Column separator used for .txt, .csv, .tsv files (default is tab).

    Returns
    -------
    pd.DataFrame
        DataFrame containing the loaded data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the path is not a file or has an unsupported extension.
    EmptyDataError
        If the file exists but contains no data.
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    if path.suffix.lower() not in {".txt", ".csv", ".xlsx", ".tsv"}:
        raise ValueError(f"Unsupported file extension: {path.suffix} "
                         f"(allowed: .txt, .csv, .xlsx, .tsv)")

    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path)
    else:
        return pd.read_csv(path, sep=sep)

# def clean_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean a raw Eurostat-style dataset, keeping only valid rows for a given country.

    The input DataFrame is expected to have its first column containing comma-separated 
    metadata fields (unit, sex, age, geo), followed by year columns with string values. 
    This function:
    - Splits the first column into explicit metadata columns.
    - Converts the data from wide to long format.
    - Renames 'geo' to 'region' and casts 'year' to int.
    - Removes missing or placeholder values (': ') and coerces numeric types.
    - Filters rows by the specified country/region code.
    - Resets the index for the cleaned dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Raw input data with the first column containing comma-separated metadata 
        and subsequent columns containing year values.
    country : str
        ISO or region code used to filter the cleaned dataset.

    Returns
    -------
    pd.DataFrame
        A cleaned, long-format DataFrame containing only rows corresponding 
        to the given country, with numeric 'value' column.
    """

    data = df.copy()

    data[['unit', 'sex', 'age', 'geo']] = data.iloc[:, 0].str.split(',', expand=True)

    data = data.drop(columns=[r'unit,sex,age,geo\time'])

    data_melted = pd.melt(
                    data,
                    id_vars=['unit', 'sex', 'age', 'geo'],
                    var_name='year',
                    value_name='value'
    )

    data_melted.rename(columns={"geo": "region"}, inplace=True)

    data_melted['year'] = data_melted['year'].astype(int)

    data_melted = data_melted[data_melted['value'] != ': ']
    
    data_melted['value'] = pd.to_numeric(
                            data_melted['value'].str.replace(
                                r'[^0-9.]', '', regex=True), errors='coerce')

    # data_cleaned = data_melted[
    #     (~data_melted['value'].isna()) &
    #     (data_melted['region'] == country)
    # ]
    
    data_cleaned = data_melted[
        (~data_melted['value'].isna())
    ]

    data_cleaned.reset_index(drop=True, inplace=True)

    return data_cleaned


def save_data(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    Saves a DataFrame into a CSV file, creating parent directories if needed.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be saved.
    output_path : str or pathlib.Path
        Destination file path for the CSV. Parent directories are created 
        automatically if they don't exist.

    Returns
    -------
    None
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


# def run_cleaning(country: str, raw_data_path: str | Path, data_path: str | Path) -> None:
#     """
#     Loads the raw data, cleans it and filters it for a specific country, then saves it as CSV.

#     This function acts as the high-level entry point for the cleaning workflow:
#     - Loads the raw dataset from the given path.
#     - Cleans and filters it using the specified country code.
#     - Writes the cleaned data to the target directory with a standardized filename.

#     Parameters
#     ----------
#     country : str
#         ISO or region code to filter data on.
#     raw_data_path : str or pathlib.Path
#         Path to the raw input data file.
#     data_path : str or pathlib.Path
#         Directory where the cleaned CSV will be stored.

#     Returns
#     -------
#     None
#     """
#     df = load_data(raw_data_path)
#     df_clean = clean_data(df, country)
#     save_data(df_clean, data_path / f"{country}_life_expectancy.csv")

def run_cleaning(raw_data_path: str|Path, data_path: str|Path) -> None:
    df = load_data(raw_data_path)
    df_clean = clean_data(df)
    save_data(df_clean, data_path / "eu_life_expectancy.csv")


def parse_args():
    """
    Command-line entry point for cleaning life expectancy data.

    Parses command-line arguments for country code, raw data path, and output path; 
    """
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")
    # parser.add_argument("--country", type=str, default="PT")
    # parser.add_argument("--raw-data-path", type=str, default=str(OUTPUT_DIR / "eu_life_expectancy_raw.tsv"))
    parser.add_argument("--raw-data-path", type=str, default=str(FIXTURES_DIR / "eu_life_expectancy_raw.tsv"))

    # parser.add_argument("--data-path", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--data-path", type=Path, default=FIXTURES_DIR)

    return parser.parse_args()

def main():
    """
    Runs the full cleaning workflow to produce a cleaned CSV file.
    """
    args = parse_args()
    # run_cleaning(args.country, args.raw_data_path, args.data_path)
    run_cleaning(args.raw_data_path, args.data_path)


if __name__ == "__main__":  # pragma: no cover
    main()
