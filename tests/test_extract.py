import sys
import os
# Menambahkan direktori root ke sys.path agar modul utils bisa diimpor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_all_pages, fetching_content, extract_fashion_data  # Adjust this import
from bs4 import BeautifulSoup

# Test for the scrape_all_pages function
@pytest.fixture
def mock_fetching_content():
    with patch('utils.extract.fetching_content') as mock_fetch:
        yield mock_fetch

@pytest.fixture
def mock_extract_fashion_data():
    with patch('utils.extract.extract_fashion_data') as mock_extract:
        yield mock_extract

# Test for a successful scraping scenario
def test_scrape_all_pages_success(mock_fetching_content, mock_extract_fashion_data):
    # Mock the fetching_content to return HTML content for two pages
    mock_fetching_content.side_effect = [
        b"<html><body><div class='product-details'><h3 class='product-title'>Product 1</h3><div class='price-container'><span class='price'>$20</span></div></div><li class='page-item next'></li></body></html>",
        b"<html><body><div class='product-details'><h3 class='product-title'>Product 2</h3><div class='price-container'><span class='price'>$30</span></div></div></body></html>", 
        None  # Simulate no more content
    ]
    
    # Mock the extract_fashion_data to return dummy data
    mock_extract_fashion_data.side_effect = [
        {"title": "Product 1", "price": "$20", "colors": 2, "size": "M", "gender": "Unisex", "rating": "4", "timestamp": "2023-05-01 12:00:00"},
        {"title": "Product 2", "price": "$30", "colors": 3, "size": "L", "gender": "Male", "rating": "4.5", "timestamp": "2023-05-01 12:00:00"}
    ]
    
    base_url = "http://example.com"
    items_data = scrape_all_pages(base_url, delay=0)

    # Assert that the function correctly processes two products
    assert len(items_data) == 2
    assert items_data[0]['title'] == "Product 1"
    assert items_data[1]['price'] == "$30"
    assert items_data[1]['colors'] == 3

# Test for no content on a page
def test_scrape_all_pages_no_content(mock_fetching_content):
    # Mock the fetching_content to return an empty response (None)
    mock_fetching_content.side_effect = [None, None]

    base_url = "http://example.com"
    items_data = scrape_all_pages(base_url, delay=0)

    # Assert that no items are collected if no content is fetched
    assert len(items_data) == 0

# Test for an error during extraction of data
def test_scrape_all_pages_error(mock_fetching_content, mock_extract_fashion_data):
    # Mock fetching_content to return HTML content for one page
    mock_fetching_content.side_effect = [
        b"<html><body><div class='product-details'><h3 class='product-title'>Product 1</h3><div class='price-container'><span class='price'>$20</span></div></div></body></html>", 
        None  # Simulate no more content
    ]
    
    # Mock extract_fashion_data to raise an error during extraction for the first item
    mock_extract_fashion_data.side_effect = Exception("Error extracting data")

    base_url = "http://example.com"
    items_data = scrape_all_pages(base_url, delay=0)

    # Assert that one item is processed despite an extraction error
    assert len(items_data) == 1  # There should be one item processed
    assert "error" in items_data[0]  # The item should contain an "error" key
    assert items_data[0]["error"] == "Failed to extract data: Error extracting data"  # Ensure the error message is present
