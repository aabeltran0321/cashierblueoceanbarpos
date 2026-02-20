import requests

url = "https://api.cloudbeds.com/api/v1.3/getReservations"

headers = {
    "accept": "application/json",
    "x-api-key": "cbat_ytHoA2RACmuxpTP9TcdSJdPUS4JjreuN"
}

response = requests.get(url, headers=headers)

print(response.text)