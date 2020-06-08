import re
import folium
from bs4 import BeautifulSoup
from utils import async_fetch


class RealEstateMap:
    """Class for turning a data-frame into a web map
    containing the relevant points of interest and a popup for
    each one with a link to their pages.
    """

    def __init__(self, df):
        self.df = df

    @property
    def get_html(self):
        """Returns an html string of a web map based on the given data-frame."""

        geos = self._get_geos()
        web_map = folium.Map(tiles='OpenStreetMap')

        html = """
        Address: %s<br>
        <a href="%s" target="_blank">Click to see the property</a>
        """

        # Setting up the zoom level of the map to fit the relevant interest points.
        sw = self.df[['LAT', 'LNG']].min().values.tolist()
        ne = self.df[['LAT', 'LNG']].max().values.tolist()
        web_map.fit_bounds([sw, ne])

        # Configuring the interest point with their co-responding parameters on the map.
        for address, link, lat, lng in geos:
            iframe = folium.IFrame(html=html % (address, link), width=250, height=75)
            folium.Marker(location=(lat, lng), popup=folium.Popup(iframe)).add_to(web_map)

        return web_map._repr_html_()

    def _get_geos(self):
        """Returns a zip object of the addresses and their coordinates."""

        coordinates = self._get_coordinates()
        self.df['LAT'] = [c[0] for c in coordinates]
        self.df['LNG'] = [c[1] for c in coordinates]

        self.df.dropna(subset=['Address', 'Link', 'LAT', 'LNG'], how='any', inplace=True)
        geos = zip(self.df.loc[:, 'Address'], self.df.loc[:, 'Link'], self.df.loc[:, 'LAT'], self.df.loc[:, 'LNG'])
        return geos

    def _get_coordinates(self):
        """Extracting the coordinates of all the addresses by scraping the
        google-maps search result of each address.
        By making asynchronous requests I minimize the running time
        substantially. Returning a list of tuples of all the coordinates.
        """

        coordinates = []
        base_url = r'https://www.google.com/maps/search/'
        self.df['Full_address'] = self.df[['Address', 'State']].agg(' '.join, axis=1)

        urls = [base_url + add.replace(' ', '%20')
                for add in self.df['Full_address']]

        # Fetching the html all the urls asynchronously.
        pages = async_fetch.all_pages(urls)
        # Extracting the coordinates from each.
        for page_content in pages:
            page_soup = BeautifulSoup(page_content, 'html.parser')
            try:
                url = page_soup.select_one('head meta[itemprop="image"]').attrs['content']

                phrase = 'center=(.*?)&'
                coord_str = re.search(phrase, url).group(1)
                lat, lng = coord_str.split('%2C')

                coordinates.append((float(lat), float(lng)))
            except AttributeError:
                coordinates.append((None, None))
        return coordinates


