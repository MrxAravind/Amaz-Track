import requests
from bs4 import BeautifulSoup
import time
import random
from typing import Dict, Optional

class AmazonScraper:
    def __init__(self):
        # Using a realistic user agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.base_url = "https://www.amazon.com"

    def get_product_details(self, product_url: str) -> Optional[Dict]:
        """
        Fetch product details from Amazon product page
        
        Args:
            product_url (str): Complete Amazon product URL
            
        Returns:
            dict: Dictionary containing product details
        """
        try:
            # Add delay to be respectful to Amazon's servers
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(product_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Failed to fetch page. Status code: {response.status_code}")
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product details
            product_details = {
                'id':product_url.split("/")[-1],
                'name': self._get_title(soup),
                'price': self._get_price(soup),
                'rating': self._get_rating(soup),
                'review_count': self._get_review_count(soup),
                'availability': self._get_availability(soup),
                'description': self._get_description(soup),
                'image_url': self._get_image(soup),
                'explore_link': product_url
            }
            
            return product_details
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
    
    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract product title"""
        title_elem = soup.find('span', {'id': 'productTitle'})
        return title_elem.text.strip() if title_elem else "Not found"
    
    def _get_price(self, soup: BeautifulSoup) -> str:
        """Extract product price"""
        price_elem = soup.find('span', {'class': 'a-price-whole'})
        if price_elem:
            return price_elem.text.strip()
        return "Not found"
    
    def _get_rating(self, soup: BeautifulSoup) -> str:
        """Extract product rating"""
        rating_elem = soup.find('span', {'class': 'a-icon-alt'})
        return rating_elem.text.split()[0] if rating_elem else "Not found"
    
    def _get_review_count(self, soup: BeautifulSoup) -> str:
        """Extract number of reviews"""
        review_elem = soup.find('span', {'id': 'acrCustomerReviewText'})
        return review_elem.text.split()[0] if review_elem else "Not found"
    
    def _get_availability(self, soup: BeautifulSoup) -> str:
        """Extract availability status"""
        availability_elem = soup.find('div', {'id': 'availability'})
        return availability_elem.text.strip() if availability_elem else "Not found"
    
    def _get_description(self, soup: BeautifulSoup) -> str:
        """Extract product description"""
        desc_elem = soup.find('div', {'id': 'productDescription'})
        return desc_elem.text.strip() if desc_elem else "Not found"

    def _get_image(self, soup: BeautifulSoup) -> str:
        """Extract product image URL"""
        image_elem = soup.find('img', {'id': 'landingImage'})
        return image_elem['src'] if image_elem else "Image not found"