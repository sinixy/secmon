import aiohttp
import asyncio
from time import time

from config import Edgar
from server import Server
from sec.utils import parse_feed
from sec.filing import Filing


def broadcast(filing: Filing, server: Server):
    for con_id, filter in server.filters():
        if filing.fits(filter):
            asyncio.create_task(
                server.send(con_id, {'event': 'filing', 'data': filing.to_dict()})
            )

async def fetch_filings(page: int = 0) -> list[Filing]:
    try:
        return await __fetch_filings(page)
    except Exception as e:
        print('Fetch filings error:', e)
        return []

async def __fetch_filings(page: int = 0) -> list[Filing]:
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
            if f.accession_no == latest_an: return True
            broadcast(f, server)
        return False

    filings = await fetch_filings(0)
    latest_an = filings[-1].accession_no
    while True:
        t0 = time()
        page = 0
        filings = await fetch_filings(page)
        if not filings:
            # costilikiiiii
            print('Wtf no filings?')
            await asyncio.sleep(1)
            continue 
        # new_latest_an = filings[0].accession_no
        # done = process_filings(filings, latest_an)
        # while not done:
        #     if page == 5:
        #         print("That's too many pages; something gotta be wrong.", latest_an)
        #         break
        #     page += 1
        #     filings = await fetch_filings(page)
        #     if not filings: break
        #     done = process_filings(filings, latest_an)
        process_filings(filings, latest_an)
        latest_an = filings[0].accession_no
        t1 = time()
        if t1 - t0 < 0.13: await asyncio.sleep(0.13 - (t1 - t0))