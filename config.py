from dotenv import load_dotenv
from os import getenv

load_dotenv()


EDGAR_IDENTITY = getenv("EDGAR_IDENTITY")
EDGAR_HEADERS = {
    'User-Agent': EDGAR_IDENTITY,
    'Host': 'www.sec.gov'
}
EDGAR_RSS_FEED = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&count=100&output=atom'