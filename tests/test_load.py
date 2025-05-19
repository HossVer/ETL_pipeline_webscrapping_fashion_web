import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Tambahkan path ke folder utama
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import load_to_csv, upload_dataframe_to_sheet

@patch("utils.load.pd.DataFrame.to_csv")
def test_load_to_csv(mock_to_csv):
    df = pd.DataFrame({"name": ["Item 1", "Item 2"], "price": [10000, 15000]})
    load_to_csv(df, "mock_products.csv")
    mock_to_csv.assert_called_once_with("mock_products.csv", index=False)

@patch("utils.load.build")
@patch("utils.load.Credentials.from_service_account_file")
def test_upload_dataframe_to_sheet(mock_creds, mock_build):
    # Buat dataframe
    df = pd.DataFrame({"product": ["A", "B"], "price": [1000, 2000]})

    # Mock Google Sheets service
    mock_service = MagicMock()
    mock_values = MagicMock()
    mock_update = MagicMock()
    mock_execute = MagicMock(return_value={"updatedRows": 2})

    mock_update.execute = mock_execute
    mock_values.update = MagicMock(return_value=mock_update)
    mock_service.values = MagicMock(return_value=mock_values)
    mock_build.return_value.spreadsheets.return_value = mock_service

    # Jalankan fungsi
    upload_dataframe_to_sheet(df, "dummy_spreadsheet_id", "Sheet1!A1")

    # Verifikasi pemanggilan update
    mock_service.values().update.assert_called_once_with(
        spreadsheetId="dummy_spreadsheet_id",
        range="Sheet1!A1",
        valueInputOption="RAW",
        body={"values": df.values.tolist()}
    )
