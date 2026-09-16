import os
import requests
from dotenv import load_dotenv
import airportsdata
import pycountry

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
AVIATIONSTACK_URL = "https://api.aviationstack.com/v1/flights"

_airports = airportsdata.load("IATA")

COUNTRY_MAIN_AIRPORT = {
    "BD": "DAC",   # Bangladesh - Dhaka
    "IN": "DEL",   # India - Delhi
    "JP": "NRT",   # Japan - Narita
    "US": "JFK",   # United States - New York
    "GB": "LHR",   # United Kingdom - London Heathrow
    "AE": "DXB",   # United Arab Emirates - Dubai
    "SG": "SIN",   # Singapore - Changi
    "MY": "KUL",   # Malaysia - Kuala Lumpur
    "TH": "BKK",   # Thailand - Bangkok
    "ID": "CGK",   # Indonesia - Jakarta
    "CN": "PEK",   # China - Beijing
    "KR": "ICN",   # South Korea - Incheon
    "NP": "KTM",   # Nepal - Kathmandu
    "QA": "DOH",   # Qatar - Doha
    "SA": "JED",   # Saudi Arabia - Jeddah
    "TR": "IST",   # Türkiye - Istanbul
    "CA": "YYZ",   # Canada - Toronto
    "AU": "SYD",   # Australia - Sydney
    "EG": "CAI",   # Egypt - Cairo
}

CITY_MAIN_AIRPORT = {
    "Dhaka": "DAC",
    "Delhi": "DEL",
    "Tokyo": "NRT",
    "New York": "JFK",
    "London": "LHR",
    "Dubai": "DXB",
    "Singapore": "SIN",
    "Kuala Lumpur": "KUL",
    "Bangkok": "BKK",
    "Jakarta": "CGK",
    "Beijing": "PEK",
    "Seoul": "ICN",
    "Kathmandu": "KTM",
    "Doha": "DOH",
    "Jeddah": "JED",
    "Istanbul": "IST",
    "Toronto": "YYZ",
    "Sydney": "SYD",
    "Cairo": "CAI",
}


def _resolve_airport_code(place: str) -> str | None:
    """Resolve a city name, country name/code, or IATA code to an IATA code."""
    place = place.strip()

    # Already an IATA code
    if len(place) == 3 and place.upper() in _airports:
        return place.upper()

    # City name
    for city, airport_code in CITY_MAIN_AIRPORT.items():
        if city.lower() == place.lower():
            return airport_code

    # Country name -> ISO code -> main airport
    try:
        country = pycountry.countries.lookup(place)
        if country.alpha_2 in COUNTRY_MAIN_AIRPORT:
            return COUNTRY_MAIN_AIRPORT[country.alpha_2]
    except LookupError:
        pass

    # Direct country code
    if place.upper() in COUNTRY_MAIN_AIRPORT:
        return COUNTRY_MAIN_AIRPORT[place.upper()]

    return None


def get_flights(source: str, destination: str) -> list[dict]:
    """
    Take a source and destination (each a city name, country name, or
    IATA code) and return the flights going from source to destination.
    """
    source_code = _resolve_airport_code(source)
    if not source_code:
        raise ValueError(f"Could not resolve an airport for source '{source}'")

    dest_code = _resolve_airport_code(destination)
    if not dest_code:
        raise ValueError(f"Could not resolve an airport for destination '{destination}'")

    response = requests.get(
        AVIATIONSTACK_URL,
        params={
            "access_key": AVIATIONSTACK_API_KEY,
            "dep_iata": source_code,
            "arr_iata": dest_code,
            "limit": 5,
            
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"].get("info", "Unknown API error"))

    flights = []
    for f in data.get("data", []):
        flights.append({
            "airline": f.get("airline", {}).get("name"),
            "flight_number": f.get("flight", {}).get("iata"),
            "status": f.get("flight_status"),
            "departure_airport": f.get("departure", {}).get("airport"),
            "departure_time": f.get("departure", {}).get("scheduled"),
            "arrival_airport": f.get("arrival", {}).get("airport"),
            "arrival_time": f.get("arrival", {}).get("scheduled"),
        })

    return flights


if __name__ == "__main__":
    print(get_flights("Egypt", "London"))