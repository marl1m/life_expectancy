"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import *
from life_expectancy.constants import *

def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""

    save_data(
        clean_data(
            load_data(
                DATA_PATH),
            country='PT'), 
        OUTPUT_DIR)

    pt_life_expectancy_actual = pd.read_csv(
        "/Users/marlim/life_expectancy/life_expectancy/tests/fixtures/pt_life_expectancy_expected.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )

''' proper proper backbone of testing
def test_load_data(tmp_path):
    # Arrange
    sample_data = "col1\tcol2\n1\t2\n3\t4\n"
    sample_file = tmp_path / "sample.tsv"
    sample_file.write_text(sample_data)

    # Act
    df = load_data(sample_file)

    # Assert
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]
    assert df.shape == (2, 2)


def test_clean_data(pt_life_expectancy_raw, pt_life_expectancy_expected):
    # Act
    cleaned = clean_data(pt_life_expectancy_raw, "PT")

    # Assert
    pd.testing.assert_frame_equal(cleaned, pt_life_expectancy_expected)


def test_save_data(tmp_path):
    # Arrange
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    output_file = tmp_path / "test.csv"

    # Act
    save_data(df, output_file)

    # Assert
    assert output_file.exists()
    saved_df = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(saved_df, df)


def test_main(tmp_path, monkeypatch, pt_life_expectancy_raw, pt_life_expectancy_expected):
    # Arrange
    input_file = tmp_path / "input.tsv"
    pt_life_expectancy_raw.to_csv(input_file, sep="\t", index=False)

    output_template = str(tmp_path / "{country}_life_expectancy.csv")

    monkeypatch.setattr("your_module.DATA_PATH", input_file)
    monkeypatch.setattr("your_module.OUTPUT_DIR", output_template)

    # Act
    main("PT")

    # Assert
    output_file = tmp_path / "pt_life_expectancy.csv"
    assert output_file.exists()
    saved_df = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(saved_df, pt_life_expectancy_expected)

'''
