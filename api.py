import requests

def recipe_api(recipe_name):
    url = "https://www.themealdb.com/api/json/v1/1/search.php"

    response = requests.get(url, params={"s": recipe_name})
    return response.json()


