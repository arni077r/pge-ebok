import re
import logging
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

def parse_finanse_page(html: str, data: dict) -> dict:
    """Parsowanie danych ze strony finanse.xhtml."""
    soup = BeautifulSoup(html, 'html.parser')
    
    fin_table = soup.find(class_=re.compile(r"balancePanelGrid"))
    if fin_table:
        for label in fin_table.find_all("label"):
            text_clean = label.get_text(strip=True).replace("\xa0", "").replace(" ", "").replace(",", ".")
            
            # Szukamy sumy finansów
            if re.match(r"^\d+,\d+$|^\d+\.\d+$", text_clean) and "zł" not in label.get_text():
                try:
                    data["w_sumie_finanse"] = float(text_clean)
                except ValueError:
                    pass
            
            # Szukamy liczby dokumentów
            text_raw = label.get_text()
            if "dokument" in text_raw:
                match = re.search(r"(\d+)", text_raw)
                if match:
                    data["dokumenty_liczba"] = int(match.group(1))
                    
    return data