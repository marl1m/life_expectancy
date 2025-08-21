"""Getting all regions"""

import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).parents[1]
PACKAGE_DIR = PROJECT_DIR / "life_expectancy"
FIXTURES_DIR = Path(__file__).parent / "fixtures"
OUTPUT_DIR = PACKAGE_DIR / "data"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

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

    data_cleaned = data_melted[
        (~data_melted['value'].isna()) 
        # &
        # (data_melted['region'] == country)
    ]

    data_cleaned.reset_index(drop=True, inplace=True)

    return data_cleaned

clean_data(
    pd.read_csv(
        str(OUTPUT_DIR / "eu_life_expectancy_raw.tsv")))
