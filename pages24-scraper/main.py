from scraper import Pages24Scraper
from utils import list_of_dicts_to_csv

if __name__ == '__main__':

    # Input Parameters for the Scraper
    FILENAME = 'pages24.csv'
    scrape_url = 'https://www.pages24.com/somerset-tx/san-antonio'

    # scraping the data
    scraper = Pages24Scraper(url=scrape_url)
    data = scraper.scrape()
    count = len(data)
    if count == 0:
        print("No data found")
    else:
        print(f"{count} entries have been extracted successfully")
        list_of_dicts_to_csv(data_list=data, csv_filename=FILENAME)