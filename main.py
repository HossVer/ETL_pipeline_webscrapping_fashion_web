## =====================================================
## ================== Import Libraries =================
## =====================================================

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

from utils.extract import scrape_all_pages
from utils.transform import data_transforming, transform_to_DataFrame
from utils.load import load_to_csv, upload_dataframe_to_sheet

## =====================================================
## ================== Main Programs ====================
## =====================================================

SPREADSHEET_ID = "1HtUgHxlhZSxWdgfUffGewvj-FX_Ir1ipyv1i9CI2Evk"  # ID spreadsheet kamu
RANGE_NAME = 'Sheet1!A2'

def main():
    """
    Fungsi utama: scraping, transformasi, dan upload data ke CSV + Google Sheets
    """
    BASE_URL = 'https://fashion-studio.dicoding.dev/'
    fashion_data = []

    try:
        print("🔄 Mulai proses scraping...")
        fashion_data = scrape_all_pages(BASE_URL)
    except Exception as e:
        print(f"❌ Gagal scraping data: {e}")
        return

    if fashion_data:
        try:
            print("🔄 Transformasi data...")
            fashion_data = transform_to_DataFrame(fashion_data)
            fashion_data = data_transforming(fashion_data, 16000)
        except Exception as e:
            print(f"❌ Gagal saat transformasi data: {e}")
            return

        try:
            print("💾 Menyimpan ke file CSV...")
            load_to_csv(fashion_data)
        except Exception as e:
            print(f"❌ Gagal menyimpan ke CSV: {e}")

        try:
            print("📤 Upload ke Google Sheets...")
            upload_dataframe_to_sheet(fashion_data, SPREADSHEET_ID, RANGE_NAME)
        except Exception as e:
            print(f"❌ Gagal upload ke Google Sheets: {e}")
    else:
        print("❌ Tidak ada data yang berhasil di-scrape.")

if __name__ == '__main__':
    main()
