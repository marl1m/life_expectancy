"""Tests for the cleaning module"""

import sys
import pandas as pd
from pandas.errors import EmptyDataError
import pytest
from pathlib import Path
from life_expectancy import cleaning
from . import OUTPUT_DIR, FIXTURES_DIR

'''def test_clean_data():
    """Run the `clean_data` function and compare the output to the expected output"""

    cleaning.save_data(
        (cleaning.clean_data(
            (cleaning.load_data(
                str(OUTPUT_DIR / "eu_life_expectancy_raw.tsv"))),
            country='PT')),
        OUTPUT_DIR / "pt_life_expectancy.csv")

    output_saved_data = OUTPUT_DIR / "pt_life_expectancy.csv"
    expected_output_data = FIXTURES_DIR / "pt_life_expectancy_expected.csv"

    assert output_saved_data.exists()
    assert expected_output_data.exists()

    pt_life_expectancy_actual = pd.read_csv(str(output_saved_data))
    pt_life_expectancy_expected = pd.read_csv(str(expected_output_data))

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
'''

# LOADING TESTS
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })

@pytest.mark.parametrize("suffix, sep", [
    (".csv", ","),   # comma separated file
    (".tsv", "\t")   # tab separated file
])

def test_load_data(tmp_path, suffix, sep, sample_data):

    # Create temporary file
    file_path = tmp_path / f"test{suffix}"  
    sample_data.to_csv(file_path, sep=sep, index=False)
    
    # Load and compare
    df = cleaning.load_data(file_path, sep=sep)
    pd.testing.assert_frame_equal(df, sample_data)


def test_file_not_found(tmp_path):
    file_path = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        cleaning.load_data(file_path)


def test_path_is_directory(tmp_path):
    with pytest.raises(ValueError):
        cleaning.load_data(tmp_path)  # directory, not file


def test_unsupported_extension(tmp_path):
    file_path = tmp_path / "test.invalid"
    file_path.touch()
    with pytest.raises(ValueError):
        cleaning.load_data(file_path)


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.touch()
    with pytest.raises(EmptyDataError):
        cleaning.load_data(file_path)


# CLEAN TESTS


import pandas as pd
import pytest

@pytest.fixture
def sample_raw():
    """Eurostat-style raw dataset for testing clean_data."""
    return pd.DataFrame({
        "unit,sex,age,geo\\time": [
            "YR,F,Y1,PT",
            "YR,F,Y1,ES",
            "YR,F,Y1,PT"
        ],
        "2021": [": ", "79.4", "80.0"],
        "2020": ["79.0", "78.5", ": "],
        "2019": ["80.0", ": ", "81.0"]
    })


def test_splitting_first_few_collumns():
    raw = sample_raw()
    cleaned = cleaning.clean_data(raw, country="PT")
    for col in ["unit", "sex", "age", "region"]:
        assert col in cleaned.columns


def test_year_columns_being_melted():
    raw = sample_raw()
    cleaned = cleaning.clean_data(raw, country="PT")
    assert "year" in cleaned.columns
    assert cleaned['year'].dtype == int
    pt_rows = raw[raw['unit,sex,age,geo\\time'].str.endswith("PT")]
    assert cleaned.shape[0] >= len(pt_rows)


def test_dtypes_and_removal_NAs():
    raw = sample_raw()
    cleaned = cleaning.clean_data(raw, country="PT")
    assert all(cleaned['value'].notna())
    assert pd.api.types.is_numeric_dtype(cleaned['value'])


def test_filtering_by_country_specified():
    raw = sample_raw()
    cleaned = cleaning.clean_data(raw, country="PT")
    assert all(cleaned['region'] == "PT")
    cleaned_empty = cleaning.clean_data(raw, country="XX")
    assert cleaned_empty.empty

# -------------------------------
# 5️⃣ Index reset
# -------------------------------
def test_index_reset():
    raw = sample_raw()
    cleaned = cleaning.clean_data(raw, country="PT")
    assert list(cleaned.index) == list(range(len(cleaned)))

# -------------------------------
# 6️⃣ Non-numeric character cleaning
# -------------------------------
def test_non_numeric_characters():
    raw = pd.DataFrame({
        "unit,sex,age,geo\\time": ["YR,F,Y1,PT"],
        "2021": [": "],
        "2020": ["12%"]
    })
    cleaned = cleaning.clean_data(raw, country="PT")
    assert cleaned['value'].tolist() == [12]

# -------------------------------
# 7️⃣ No NaNs after cleaning
# -------------------------------
def test_no_nans():
    raw = sample_raw()
    cleaned = cleaning.clean_data(raw, country="PT")
    assert not cleaned.isna().any().any()














# RUNNING TEST

def test_run_cleaning(monkeypatch, tmp_path):
    # Fake data to flow through the function
    fake_df = pd.DataFrame({"x": [1, 2]})
    cleaned_df = pd.DataFrame({"x": [42]})
    calls = {}

    # Patch dependencies
    monkeypatch.setattr(cleaning, "load_data", lambda path: (calls.update({"load": path}) or fake_df))
    monkeypatch.setattr(cleaning, "clean_data", lambda df, country: (calls.update({"clean": (df, country)}) or cleaned_df))
    monkeypatch.setattr(cleaning, "save_data", lambda df, path: calls.update({"save": (df, path)}))

    # Run
    cleaning.run_cleaning("PT", "raw.tsv", tmp_path)

    # Assertions
    assert calls["load"] == "raw.tsv"
    assert calls["clean"][0].equals(fake_df)
    assert calls["clean"][1] == "PT"
    saved_df, saved_path = calls["save"]
    assert saved_df.equals(cleaned_df)
    assert saved_path == tmp_path / "PT_life_expectancy.csv"

 
# ARGS TESTS
def test_parse_args_defaults(monkeypatch):
    # Only program name provided → should use defaults
    monkeypatch.setattr(sys, "argv", ["prog"])
    args = cleaning.parse_args()

    assert args.country == "PT"
    assert str(args.raw_data_path).endswith("eu_life_expectancy_raw.tsv")
    assert isinstance(args.data_path, Path)


def test_parse_args_custom(monkeypatch):
    monkeypatch.setattr(sys, "argv", [
        "prog",
        "--country", "ES",
        "--raw-data-path", "raw.tsv",
        "--data-path", "outdir"
    ])
    args = cleaning.parse_args()
    assert args.country == "ES"
    assert args.raw_data_path == "raw.tsv"
    assert args.data_path == Path("outdir")

# MAIN TEST
def test_main(monkeypatch):
    # Prepare fake args
    monkeypatch.setattr(sys, "argv", [
        "prog",
        "--country", "DE",
        "--raw-data-path", "input.tsv",
        "--data-path", "outdir"
    ])

    # Capture arguments passed to run_cleaning
    captured = {}
    monkeypatch.setattr(cleaning, "run_cleaning",
                        lambda country, raw, out: captured.update({
        "country": country, "raw": raw, "out": out
    }))

    cleaning.main()

    # Only assert that run_cleaning received the args from parse_args
    assert captured["country"] == "DE"
    assert captured["raw"] == "input.tsv"
    assert str(captured["out"]) == "outdir"
    
