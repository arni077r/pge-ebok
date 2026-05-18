import re
import json
import logging
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

def parse_zuzycie_page(html: str, data: dict) -> dict:
    """Parsowanie danych o zużyciu z wykresu JavaScript."""
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', id="zuzycieEnergii:wykresForm:wykres_s")
    
    if not script_tag or not script_tag.string:
        return data

    script_text = script_tag.string

    try:
        # 1. Wyciągamy tablice danych zużycia
        data_match = re.search(r'data:\s*(\[\[.*?\]\])', script_text)
        if data_match:
            parsed_data = json.loads(data_match.group(1))
            if len(parsed_data) >= 2:
                if parsed_data[0]:  # Strefa 1 (ostatni element)
                    data["zuzycie_strefa_1"] = float(parsed_data[0][-1])
                if parsed_data[1]:  # Strefa 2 (ostatni element)
                    data["zuzycie_strefa_2"] = float(parsed_data[1][-1])

        # 2. Wyciągamy datę końca okresu z "ticks"
        ticks_match = re.search(r'ticks:\s*(\[.*?\])', script_text)
        if ticks_match:
            clean_ticks = ticks_match.group(1).replace(r'\-', '-')
            parsed_ticks = json.loads(clean_ticks)
            if parsed_ticks:
                date_match = re.search(r'(\d{2}-\d{2}-\d{4})$', parsed_ticks[-1].strip())
                if date_match:
                    data["zuzycie_data_aktualizacji"] = date_match.group(1)

    except Exception as e:
        _LOGGER.error("Błąd podczas parsowania wykresu zużycia PGE: %s", e)

    return data