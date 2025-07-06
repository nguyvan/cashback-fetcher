from flask import Flask, jsonify
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

app = Flask(__name__)
hdr = {'User-Agent': 'Mozilla/5.0'}

def getSoupParser(url: str):
    req = Request(url=url, headers=hdr)
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

def parseCashback(cashback: str):
    return float(str(cashback).replace("%","").replace(",","."))

def getCashbackEbuyclub() -> float:
    url = "https://www.ebuyclub.com/reduction-marionnaud-522"
    soup = getSoupParser(url)

    content_container = soup.find("form", id="fake-reload")
    content = content_container.find("strong")
    cashback = parseCashback(str(content.text))
    return cashback

def getCashbackPoulpeo() -> float:
    url = "https://www.poulpeo.com/reductions-marionnaud.htm"
    soup = getSoupParser(url)

    content_container = soup.find_all("div", class_="m-offer__sidebar")
    contents = content_container[2].find_all("div", class_="m-offer__colored")
    cashback = parseCashback(str(contents[0].text))
    return cashback

def getCashbackIgraal() -> float:
    url = "https://fr.igraal.com/codes-promo/Marionnaud/bon-de-reduction"
    soup = getSoupParser(url)
    
    content_container = soup.find_all("span", class_="cashback_rate")
    content = content_container[0]
    cashback = parseCashback(str(content.text))
    return cashback

def getCashbackWidilo() -> float:
    url = "https://www.widilo.fr/code-promo/marionnaud"
    soup = getSoupParser(url)

    content_container = soup.find_all("span", class_="btn-badge")
    content_cashback = content_container[0]
    content_cashback_giftcard = content_container[1]
    cashback = parseCashback(str(content_cashback.text)) + parseCashback(str(content_cashback_giftcard.text))
    return cashback

@app.route("/")
def main():
    # Except Widilo, all others platform has affiliate offer: 10% cashback of cashback gained
    cashbackEbuyclub = getCashbackEbuyclub() * 1.1 + 10
    cashbackWidilo = getCashbackWidilo()
    cashbackIgraal = getCashbackIgraal() * 1.1 + 10
    cashbackPoulpeo = getCashbackPoulpeo() * 1.1 + 10

    cashbacks = [cashbackEbuyclub, cashbackWidilo, cashbackIgraal, cashbackPoulpeo]

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

    return jsonify({
        "cashback": cashbackFinal,
        "plateform": plateformStr
    })

    