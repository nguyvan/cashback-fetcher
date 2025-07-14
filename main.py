from flask import Flask, render_template
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import xmltodict, json
import requests
from datetime import datetime

app = Flask(__name__, static_folder='./templates/assets')
hdr = {'User-Agent': 'Mozilla/5.0'}

def formatEuroRateStr(rate: str) -> float:
    return float(rate.replace(",", ""))

def formatCashbackStr(cashback: str):
    return float(str(cashback).replace("%","").replace(",","."))

def getSoupParser(url: str):
    req = Request(url=url, headers=hdr)
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getCashbackEbuyclub(name: str) -> float:
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
    soup = getSoupParser(url)

    content_container = soup.find("form", id="fake-reload")
    content = content_container.find("strong")
    cashback = formatCashbackStr(str(content.text))
    return cashback

def getCashbackPoulpeo(name: str) -> float:
    url = f"https://www.poulpeo.com/reductions-{name}.htm"
    soup = getSoupParser(url)

    content_container = soup.find_all("div", class_="m-offer__sidebar")
    contents = content_container[1].find_all("div", class_="m-offer__colored")
    cashback = formatCashbackStr(str(contents[0].text))
    return cashback

def getCashbackIgraal(name: str) -> float:
    url = f"https://fr.igraal.com/codes-promo/{name}"
    soup = getSoupParser(url)
    
    content_container = soup.find_all("span", class_="cashback_rate")
    content = content_container[0]
    cashback = formatCashbackStr(str(content.text))
    return cashback

def getCashbackWidilo(name: str) -> float:
    url = f"https://www.widilo.fr/code-promo/{name}"
    soup = getSoupParser(url)

    content_container = soup.find_all("span", class_="btn-badge")
    content_cashback = content_container[0]
    cashback = formatCashbackStr(str(content_cashback.text))
    if name == "marionnaud":
        content_cashback_giftcard = content_container[1]
        cashback += formatCashbackStr(str(content_cashback_giftcard.text))
    return cashback

def getCashback(name: str):
    # Except Widilo, all others platform has affiliate offer
    cashbackEbuyclub = getCashbackEbuyclub(name) * 1.1
    cashbackWidilo = getCashbackWidilo(name)
    cashbackIgraal = getCashbackIgraal(name) * 1.1
    cashbackPoulpeo = getCashbackPoulpeo(name) * 1.

    # 10% cashback of cashback gained (only for Marionnaud and Sephora)
    if (name == "marionnaud" or name == "sephora"):
        cashbackEbuyclub += 10
        cashbackIgraal += 10
        cashbackPoulpeo += 10

    cashbacks = [cashbackEbuyclub, cashbackWidilo, cashbackIgraal, cashbackPoulpeo]
    print(cashbacks)
    cashbackFinal = max(cashbacks)
    indexMax = cashbacks.index(cashbackFinal)

    plateformStr = ""
    
    if (indexMax == 0):
        plateformStr = "eBuyclub"
    elif (indexMax == 1):
        plateformStr = "Widilo"
    elif (indexMax == 2):
        plateformStr = "iGraal"
    else:
        plateformStr = "Poulpeo"

    return {
        "cashback": round(cashbackFinal, 2),
        "plateform": plateformStr
    }

def getEuroRate():
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
        euro_buy = formatEuroRateStr(euro["@Buy"])
        euro_sell = formatEuroRateStr(euro["@Sell"])
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

@app.route("/")
def main():
    euro_data = getEuroRate()
    marionnaud = getCashback("marionnaud")
    sephora = getCashback("sephora")
    lacoste = getCashback("lacoste")
    zalando_prive = getCashback("zalando-prive")
    nocibe = getCashback("nocibe")
    updated_date = datetime.today().strftime('%d-%m-%Y')
    return render_template("index.html", 
                           today=updated_date,
                           euro_buy=euro_data["col1"],
                           euro_sell=euro_data["col3"],
                           euro_rate=euro_data["rate"],
                           cashback_marionnaud=marionnaud["cashback"],
                           plateform_marionnaud=marionnaud["plateform"],
                           cashback_sephora=sephora["cashback"],
                           plateform_sephora=sephora["plateform"],
                           cashback_lacoste=lacoste["cashback"],
                           plateform_lacoste=lacoste["plateform"],
                           cashback_zalando_prive=zalando_prive["cashback"],
                           plateform_zalando_prive=zalando_prive["plateform"],
                           cashback_nocibe=nocibe["cashback"],
                           plateform_nocibe=nocibe["plateform"])