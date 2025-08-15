from flask import Flask, render_template
from datetime import datetime
from database import collection
app = Flask(__name__, static_folder="./templates/assets")

@app.route("/")
def main():
    data = collection.find_one({})
    euro_data = data.get("euro_data", {})
    marionnaud = data.get("marionnaud", {})
    sephora = data.get("sephora", {})
    lacoste = data.get("lacoste", {})
    zalando_prive = data.get("zalando_prive", {})
    nocibe = data.get("nocibe", {})
    updated_date = data.get("updated_date", datetime.today().strftime('%d-%m-%Y'))
    return render_template("index.html", 
                           today=updated_date,
                           euro_buy=euro_data["col1"],
                           euro_sell=euro_data["col3"],
                           euro_rate=euro_data["rate"],
                           cashback_marionnaud=marionnaud["cashback"],
                           platform_marionnaud=marionnaud["platform"],
                           cashback_sephora=sephora["cashback"],
                           platform_sephora=sephora["platform"],
                           cashback_lacoste=lacoste["cashback"],
                           platform_lacoste=lacoste["platform"],
                           cashback_zalando_prive=zalando_prive["cashback"],
                           platform_zalando_prive=zalando_prive["platform"],
                           cashback_nocibe=nocibe["cashback"],
                           platform_nocibe=nocibe["platform"])