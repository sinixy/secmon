import re
import json
import aiohttp


title_regex = re.compile(r"(.*) - (.*) \((\d+)\) \((.*)\)")

async def get_cik_to_ticker_lookup() -> dict[int, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.sec.gov/files/company_tickers.json") as resp:
            tickers_json = json.loads(await resp.text())
    return {
        value['cik_str']: value['ticker'] 
        for value in tickers_json.values()
    }

def parse_title(title: str) -> dict:
    """
    Given the title in this example

    "144 - monday.com Ltd. (0001845338) (Subject)"
    which contains the form type, company name, CIK, and status
    parse into a tuple of form type, company name, CIK, and status using regex
    """
    match = title_regex.match(title)
    assert match, f"Could not parse title: {title} using regex: {title_regex}"
    form, company_name, cik, _ = match.groups()
    return {
        'cik': int(cik),
        'company': company_name,
        'form': form
    }

