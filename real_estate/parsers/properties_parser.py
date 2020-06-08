from ..locators.properties_locators import PropertyLocators


class PropertyParser:
    """Class for extracting the relevant information for each property."""

    def __init__(self, prop_tag):
        self.prop_tag = prop_tag

    def __repr__(self):
        return f'A property in: {self.address}'

    @property
    def price(self):
        try:
            locator = PropertyLocators.PRICE
            price = self.prop_tag.select_one(locator).text
            return price
        except:
            pass

    @property
    def address(self):
        try:
            locator = PropertyLocators.ADDRESS
            address = self.prop_tag.select_one(locator).text.replace('/', ' ')
            return address
        except:
            pass

    @property
    def state(self):
        try:
            locator = PropertyLocators.STATE
            state = self.prop_tag.select_one(locator).text.strip()
            return state
        except:
            pass

    @property
    def size(self):
        try:
            locator = PropertyLocators.SIZE
            size = self.prop_tag.select_one(locator).text.strip()
            return size
        except:
            pass

    @property
    def description(self):
        try:
            locator = PropertyLocators.DESC
            description = self.prop_tag.select(locator)[-1].text
            if 'bed' in description:
                return description
        except:
            pass

    @property
    def link(self):
        try:
            locator = PropertyLocators.LINK
            link = self.prop_tag.select_one(locator).attrs['href']
            base_url = r'https://www.century21global.com/property'
            return base_url + link
        except:
            pass
