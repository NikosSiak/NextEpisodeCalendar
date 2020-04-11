from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from datetime import datetime
import asyncio
import aiohttp


class SeriesScrapper:

    def __init__(self, session: aiohttp.ClientSession):
        self.now = datetime.now()
        self.aiohttp_session = session
    
    async def findUrl(self, series_name: str) -> str:
        series_name = series_name.replace(' ', '_')
        url = f'https://en.wikipedia.org/wiki/List_of_{series_name}_episodes'
        async with self.aiohttp_session.get(url) as resp:
            if resp.status == 200:
                return url
        url = f'https://en.wikipedia.org/wiki/{series_name}_(TV_series)'
        async with self.aiohttp_session.get(url) as resp:
            if resp.status == 200:
                return url
    
    
   
