import requests
import json

url = "https://developers.zomato.com/api/v2.1/search?entity_id=281&entity_type=city&start=1&count=100"
headers = {'user-key': "56f8a64be7b09ee8c81a59edfd692b34", "accept": "application/json"}

response = requests.get(url, headers=headers)

print(response)

# with open('restaurants.json', 'w') as outfile:
#      outfile.write(str(response.content))

# response = requests.get(url).json()
# print(json.dumps(response, indent=4, sort_keys=True))


# with open("restaurants.json", "w") as restaurantFile:
#     json.dump(output, restaurantFile, indent=4, sort_keys=True)