import asyncio
import aiohttp
import datetime
import xmltodict

from config import EDGAR_RSS_FEED, EDGAR_HEADERS
from edgar import parse_title


class Filing:

    def __init__(self, cik: int, company: str, form: str, accession_number: str, updated: datetime.datetime):
        self.cik = cik
        self.company = company
        self.form = form
        self.accession_number = accession_number
        self.updated = updated

    @classmethod
    def from_xml_dict_entry(cls, entry: dict):
        title_dict = parse_title(entry['title'])
        updated = entry['updated']
        accession_number = entry['id'].split('=')[-1]
        return cls(**title_dict, accession_number=accession_number, updated=updated)

async def fetch_filings() -> list[Filing]:
    filings = []
    async with aiohttp.ClientSession() as session:
        async with session.get(EDGAR_RSS_FEED, headers=EDGAR_HEADERS) as resp:
            feed = xmltodict.parse(await resp.text())
            for e in feed['feed']['entry']:
                filings.append(Filing.from_xml_dict_entry(e))
    return filings

async def main():
    pass