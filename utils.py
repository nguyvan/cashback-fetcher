from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import xmltodict, json
import requests

hdr = {'User-Agent': 'Mozilla/5.0'}

def format_euro_rate_str(rate: str) -> float:
    return float(rate.replace(",", ""))

def format_cashback_str(cashback: str):
    return float(str(cashback).replace("%","").replace(",","."))

def get_soup_parser(url: str):
    req = Request(url=url, headers=hdr)
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_cashback_ebuyclub(name: str) -> float:
    if name == "marionnaud":
        url_name = "marionnaud-522"
    elif name == "sephora":
        url_name = "sephora-683"
    elif name == "lacoste":
        url_name = "lacoste-3680"
    elif name == "zalando-prive":
        url_name = "prive-by-zalando-9777"
    else:
        url_name = "nocibe-925"
    url = f"https://www.ebuyclub.com/reduction-{url_name}"
    soup = get_soup_parser(url)

    content_container = soup.find("form", id="fake-reload")
    content = content_container.find("strong")
    cashback = format_cashback_str(str(content.text))
    return cashback

def get_cashback_poulpeo(name: str) -> float:
    url = f"https://www.poulpeo.com/reductions-{name}.htm"
    soup = get_soup_parser(url)

    content_container = soup.find_all("div", class_="m-offer__sidebar")
    contents = content_container[1].find_all("div", class_="m-offer__colored")
    cashback = format_cashback_str(str(contents[0].text))
    return cashback

def get_cashback_igraal(name: str) -> float:
    url = f"https://fr.igraal.com/codes-promo/{name}"
    soup = get_soup_parser(url)
    
    content_container = soup.find_all("span", class_="cashback_rate")
    content = content_container[0]
    cashback = format_cashback_str(str(content.text))
    return cashback

def get_cashback_widilo(name: str) -> float:
    url = f"https://www.widilo.fr/code-promo/{name}"
    soup = get_soup_parser(url)

    content_container = soup.find_all("span", class_="btn-badge")
    content_cashback = content_container[0]
    cashback = format_cashback_str(str(content_cashback.text))
    if name == "marionnaud":
        content_cashback_giftcard = content_container[1]
        cashback += format_cashback_str(str(content_cashback_giftcard.text))
    return cashback

def get_cashback(name: str):
    # Except Widilo, all others platform has affiliate offer
    cashback_ebuyclub = get_cashback_ebuyclub(name) * 1.1
    cashback_widilo = get_cashback_widilo(name)
    cashback_igraal = get_cashback_igraal(name) * 1.1
    cashback_poulpeo = get_cashback_poulpeo(name) * 1.

    # 10% cashback of cashback gained (only for Marionnaud and Sephora)
    if (name == "marionnaud" or name == "sephora"):
        cashback_ebuyclub += 10
        cashback_igraal += 10
        cashback_poulpeo += 10

    cashbacks = [cashback_ebuyclub, cashback_widilo, cashback_igraal, cashback_poulpeo]
    cashback_final = max(cashbacks)
    index_max = cashbacks.index(cashback_final)

    platform_str = ""

    if (index_max == 0):
        platform_str = "eBuyclub"
    elif (index_max == 1):
        platform_str = "Widilo"
    elif (index_max == 2):
        platform_str = "iGraal"
    else:
        platform_str = "Poulpeo"

    return {
        "cashback": round(cashback_final, 2),
        "platform": platform_str
    }

def get_euro_rate():
    vcb_api = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx?b=10"
    try:
        res = requests.get(vcb_api, headers=hdr)
        res.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        euro_rate = 0

    res_xml = xmltodict.parse(res.text)
    res_json = json.loads(json.dumps(res_xml))
    exrate_data = res_json["ExrateList"]["Exrate"]
    euro_data = [x for x in exrate_data if x['@CurrencyCode'] == 'EUR']
    if (len(euro_data) > 0):
        euro = euro_data[0]
        euro_buy = format_euro_rate_str(euro["@Buy"])
        euro_sell = format_euro_rate_str(euro["@Sell"])
        euro_rate = round((euro_buy + euro_sell)/2)
    else:
        euro_buy = 0
        euro_sell = 0
        euro_rate = 0
    
    return {
        "col1": euro_buy,
        "col3": euro_sell,
        "rate": euro_rate,
    }
