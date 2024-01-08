from modules.shodan.shodan_parser import ShodanParser, ShodanSearchResult
from modules.shodan.shodan_signup import ShodanSignup

QUERIES_PER_ACCOUNT = 20
SEARCH_URL = "https://www.shodan.io/search"
NO_RESULTS = "No results found"


class Shodan:

    def __init__(self) -> None:
        self._get_new_shodan_account()

    def search(self, query: str) -> ShodanSearchResult:
        results = self._search(query)
        self._handle_increase_search_counter()

        return results

    def _search(self, query: str) -> ShodanSearchResult:
        html = self._session.get(SEARCH_URL, params={"query": query}).text

        if NO_RESULTS in html:
            return ShodanSearchResult()

        return ShodanParser.parse(html)

    def _handle_increase_search_counter(self) -> None:
        self._counter += 1

        if self._counter == QUERIES_PER_ACCOUNT:
            self._get_new_shodan_account()

    def _get_new_shodan_account(self) -> None:
        self._counter = 0
        self._session = ShodanSignup().register_new_account()
