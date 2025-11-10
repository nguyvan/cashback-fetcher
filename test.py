from utils import get_cashback, get_euro_rate
from datetime import datetime
def job():
    # Example usage of the utility functions
    euro_data = get_euro_rate()
    marionnaud = get_cashback("marionnaud")
    sephora = get_cashback("sephora")
    lacoste = get_cashback("lacoste")
    zalando_prive = get_cashback("zalando-prive")
    nocibe = get_cashback("nocibe")
    updated_date = datetime.today().strftime('%d-%m-%Y')

    print(f"Euro Rate: {euro_data['rate']}")
    print(f"Marionnaud Cashback: {marionnaud['cashback']} on {marionnaud['platform']}")
    print(f"Sephora Cashback: {sephora['cashback']} on {sephora['platform']}")
    print(f"Lacoste Cashback: {lacoste['cashback']} on {lacoste['platform']}")
    print(f"Zalando Prive Cashback: {zalando_prive['cashback']} on {zalando_prive['platform']}")
    print(f"Nocibe Cashback: {nocibe['cashback']} on {nocibe['platform']}")
    print(f"Data updated on: {updated_date}")

if __name__ == "__main__":

    job()