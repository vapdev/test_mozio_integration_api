import requests
import time

URL = "https://api-testing.mozio.com/v2/"

HEADERS = {
    "Content-Type": "application/json",
    "API-KEY": "6bd1e15ab9e94bb190074b4209e6b6f9"
}

SEARCH_PARAMS = {
    "start_address": "44 Tehama Street, San Francisco, CA, USA",
    "end_address": "SFO",
    "mode": "one_way",
    "pickup_datetime": "2023-12-01 15:30",
    "num_passengers": 2,
    "currency": "USD",
    "campaign": "Vitor Augusto Philippsen Bohn"
}

PASSENGER = {
    "search_id": "",
    "result_id": "",
    "email": "vitordeveloper@mozio.com",
    "country_code_name": "US",
    "phone_number": "4155552478",
    "first_name": "Vitor",
    "last_name": "Bohn",
    "airline": "AA",
    "flight_number": "577",
    "customer_special_instructions": "Made with love by Vitor Bohn"
}


class MozioApi:
    def __init__(self, url, headers, search_params, search_id=None, result_id=None, search_results=None,
                 reservations=None, reservation_id=None):
        self.result_id = result_id
        self.search_id = search_id
        self.url = url
        self.headers = headers
        self.search_params = search_params
        self.search_results = search_results or []
        self.reservations = reservations or []
        self.reservation_id = reservation_id

    def start_search(self):
        response = requests.post(
            self.url + "search/", headers=self.headers, json=self.search_params).json()
        self.search_id = response["search_id"]

    def search_polling(self):
        more_coming = True
        while more_coming:
            response = requests.get(
                self.url + "search/" + self.search_id + "/poll", headers=self.headers).json()
            self.search_results.extend(response["results"])
            if not response["more_coming"]:
                more_coming = False
                if len(response["results"]) > 0:
                    self.result_id = response["results"][0]["result_id"]
            else:
                time.sleep(2)  # Wait for 2 seconds before polling again

    def start_reservation(self):
        PASSENGER["search_id"] = self.search_id
        PASSENGER["result_id"] = self.result_id
        requests.post(self.url + "reservations/",
                      headers=self.headers, json=PASSENGER).json()

    def reservation_polling(self):
        pending = True
        while pending:
            response = requests.get(self.url + "reservations/" + self.search_id + "/poll", headers=self.headers,
                                    json=PASSENGER).json()
            self.reservations.extend(response["reservations"])
            if response["status"] == "completed":
                pending = False
            else:
                time.sleep(2)
        self.reservation_id = self.reservations[0]["id"]

    def get_provider(self):
        dummy_results = [obj for obj in self.search_results if obj["steps"]
                         [0]["details"]["provider_name"] == "Dummy External Provider"]
        self.result_id = self.get_result_id_from_cheapest_vehicle(
            dummy_results)

    @staticmethod
    def get_result_id_from_cheapest_vehicle(dummy_results):
        cheapest = min(dummy_results, key=lambda x: float(
            x["total_price"]["total_price"]["value"]))
        return cheapest["result_id"]

    def cancel_reservation(self):
        requests.delete(self.url + "reservations/" +
                        self.reservation_id + "/", headers=self.headers).json()


def main():
    mozio = MozioApi(URL, HEADERS, SEARCH_PARAMS)
    mozio.start_search()
    mozio.search_polling()
    mozio.start_reservation()
    mozio.get_provider()
    mozio.reservation_polling()
    mozio.cancel_reservation()


if __name__ == "__main__":
    main()
