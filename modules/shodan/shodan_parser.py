from typing import List

from bs4 import BeautifulSoup, Tag

from modules.shodan.shodan_result import ShodanSearchResult, ShodanResult

ENTRY_CLASS = 'result'
HOSTNAME_CLASS = 'hostnames'


class ShodanParser:

    @classmethod
    def parse(cls, html: str) -> ShodanSearchResult:
        results = []

        for entry in cls._get_entries(html):
            results.append(ShodanResult(
                ip=cls._get_ip_from_entry(entry)
            ))

        return ShodanSearchResult(total=cls._get_total(html), results=results)

    @staticmethod
    def _get_ip_from_entry(entry: Tag) -> str:
        return entry.find("li", {'class': HOSTNAME_CLASS}).text

    @staticmethod
    def _get_entries(html: str) -> List[Tag]:
        return BeautifulSoup(html, 'html.parser').find_all("div", {'class': ENTRY_CLASS})

    @classmethod
    def _get_total(cls, html: str) -> int:
        try:
            return int(BeautifulSoup(html, 'html.parser').find('h4').text.replace(',', ''))
        except ValueError:
            return -1
