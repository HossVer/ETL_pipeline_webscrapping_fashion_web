import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# Menambahkan direktori root ke sys.path agar modul utils bisa diimpor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import fetching_content, extract_fashion_data

# ===============================
# Test untuk fetching_content()
# ===============================

@patch('utils.extract.requests.Session.get')
def test_fetching_content_success(mock_get):
    mock_response = MagicMock()
    mock_response.content = b"<html><body>Test</body></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetching_content("http://dummy-url.com")
    assert result == b"<html><body>Test</body></html>"

@patch('utils.extract.requests.Session.get')
def test_fetching_content_failure(mock_get):
    mock_get.side_effect = RequestException("Request failed")  # << gunakan RequestException
    result = fetching_content("http://dummy-url.com")
    assert result is None

# ===================================
# Test untuk extract_fashion_data()
# ===================================

def test_extract_fashion_data_minimal_html():
    html = """
    <div class="product-details">
        <h3 class="product-title">Cool Shirt</h3>
        <div class="price-container">
            <span class="price">$15</span>
        </div>
        <p style="font-size: 14px; color: #777;">Colors: 3 Colors</p>
        <p style="font-size: 14px; color: #777;">Size: M</p>
        <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
        <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.5 / 5</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find('div', class_='product-details')
    result = extract_fashion_data(article)

    assert result['title'] == "Cool Shirt"
    assert result['price'] == "$15"
    assert result['colors'] == 3
    assert result['size'] == "M"
    assert result['gender'] == "Unisex"
    assert result['rating'] == "4.5"
    assert "timestamp" in result
