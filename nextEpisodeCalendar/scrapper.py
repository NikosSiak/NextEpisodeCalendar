from bs4 import BeautifulSoup as soup
from datetime import datetime
import asyncio
import aiohttp


class SeriesScrapper:

    def __init__(self, session: aiohttp.ClientSession):
        self.now = datetime.now()
        self.aiohttp_session = session
    
    async def findUrl(self, series_name: str) -> str:
        '''
        Finds the wikipedia url for a series. The two common urls this function tries are 
        https://en.wikipedia.org/wiki/List_of_{series_name}_episodes and 
        https://en.wikipedia.org/wiki/{series_name}_(TV_series)

        Parameters:
            series_name (str): The series name.

        Returns:
            url (str): The series wikipedia url, if it exists.
        '''

        series_name = series_name.replace(' ', '_')
        url = f'https://en.wikipedia.org/wiki/List_of_{series_name}_episodes'
        async with self.aiohttp_session.get(url) as resp:
            if resp.status == 200:
                return url
        url = f'https://en.wikipedia.org/wiki/{series_name}_(TV_series)'
        async with self.aiohttp_session.get(url) as resp:
            if resp.status == 200:
                return url
    
    
    async def findDate(self, url: str, name: str) -> tuple:
        '''
        Finds the date of the next episode for the given url.

        Parameters:
            url (str): The series url.
            name (str): The series name, only used to return in the tuple
        
        Returns:
            episode (tuple): A tuple consisting from 3 strings. 
            The series name, the next episode title and the date the episode will be aired.
        '''

        async with self.aiohttp_session.get(url) as resp:
            if resp.status != 200:
                return None
            page_html = await resp.text()

        page_soup = soup(page_html, "html.parser")

        tr = page_soup.findAll('tr', {'class': 'vevent'})
        now = datetime.now()
        for row in tr:
            for span in row('span'):
                span.decompose()
            for sup in row('sup'):
                sup.decompose()
            
            ep_title = row('td')[1].text
            ep_date = None
            # the air date isn't always on the same column
            for td in reversed(row('td')):
                try:
                    ep_date = datetime.strptime(td.text, "%B %d, %Y")
                    break
                except ValueError:
                    continue
            
            if ep_date and now < ep_date:
                return (name, ep_title, ep_date)
        
        return None

