from datetime import datetime
import argparse
import os
import asyncio
import aiohttp

from nextEpisodeCalendar.databaseHandler import DB
from nextEpisodeCalendar.event import Event
from nextEpisodeCalendar.scrapper import SeriesScrapper
from nextEpisodeCalendar.CalendarApi import API


DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
DB_PATH = os.path.join(DATA_DIR, 'series.db')
db = DB(DB_PATH)

calendar = API() 

async def createEvents(scrapper: SeriesScrapper):
    series = db.getAll()

    episodes = await asyncio.gather(*[scrapper.findDate(s[1], s[0]) for s in series])
    events = [Event(summary=ep[0], description=ep[1], start=ep[2].replace(hour=15)) for ep in episodes if ep]
    calendar.addEvents(events)


async def addSeries(scrapper, name: str, url: str = None):
    if not url:
        url = await scrapper.findUrl(name)

    if not url:
        print('No series found, try --url')
        return

    db.insert(name, url)

def listSeries():
    print(db.getAll())

def listEpisodes():
    pass

async def main(loop):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', type=str, dest='add', help='Add a new series to db')
    parser.add_argument('--url', type=str, help='The wikipedia url, if not found by the scrapper')
    parser.add_argument('-l', '--list', action='store_true', dest='series', help='List your watchlist')
    parser.add_argument('-e', '--episodes', action='store_true', dest='episodes', help='List the next episodes')
    args = parser.parse_args()

    session = aiohttp.ClientSession(loop=loop)
    scrapper = SeriesScrapper(session)

    if args.add:
        await addSeries(scrapper, args.add, args.url)
    elif args.series:
        listSeries()
    elif args.episodes:
        listEpisodes()
    else:
        await createEvents(scrapper)

    await session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(main(loop))

    loop.close()
