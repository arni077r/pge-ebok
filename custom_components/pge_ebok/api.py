import logging
import aiohttp
from .const import DOMAIN, LOGIN_URL, INDEX_URL, FINANSE_URL

from .parsers.index_parser import parse_index_page
from .parsers.finanse_parser import parse_finanse_page

_LOGGER = logging.getLogger(__name__)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive'
}

class PGEEbokAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None

    async def login(self) -> bool:
        client_timeout = aiohttp.ClientTimeout(total=15)
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=client_timeout)

        try:
            async with self.session.get(LOGIN_URL, headers=HEADERS) as response:
                if response.status != 200:
                    _LOGGER.error("Strona logowania PGE zwróciła status: %s", response.status)
                    return False
                html = await response.text()

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            view_state_element = soup.find('input', {'name': 'javax.faces.ViewState'})
            if not view_state_element:
                _LOGGER.error("Nie znaleziono tokenu ViewState na stronie logowania PGE")
                return False
            
            view_state = view_state_element['value']

            payload = {
                'hiddenLoginForm': 'hiddenLoginForm',
                'hiddenLoginForm:hiddenLogin': self.username,
                'hiddenLoginForm:hiddenPassword': self.password,
                'hiddenLoginForm:loginButton': '',
                'javax.faces.ViewState': view_state
            }
            
            post_headers = HEADERS.copy()
            post_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            post_headers['Referer'] = LOGIN_URL

            async with self.session.post(LOGIN_URL, data=payload, headers=post_headers, allow_redirects=False) as response:
                if response.status in [301, 302, 303]:
                    return True
                
                res_text = await response.text()
                if "hiddenLoginForm:loginButton" in res_text:
                    _LOGGER.error("Błąd logowania PGE: Niepoprawny login lub hasło")
                    return False
                return True
                
        except Exception as e:
            _LOGGER.error("Błąd połączenia z PGE podczas logowania: %s", e)
            return False

    async def fetch_data(self) -> dict:
        """Pobiera surowy kod HTML ze stron PGE i deleguje go do odpowiednich parserów."""
        if not await self.login():
            raise Exception("Nie udało się zalogować do PGE")

        # Bazowa struktura danych przekazywana do Home Assistanta
        data = {
            "account_id": "PGE eBOK",
            "saldo_index": None,
            "termin_za_dni": None,
            "powiadomienia_liczba": 0,
            "w_sumie_finanse": None,
            "dokumenty_liczba": None
        }

        try:
            # --- 1. STRONA GŁÓWNA ---
            async with self.session.get(INDEX_URL, headers=HEADERS) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    # Wywołanie zewnętrznego parsera dla strony głównej
                    data = parse_index_page(html, data)

            # --- 2. STRONA FINANSE ---
            async with self.session.get(FINANSE_URL, headers=HEADERS) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    # Wywołanie zewnętrznego parsera dla strony finansów
                    data = parse_finanse_page(html, data)

            return data

        except Exception as e:
            _LOGGER.error("Błąd podczas pobierania lub parsowania danych z PGE: %s", e)
            raise e
        finally:
            if self.session:
                await self.session.close()