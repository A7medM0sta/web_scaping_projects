from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import math
from utils import clean_phone_number

class Pages24Scraper:
    def __init__(self, url):
        """
        Initialize the BusinessScraper with the provided URL.
        """
        self.domain = "www.pages24.com"
        self.url = url
        self.current_page = 1
        self.max_page = None
        self.page_size = 25
        self.data = []

    def validate_url(self, url):

        parsed_url = urlparse(url)
        if parsed_url.netloc != self.domain:
            return False
        path_segments = parsed_url.path.strip('/').split('/')
        if len(path_segments) != 2:
            return False
        return True

    def extract_business_info(self, soup):
        """
        Extract business information from the given BeautifulSoup soup object.
        """
        base_url = 'https://www.pages24.com'
        business_info = {}

        # Extract business name
        business_name_tag = soup.find('span', itemprop='name')
        if business_name_tag:
            business_name = business_name_tag.text.strip()
            business_info['name'] = business_name

            # Extract business URL
            business_url = business_name_tag.find_parent('a')['href']
            business_info['url'] = base_url + business_url

        # Extract address details
        address_span = soup.find('span', itemprop='streetAddress')
        if address_span:
            street_address = address_span.text.strip()
            business_info['street_address'] = street_address

        locality_span = soup.find('span', itemprop='addressLocality')
        if locality_span:
            locality = locality_span.text.strip()
            business_info['locality'] = locality

        postal_code_span = soup.find('span', itemprop='postalCode')
        if postal_code_span:
            postal_code = postal_code_span.text.strip()
            business_info['postal_code'] = postal_code

        # Extract phone number
        phone_span = soup.find('span', itemprop='telephone')
        if phone_span:
            phone_number = phone_span.text.strip()
            business_info['phone_number'] = clean_phone_number(phone_number)

        # Extract description
        description_paragraph = soup.find('p', itemprop='description')
        if description_paragraph:
            description = description_paragraph.text.strip()
            business_info['description'] = description

        # Extract keywords
        keywords_div = soup.find('div', class_='keywords')
        if keywords_div:
            keywords = keywords_div.text.strip()
            business_info['keywords'] = keywords

        return business_info

    def initialize(self):
        """
        Initialize the scraper by making an initial request to the URL and setting the maximum page count.
        """
        if self.validate_url(self.url):
            res = requests.get(self.url)
            if res.status_code == 200:
                self.soup = BeautifulSoup(res.content, 'html.parser')
                try:
                    print(f'checking the {self.url}')
                    counter = self.soup.select_one(
                        '.searchresult-counter').text.strip().split(' ')[0]
                    counter = int(counter)
                    self.max_page = math.ceil(counter / self.page_size)
                    return True
                except Exception as e:
                    print(f"Error initializing scraper: {e}")
                    return False
            else:
                print(f"Server Error {res.status_code}")
                return False
        print("Invalid URL")

    def response_extract(self, page_no):
        """
        Extract the content of a specific page from the URL.
        """
        response = requests.get(f'{self.url}/{page_no}')
        print(f"Scraping page: {page_no}/{self.max_page}")
        if response.status_code == 200:
            return response.content

    def extract_pages(self):
        """
        Extract business information from all pages and store it in the data list.
        """
        if self.initialize():
            while self.current_page <= self.max_page:
                content = self.response_extract(self.current_page)
                soup = BeautifulSoup(content, 'html.parser')
                items = soup.select('.search-item')

                for item in items:

                    # passing the soup and storing the return dictioanry
                    business_info = self.extract_business_info(item)

                    # appending the data to the list
                    self.data.append(business_info)

                self.current_page += 1

    def scrape(self):
        """
        Performing the scraping process and return the collected data.
        """
        self.extract_pages()
        return self.data