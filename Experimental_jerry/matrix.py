import requests


origins = [{"lat": 12.91345, "lng" : 77.57498}, {"lat" : 12.94022, "lng": 77.53995}]
destinations = [{"lat": 12.89963, "lng" : 77.64903}, {"lat" : 12.9319, "lng": 77.60736}]


payload = { "origins": origins,
            "destinations": destinations,
            "metrics": ["duration"],
            "mode": "fastest;car;traffic:disabled"
            }

url = "https://matrix.router.hereapi.com/v8/matrix?apiKey=dQaOzawFKqnYhdgInWi9-y7INEOmkILZixoaOZPrNik&async=false"

response = requests.get(url, params = payload)

routes = response.json()