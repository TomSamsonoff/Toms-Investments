import pandas
import requests
from bs4 import BeautifulSoup
from .pages.properties_page import PropertiesPage
from utils import async_fetch


def _get_df(properties):
    """Returns a data-frame object based on a given
    list of PropertyParser objects.
    """

    # List of data-frame objects -- each for every property.
    prop_lst = [pandas.DataFrame(
        [[p.price, p.state, p.address, p.size, p.description, p.link]],
        columns=['Price', 'State', 'Address', 'Size', 'Description', 'Link'])
        for p in properties]

    df = pandas.concat(prop_lst, ignore_index=True)
    df.index += 1
    return df


class RealEstate:
    """Class for getting the parameters of the properties in a given US state.
    Scraping the website: 'www.century21global.com' and extracting the relevant
    parameters of all the properties.
    """

    def __init__(self, state):
        self.base_url = f'https://www.century21global.com/for-sale-residential/USA/{state}?pageNo='
        self.pages_count = self.first_page.page_count
        self.listings_count = self.first_page.listing_count

    @property
    def top_properties(self):
        """Returns a data-frame of all the properties showing in the first page."""

        properties = self.first_page.properties  # List of PropertyParser objects
        df = _get_df(properties)
        return df

    @property
    def all_properties(self):
        """Returns a data-frame of all the properties in all page.

        Fetching the pages asynchronously minimizes the running time
        significantly.
        """

        properties = []
        # List of urls of all the relevant pages.
        urls = [f'{self.base_url}{page_num+1}'
                for page_num in range(self.pages_count)]

        # Fetching the pages asynchronously
        pages = async_fetch.all_pages(urls)

        # Creating a list of PropertyParser objects
        for page_content in pages:
            page_soup = BeautifulSoup(page_content, 'html.parser')
            page = PropertiesPage(page_soup)
            properties.extend(page.properties)

        df = _get_df(properties)
        return df

    @property
    def first_page(self):
        """Returns a PropertiesPage object of the first page"""

        page_content = requests.get(self.base_url+'1').content
        page_soup = BeautifulSoup(page_content, 'html.parser')
        first_page = PropertiesPage(page_soup)
        return first_page

