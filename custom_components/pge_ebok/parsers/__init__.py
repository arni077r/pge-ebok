import re
import logging
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

def parse_index_page(html: str, data: dict) -> dict:
    """Parsowanie danych ze strony głównej (index.xhtml)."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Pobieranie ID klienta (Konto)
    account_id_found = False
    konto_label = soup.find(lambda tag: tag.name in ["label", "span"] and "Konto:" in tag.get_text())
    if konto_label:
        next_val = konto_label.find_next(["label", "span"])
        if next_val:
            data["account_id"] = next_val.get_text(strip=True)
            account_id_found = True

    if not account_id_found:
        for node in soup.find_all(class_=re.compile(r"hello-name")):
            text = node.get_text(strip=True)
            if text and "@" not in text:
                data["account_id"] = text
                break

    # 2. Pobieranie liczby nowych powiadomień
    powiadomienia_node = soup.find(id=re.compile(r"iloscKom$"))
    if powiadomienia_node:
        txt = powiadomienia_node.get_text()
        match = re.search(r"(\d+)", txt)
        if match:
            data["powiadomienia_liczba"] = int(match.group(1))

    # 3. Parsowanie Salda
    saldo_div = soup.find(id="formNaleznosc:idSaldoNaDzien")
    if not saldo_div:
        saldo_div = soup.find(id=re.compile(r"idSaldoNaDzien"))

    if saldo_div:
        for label in saldo_div.find_all("label"):
            val_text = label.get_text(strip=True).replace("\xa0", "").replace(" ", "").replace(",", ".")
            if re.match(r"^-?\d+\.\d+$|^\d+$", val_text):
                try:
                    data["saldo_index"] = float(val_text)
                    break
                except ValueError:
                    pass

    # 4. Termin za X dni
    for element in soup.find_all(["label", "span", "div"]):
        text_raw = element.get_text()
        if "Termin za" in text_raw:
            match = re.search(r"Termin za\s*(\d+)", text_raw)
            if match:
                data["termin_za_dni"] = int(match.group(1))
                break

    return data