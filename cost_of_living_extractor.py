
import requests
import json


def extract_cost_of_living(city,country):
    url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"

    querystring = {"city_name":city,"country_name":country}

    headers = {
        "x-rapidapi-key": "ead3bebcd6mshd1508678ed842c7p11adfdjsnead29c4f932a",
        "x-rapidapi-host": "cost-of-living-and-prices.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code != 200:
        return response.status_code
    
    #print(response.json())
    dic = dict()
    dic = response.json()
    
    columns = {'sqrtm_suburbs':1, 'sqrtm_center':2, 'beer':14, 'rent_onebed_suburbs':28, 'rent_onebed_center':29,'rent_threebed_suburbs':30, 'rent_threebed_center':31, 'mcmeal': 36, 'salary_after_tax':40, 'utilities':54}

    city_info = dict()
    city_info["city"] = city
    city_info["country"] = country
    for key, value in columns.items():
        for param in dic["prices"]:
            if param["good_id"] == value:
                city_info[key] = param["avg"]
                
    with open(f'data/cost/{city}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(city_info))  # Convert results to JSON and write to file
    return city_info