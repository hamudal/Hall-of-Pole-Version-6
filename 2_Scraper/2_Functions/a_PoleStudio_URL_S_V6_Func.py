import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

class PoleStudioScraper:
    """
    A class for scraping data from pole studio websites.
    """

    def __init__(self, url):
        """
        Initialize the scraper with a given URL.
        """
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def extract_overview_buttons(self):
        """
        Extract overview buttons from the pole studio website.
        """
        buttons_divs = self.soup.find_all('div', class_="MuiStack-root css-sgccrm")
        button_texts = [button.text for div in buttons_divs for button in div.find_all('a')]
        return button_texts

    def extract_pole_studio_name(self):
        """
        Extract the name of the pole studio.
        """
        name_element = self.soup.find('h1', class_='MuiTypography-root MuiTypography-h1 css-qinhw0')
        return name_element.text if name_element else None

    def extract_contact_info(self):
        """
        Extract contact information from the pole studio website.
        """
        contact_divs = self.soup.find_all('div', class_='css-1x2phcg')
        contact_info = {'E-Mail': None, 'Homepage': None, 'Telefon': None}
        for div in contact_divs:
            for a in div.find_all('a', href=True):
                href = a['href']
                if href.startswith('mailto:'):
                    contact_info["E-Mail"] = href.replace('mailto:', '')
                elif href.startswith('tel:'):
                    contact_info["Telefon"] = href.replace('tel:', '')
                else:
                    contact_info["Homepage"] = href
        return contact_info

    def extract_address(self):
        """
        Extract address information from the pole studio website.
        """
        address_element = self.soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-1619old')
        if address_element:
            address_text = address_element.text.split(',')
            return address_text, address_text[1].split(" ")[2], address_text[1].split(" ")[1], address_text[0]
        return None, None, None, None

    def extract_description(self):
        """
        Extract the description of the pole studio.
        """
        description_element = self.soup.find('div', class_="MuiBox-root css-0")
        return description_element.text if description_element else None

    def extract_rating(self):
        """
        Extract the rating of the pole studio.
        """
        rating_element = self.soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-2g7rhg')
        if rating_element:
            parts = rating_element.text.split('(')
            return parts[0].strip(), parts[1].replace(')', '').strip()
        return None, None

    def extract_rating_factors(self):
        """
        Extract rating factors from the pole studio website.
        """
        items = self.soup.find_all('div', class_='MuiStack-root css-95g4uk')
        return [f"{item.find('p', class_='MuiTypography-root MuiTypography-body1 css-1k55edk').text}: {item.find('p', class_='MuiTypography-root MuiTypography-body1 css-1y0caop').text}" for item in items if item.find('p', class_='MuiTypography-root MuiTypography-body1 css-1k55edk') and item.find('p', class_='MuiTypography-root MuiTypography-body1 css-1y0caop')]

    def extract_art(self):
        """
        Extract art information from the pole studio website.
        """
        art_elements = self.soup.find_all("p", class_="MuiTypography-root MuiTypography-body1 css-6ik050")
        return [art.text for art in art_elements]

    def extract_sale(self):
        """
        Extract sale information from the pole studio website.
        """
        sale_element = self.soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-153qxhx")
        return sale_element.text if sale_element else None

    def extract_image_urls(self):
        """
        Extract image URLs from the pole studio website.
        """
        pictures = self.soup.find_all("div", class_="MuiBox-root css-1fivxf")
        return [img["src"] for div in pictures if (img := div.find("img")) and img.has_attr("src")]

class ScraperErrorManager:
    """
    A class for handling errors that may occur during scraping.
    """

    def __init__(self, logger_name='scraper_error_logger'):
        """
        Initialize the error manager with a logger.
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)  # You can adjust the logging level as needed

    def log_error(self, message):
        """
        Log an error message.
        """
        self.logger.error(message)

    def log_warning(self, message):
        """
        Log a warning message.
        """
        self.logger.warning(message)

    def handle_url_error(self, url, exception):
        """
        Handle errors related to unreachable URLs.
        """
        error_message = f"Error accessing URL '{url}': {str(exception)}"
        self.log_error(error_message)

    def handle_element_error(self, element_name, exception):
        """
        Handle errors related to unreachable or missing elements on the webpage.
        """
        error_message = f"Error accessing element '{element_name}': {str(exception)}"
        self.log_warning(error_message)

# Example usage
url_list_s = ["https://www.eversports.de/s/poda-studio", "https://www.eversports.de/s/nordpole"]

error_manager = ScraperErrorManager()

for url in url_list_s:
    try:
        pole_scraper = PoleStudioScraper(url)
        buttons_list = pole_scraper.extract_overview_buttons()
        print(f"Buttons for {url}: {buttons_list}")
        # Include other extraction methods as needed
    except requests.exceptions.RequestException as url_error:
        error_manager.handle_url_error(url, url_error)
    except Exception as element_error:
        error_manager.handle_element_error("overview buttons", element_error)
