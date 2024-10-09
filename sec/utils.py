import re
import aiohttp
import xmltodict

from utils import asyncify
from config import Edgar

title_regex = re.compile(r"(.*) - (.*) \((\d+)\) \((.*)\)")


# this cik_to_ticker stuff is fucking ugly, but I don't wanna connect a whole database/redis just for this data,
# so just don't dereference it accidentally and you should be fine
cik_to_ticker = {}
async def update_cik_to_ticker():
    cik_to_ticker.clear()
    cik_to_ticker.update(await get_cik_to_ticker_lookup())


async def get_cik_to_ticker_lookup() -> dict[int, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.sec.gov/files/company_tickers.json", headers=Edgar.HEADERS) as resp:
            tickers_json = await resp.json()
    return {
        value['cik_str']: value['ticker'] 
        for value in tickers_json.values()
    }

@asyncify
def parse_feed(raw_feed: str):
    return xmltodict.parse(raw_feed)

def parse_title(title: str) -> dict:
    match = title_regex.match(title)
    assert match, f"Could not parse title: {title} using regex: {title_regex}"
    form, company_name, cik, _ = match.groups()
    return {
        'cik': int(cik),
        'company': company_name,
        'form': form
    }

