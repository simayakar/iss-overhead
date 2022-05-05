import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 41.008240 # Your latitude
MY_LONG = 28.978359 # Your longitude
MY_EMAIL = "yourmail@gmail.com"
MY_PASSWORD = "yourpassword"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():

        target_mail = "targetmail@gmail.com"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()  # make conn secure!
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=target_mail, msg=f"Subject:Hey you!\n\nLook up, the ISS is above you in the sky :)")


