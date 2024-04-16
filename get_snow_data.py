import requests

headers = {
	"X-RapidAPI-Key": "ce76d5a1b4msh8fb38a44ed05901p1c72d0jsn6c01ab4d8054",
	"X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
}


def get_snow_data(resort_name, headers):
    querystring = {"units":"i"}
    url = f"https://ski-resort-forecast.p.rapidapi.com/{resort_name}/snowConditions"
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

