## =====================================================
## ================== Import Libraries =================
## =====================================================
import time
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

from datetime import datetime

## =====================================================
## ==================== Functions ======================
## =====================================================

# Headers digunakan untuk meniru perilaku request browser dan terhindar dari praduga bot
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """     
        Mengambil konten HTML dari URL yang diberikan untuk 
        diekstrak informasi dari tag headernya  
    """
    session = requests.Session()
    try:   
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # Menangani error jika request gagal
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat melakukan request terhadap {url}: {e}")
        return None
    
def extract_fashion_data(article):
    """
        Mengekstrak informasi katalog berdasarkan umpan artikel yang didapat
        dari hasil requesting html fetching_content()
        data yang diambil:
            - Title
            - Price
            - Colors
            - Size
            - Gender
            - Rating
    """
    datas = {
        "title": None,
        "price": None,
        "colors": None,
        "size": None,
        "gender": None,
        "rating": None,
    }

    # Title
    title = article.find('h3', class_="product-title")
    if title:
        datas["title"] = title.get_text(strip=True)

    # Price
    price_element = article.find('div', class_="price-container")
    if price_element:
        price_tag = price_element.find('span', class_="price")
        if price_tag:
            datas['price'] = price_tag.get_text(strip=True)

    # Colors, Size, Gender, Rating
    for p in article.find_all('p', style="font-size: 14px; color: #777;"):
        text = p.get_text(strip=True)

        if "Rating" in text:
            rating_text = text.replace("Rating: ⭐", "").strip()
            datas["rating"] = rating_text.replace("/ 5", "").strip()
        elif "Colors" in text:
            # Extract only the numeric value for colors (e.g., "3")
            colors_text = text.replace("Colors:", "").strip()
            # Using regex to extract the numeric part
            numbers = re.findall(r'\d+', colors_text)
            datas["colors"] = int(numbers[0]) if numbers else 0
        elif "Size:" in text:
            datas["size"] = text.replace("Size:", "").strip()
        elif "Gender:" in text:
            datas["gender"] = text.replace("Gender:", "").strip()
    
    # Add Timestamp
    datas["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return datas

def scrape_all_pages(base_url, delay=1):
    """
    Mengambil keseluruhan data dari tiap-tiap halaman webpage
    dengan mekanisme try-except untuk penanganan error yang lebih baik
    """
    print("🔄 Memulai proses scraping data")
    items_data = []
    page_num = 1

    while True:
        try:
            # Tentukan URL berdasarkan halaman
            if page_num == 1:
                url = base_url
            else:
                url = f"{base_url.rstrip('/')}/page{page_num}"
            
            print(f"🔼 Scraping halaman: {url}")
            content = fetching_content(url)

            if not content:
                print("❌ Gagal mengambil konten halaman.")
                break

            try:
                soup = BeautifulSoup(content, "html.parser")
                div_elements = soup.find_all('div', class_='product-details')

                if not div_elements:
                    print("❌ Tidak ada produk ditemukan, berhenti scraping.")
                    break

                for div in div_elements:
                    try:
                        item = extract_fashion_data(div)
                        items_data.append(item)
                    except Exception as e:
                        print(f"⚠️ Gagal mengekstrak item: {e}")
                        continue  # lanjut ke produk berikutnya

                # Cek apakah ada tombol "next"
                next_button = soup.find('li', class_='page-item next')
                if next_button:
                    page_num += 1
                    time.sleep(delay)
                else:
                    print("✅ Scraping selesai, tidak ada halaman berikutnya.")
                    break

            except Exception as e:
                print(f"⚠️ Gagal memproses halaman: {e}")
                break

        except Exception as e:
            print(f"❌ Terjadi kesalahan tidak terduga saat scraping: {e}")
            break

    return items_data
