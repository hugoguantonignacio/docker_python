from flask import Flask
import requests
from datetime import datetime
from urllib.parse import quote_plus

app = Flask(__name__)

# Load API key from file
def load_token():
    try:
        with open("data/token.txt", "r") as f:
            return f.read().strip()
    except:
        return None

# Fetch departures
def get_departures():
    token = load_token()
    if not token:
        return ["Missing API token"]

    # current time in ISO format
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    time_encoded = quote_plus(now)

    url = f"https://api.golemio.cz/v2/pid/departureboards?names=Neratovice%2CKojetick%C3%A1&minutesAfter=180&timeFrom={time_encoded}&limit=5"

    try:
        response = requests.get(url, headers={"x-access-token": token})
        if response.status_code != 200:
            return [f"API error: {response.status_code}"]

        data = response.json()

        departures = []
        for item in data.get("departures", [])[:5]:
            line = item.get("route", {}).get("short_name", "N/A")
            destination = item.get("trip", {}).get("headsign", "N/A")
            departure_time = item.get("departure_timestamp", {}).get("predicted", "N/A")

            departures.append(f"{line} → {destination} at {departure_time}")

        return departures if departures else ["No departures found"]

    except Exception as e:
        return [f"Request failed: {str(e)}"]


@app.route("/")
def index():
    departures = get_departures()
    html = "<h1>Odjezdy:</h1><ul>"

    for d in departures:
        html += f"<li>{d}</li>"

    html += "</ul>"
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)