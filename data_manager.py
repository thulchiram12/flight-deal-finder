from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "TPE"

datamanager = DataManager()
sheet_data = datamanager.get_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# if needs to add new account
# data_manager.add_new_account()

tomorrow = datetime.today() + timedelta(days=1)
six_month_from_today = datetime.today() + timedelta(days=(6 * 30))


for destination in sheet_data:
    if destination['iataCode'] == '':
        flight_search.fill_iata_code(destination['id'], destination['city'])

    flight = flight_search.check_flight(
        origin_city_iata=ORIGIN_CITY_IATA,
        destination_iata=destination['iataCode'],
        date_from=tomorrow,
        date_to=six_month_from_today)

    if flight == None:
        continue

    if flight.price <= destination['lowestPrice']:
        msg = f"Low price alert! Only NTD {flight.price} to fly from {flight.departure_city}-" \
               f"{flight.departure_airport_code} to {flight.arrival_city}-" \
               f"{flight.arrival_airport_code}, from {flight.departure_date} to " \
               f"{flight.arrival_date}."

        if flight.via_city != "":
            msg += f"Flight has 1 stop over, via {flight.via_city}"

        link = f"{flight.deep_link}"

        notification_manager.send_alert(message=msg, link=link)
