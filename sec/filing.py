from datetime import datetime

from .utils import parse_title


class Filing:

    def __init__(self, cik: int, company: str, form: str, accession_number: str, updated: datetime):
        self.cik = cik
        self.company = company
        self.form = form
        self.accession_number = accession_number
        self.updated = updated

    def fits(self, filters: dict) -> bool:
        pass

    @classmethod
    def from_xml_dict_entry(cls, entry: dict):
        title_dict = parse_title(entry['title'])
        updated = datetime.fromisoformat(entry['updated'])
        accession_number = entry['id'].split('=')[-1]
        return cls(**title_dict, accession_number=accession_number, updated=updated)