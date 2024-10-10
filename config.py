from dotenv import load_dotenv
from os import getenv

load_dotenv()


SERVER_PORT = getenv("SERVER_PORT")

class Edgar:
    IDENTITY = getenv("EDGAR_IDENTITY")
    HEADERS = {
        'User-Agent': IDENTITY,
        'Host': 'www.sec.gov'
    }
    RSS_FEED_COUNT = 100
    # exclude ownership for now
    RSS_FEED_URL = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&owner=exclude&start={start}' + f'&count={RSS_FEED_COUNT}&output=atom'
    
