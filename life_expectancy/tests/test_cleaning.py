"""Tests for the cleaning module"""

import sys
import pandas as pd
from pandas.errors import EmptyDataError
import pytest
from pathlib import Path
from life_expectancy import cleaning
from . import OUTPUT_DIR, FIXTURES_DIR

def test_clean_data():
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

def test_main(monkeypatch, tmp_path):
    """Test that `cleaning.main` runs without errors
    using simulated command-line arguments."""

    input_file = OUTPUT_DIR / "eu_life_expectancy_raw.tsv"

    monkeypatch.setattr(sys, "argv", [
        "prog",
        "--country", "PT",
        "--raw-data-path", str(input_file),
        "--data-path", str(tmp_path)
    ])
    monkeypatch.setattr(cleaning, "OUTPUT_DIR", tmp_path)

    cleaning.main()

# --------------------------
# Parameterized tests for valid files
# --------------------------
@pytest.mark.parametrize("suffix, sep", [
    (".csv", ","),   # comma separated file
    (".tsv", "\t")   # tab separated file
])

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })

def test_load_text_files(tmp_path, suffix, sep, sample_data):

    # Create temporary file
    file_path = tmp_path / f"test{suffix}"
    sample_data.to_csv(file_path, sep=sep, index=False)
    
    # Load and compare
    df = cleaning.load_data(file_path, sep=sep)
    pd.testing.assert_frame_equal(df, sample_data)

# --------------------------
# Error / edge case tests
# --------------------------
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
