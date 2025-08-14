"""Tests for the cleaning module"""

import shutil
import pandas as pd
import sys
from life_expectancy import cleaning
from pathlib import Path
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

    input_file = OUTPUT_DIR / "eu_life_expectancy_raw.tsv"

    monkeypatch.setattr(sys, "argv", [
        "prog",
        "--country", "PT",
        "--raw-data-path", str(input_file),
        "--data-path", str(tmp_path)
    ])
    monkeypatch.setattr(cleaning, "OUTPUT_DIR", tmp_path)

    cleaning.main()


''' proper backbone of testing
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