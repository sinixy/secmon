import re
import json
import aiohttp
import xmltodict

from utils import asyncify

title_regex = re.compile(r"(.*) - (.*) \((\d+)\) \((.*)\)")

async def get_cik_to_ticker_lookup() -> dict[int, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.sec.gov/files/company_tickers.json") as resp:
            tickers_json = json.loads(await resp.text())
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

