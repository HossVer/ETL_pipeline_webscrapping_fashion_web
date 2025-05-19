## =====================================================
## ================== Import Libraries =================
## =====================================================

import pandas as pd
from datetime import datetime

## =====================================================
## ===================== Functions =====================
## =====================================================
"""
    Transformation function dan mengubah data menjadi sesuai keinginan
        - Ubah data mnejadi dataframe
        - Konversi data price menjadi rupiah dengan kurs Rp.16.000
        - Tipe data sesuai ketentuan 
                    1. Title Object
                    2. Price Float
                    3. Rating Float
                    4. Colors int
                    5. Size object
                    6. Gender Object
                    7. Timestamp (optional)
"""

def transform_to_DataFrame(data_array):
    """Mengubah data array menjadi pandas dataframe"""
    dataframe = pd.DataFrame(data_array)
    return dataframe

def data_transforming(dataframe, exchange_rate=16000):
    if isinstance(dataframe, pd.DataFrame):
        try:
            # Normalisasi nama kolom
            dataframe.columns = dataframe.columns.str.strip().str.lower()

            # Tangani rating tidak valid
            dataframe = dataframe[dataframe['rating'] != 'Invalid Rating'].copy()

            # Konversi price
            dataframe['price'] = dataframe['price'].astype(str).str.replace('$', '', regex=False)
            dataframe['price'] = pd.to_numeric(dataframe['price'], errors='coerce') * exchange_rate

            # Drop duplikat & NaN
            dataframe = dataframe.drop_duplicates().dropna()

            # Validasi & ubah tipe data
            if 'title' in dataframe.columns:
                dataframe['title'] = dataframe['title'].astype(object)
            if 'price' in dataframe.columns:
                dataframe['price'] = dataframe['price'].astype(float)
            if 'rating' in dataframe.columns:
                dataframe['rating'] = dataframe['rating'].astype(float)
            if 'colors' in dataframe.columns:
                dataframe['colors'] = dataframe['colors'].astype(int)
            if 'size' in dataframe.columns:
                dataframe['size'] = dataframe['size'].astype(object)
            if 'gender' in dataframe.columns:
                dataframe['gender'] = dataframe['gender'].astype(object)

            print("✅ Berhasil melakukan transformasi data")
            return dataframe

        except Exception as e:
            print(f"❌ Terjadi kesalahan saat transform: {e}")
            return None
    else:
        print("❌ input bukan dataframe pandas!")
        return None

def dataframe_value_to_list(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        return dataframe.values.tolist()
    else:
        print("❌ Input bukan DataFrame.")
        return []
