import sys
import os
import pytest
import pandas as pd

# Tambahkan direktori root agar modul utils bisa diimpor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import (
    transform_to_DataFrame,
    data_transforming,
    dataframe_value_to_list
)

def test_transform_to_DataFrame():
    data = [
        {"title": "Shirt", "price": "$10", "rating": "4.5", "colors": "3", "size": "M", "gender": "Unisex"}
    ]
    df = transform_to_DataFrame(data)
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, 'title'] == 'Shirt'

def test_data_transforming_success():
    data = [
        {"title": "Jacket", "price": "$20", "rating": "4.0", "colors": "2", "size": "L", "gender": "Male"}
    ]
    df = transform_to_DataFrame(data)
    transformed = data_transforming(df)

    assert isinstance(transformed, pd.DataFrame)
    assert transformed['price'].iloc[0] == 320000.0  # $20 * 16000
    assert transformed['rating'].iloc[0] == 4.0
    assert transformed['colors'].iloc[0] == 2
    assert transformed['title'].dtype == object

def test_data_transforming_invalid_input():
    not_df = [{"title": "Shoes"}]
    result = data_transforming(not_df)
    assert result is None

def test_data_transforming_invalid_rating():
    data = [
        {"title": "Item X", "price": "$5", "rating": "Invalid Rating", "colors": "1", "size": "S", "gender": "Female"}
    ]
    df = transform_to_DataFrame(data)
    result = data_transforming(df)
    assert result.empty

def test_dataframe_value_to_list():
    df = pd.DataFrame([
        {"title": "Test", "price": 160000.0, "rating": 4.5, "colors": 2, "size": "M", "gender": "Unisex"}
    ])
    result = dataframe_value_to_list(df)
    assert isinstance(result, list)
    assert result[0][0] == "Test"

def test_dataframe_value_to_list_invalid_input():
    not_df = "bukan dataframe"
    result = dataframe_value_to_list(not_df)
    assert result == []

