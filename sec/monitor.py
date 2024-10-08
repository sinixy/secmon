import aiohttp
import asyncio
from config import Edgar

from server import Server
from sec.utils import parse_feed
from sec.filing import Filing


async def broadcast(filing: Filing, server: Server):
    pass

async def fetch_filings(page: int = 0) -> list[Filing]:
    filings = []
    async with aiohttp.ClientSession() as session:
        async with session.get(Edgar.RSS_FEED_URL.format(start=Edgar.RSS_FEED_COUNT * page), headers=Edgar.HEADERS) as resp:
            feed = await parse_feed(await resp.text())
            for e in feed['feed']['entry']:
                filings.append(Filing.from_xml_dict_entry(e))
    return filings

async def monitor_filings(server: Server):
    def process_filings(filings: list[Filing], latest_an: str) -> bool:
        for f in filings:
            if f.accession_number == latest_an: return True
            asyncio.create_task(broadcast(f, server))
        return False

    filings = await fetch_filings(0)
    latest_an = filings[-1].accession_number
    while True:
        page = 0
        filings = await fetch_filings(page)
        new_latest_an = filings[0].accession_number
        done = process_filings(filings, latest_an)
        while not done:
            if page == 9: raise Exception("That's too many pages; something gotta be wrong")
            page += 1
            filings = await fetch_filings(page)
            done = process_filings(filings, latest_an)
        latest_an = new_latest_an
            