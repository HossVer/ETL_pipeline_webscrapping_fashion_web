## =====================================================
## ================== Import Libraries =================
## =====================================================

import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

## =====================================================
## ==================== Functions ======================
## =====================================================
def load_to_csv(data_frame, filepath='products.csv'):
    data_frame.to_csv(filepath, index=False)
    print(f"✅ Data berhasil disimpan ke {filepath}") 

SERVICE_ACCOUNT_FILE = 'utils/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_gsheet_service():
    """Mengembalikan objek layanan Google Sheets API."""
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def upload_dataframe_to_sheet(dataframe, spreadsheet_id, sheet_range):
    """Mengunggah DataFrame ke Google Sheets"""
    try:
        """
       Google Sheets API butuh data dalam bentuk List[List[str]], 
       jadi kita harus mengonversi DataFrame seperti ini:
            values = dataframe.values.tolist()"""  
          
        sheet = get_gsheet_service()
        values = dataframe.values.tolist()

        body = {
            'values': values
        }

        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"✅ Berhasil mengupload {result.get('updatedRows')} baris ke Google Sheet. \n link: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat upload: {e}")
