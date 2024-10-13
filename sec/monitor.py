import aiohttp
import asyncio
from time import time
from collections import deque

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
    def process_filings(filings: list[Filing], latest_ans: deque[str]):
        for f in filings:
            if f.accession_no in latest_ans: continue
            latest_ans.append(f.accession_no)
            broadcast(f, server)

    latest_ans: deque[str] = deque([], maxlen=Edgar.RSS_FEED_COUNT*2)
    while True:
        t0 = time()
        filings = await fetch_filings()
        if not filings:
            # costilikiiiii
            print('Wtf no filings?')
            await asyncio.sleep(1)
            continue
        process_filings(filings, latest_ans)
        t1 = time()
        if t1 - t0 < 0.15: await asyncio.sleep(0.15 - (t1 - t0))