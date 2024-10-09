from datetime import datetime

from .utils import cik_to_ticker, parse_title


class Filing:

    def __init__(self, cik: int, company: str, form: str, accession_number: str, updated: datetime):
        self.cik = cik
        self.ticker = cik_to_ticker.get(self.cik, '')
        self.company = company
        self.form = form
        self.accession_number = accession_number
        self.updated = updated

    def fits(self, filter: dict[str, list]) -> bool:
        # ugly but fine for now; gotta make some sort of a filter class later with validations and stuff
        fits = True
        for k, v in filter.items():
            if self.__getattribute__(k) not in v:
                fits = False
                break
        return fits
    
    def to_dict(self) -> dict:
        return {
            'ticker': self.ticker,
            'cik': self.cik,
            'company': self.company,
            'form': self.form,
            'accession_number': self.accession_number,
            'updated': self.updated.isoformat(),
        }

    @classmethod
    def from_xml_dict_entry(cls, entry: dict):
        title_dict = parse_title(entry['title'])
        updated = datetime.fromisoformat(entry['updated'])
        accession_number = entry['id'].split('=')[-1]
        return cls(**title_dict, accession_number=accession_number, updated=updated)