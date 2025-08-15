from datetime import datetime
import schedule
import time
from utils import get_cashback, get_euro_rate
from database import collection

def job():
    # Example usage of the utility functions
    euro_data = get_euro_rate()
    marionnaud = get_cashback("marionnaud")
    sephora = get_cashback("sephora")
    lacoste = get_cashback("lacoste")
    zalando_prive = get_cashback("zalando-prive")
    nocibe = get_cashback("nocibe")
    updated_date = datetime.today().strftime('%d-%m-%Y')

    # Prepare the data to be inserted into the database
    data = {
        "date": updated_date,
        "euro_data": euro_data,
        "marionnaud": marionnaud,
        "sephora": sephora,
        "lacoste": lacoste,
        "zalando_prive": zalando_prive,
        "nocibe": nocibe
    }

    # Insert the data into the database
    new_document = collection.find_one_and_update({}, {"$set": data}, upsert=True, return_document=True)

    print(f"Data updated in the database: {new_document}")


if __name__ == "__main__":
    # Schedule the job to run every day at a specific time
    print("Scheduling job to run every 3 hours...")
    schedule.every(3).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)