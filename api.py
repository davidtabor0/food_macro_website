from flask import Blueprint, request, jsonify, make_response
import os
import requests

def get_macro_data(food_name):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": os.getenv("API_KEY"),
        "query": food_name,
        "dataType": "Foundation",
        "pageSize": 1
        }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data["foods"]:
            food = data["foods"][0]
            nutrients = food["foodNutrients"]
            result = {
                "description": food["description"],
                "serving_size": "100g excluding refuse",
                "nutrients": []
            }

            for nutrient in nutrients:
                nutrient_name = nutrient["nutrientName"]
                nutrient_value = nutrient["value"]
                unit_name = nutrient["unitName"]
                
                if nutrient_name in ["Total lipid (fat)", "Protein", "Carbohydrate, by difference"]:
                    result["nutrients"].append({
                        "name": nutrient_name,
                        "value": nutrient_value,
                        "unit": unit_name
                    })
            return result
        else:
            return {"error": "Food not found."}
    else:
        return {"error:" f"Error: {response.status_code}"}

api = Blueprint('api_routes', __name__)

@api.route('/search', methods=['GET'])
def search():
    print("data requested!!!")
    query = request.args.get('query')
    result = get_macro_data(query)
    response = make_response(jsonify(result))
    response.headers.add('Access-Control-Allow-Origin', '*')
    #process results?
    return response