import math
from ..locators.results_page_locators import AllPropertiesLocators
from ..parsers.properties_parser import PropertyParser


class PropertiesPage:
    """Class for a given page of properties."""

    def __init__(self, page_tag):
        self.page_tag = page_tag

    @property
    def properties(self):
        """Returns a list of PropertyParser objects
         for all the properties in a page.
         """

        locator = AllPropertiesLocators.PROP
        all_props = self.page_tag.select(locator)
        return [PropertyParser(p) for p in all_props]

    @property
    def page_count(self):
        """Returns the totla number of pages."""

        # There are 20 listings in a page, hence the calculation.
        pages_count = math.ceil(self.listing_count/20)
        return pages_count

    @property
    def listing_count(self):
        """Returns the total number of listings."""

        locator = AllPropertiesLocators.RESULTS_COUNT
        listings = int(self.page_tag.select_one(locator).text.replace(',', '').strip('()'))
        return listings

