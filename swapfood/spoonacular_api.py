import requests
import os
from PIL import Image

def resize_image(image_path, max_size=(500, 500)):
    """ Resize image before sending to API """
    img = Image.open(image_path)
    img.thumbnail(max_size)
    img.save(image_path)  # Overwrites the existing image

def analyze_food_image(image_path):
    """ Sends the image to Spoonacular API and gets food details """

    # Resize the image before sending
    resize_image(image_path)

    api_key = os.getenv("SPOONACULAR_API_KEY")

    if not api_key:
        return {"error": "API key is missing!"}

    # Step 1: Classify the image (get food name)
    classify_url = "https://api.spoonacular.com/food/images/classify"
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        params = {"apiKey": api_key}

        response = requests.post(classify_url, files=files, params=params)

        if response.status_code != 200:
            return {"error": "Failed to classify image", "status_code": response.status_code, "message": response.text}

    classification_data = response.json()
    food_category = classification_data.get("category", "unknown")

    # Step 2: Get Nutrition Information
    nutrition_url = f"https://api.spoonacular.com/recipes/guessNutrition"
    params = {"title": food_category, "apiKey": api_key}

    nutrition_response = requests.get(nutrition_url, params=params)
    if nutrition_response.status_code != 200:
        return {"error": "Failed to get nutrition data", "status_code": nutrition_response.status_code, "message": nutrition_response.text}

    nutrition_data = nutrition_response.json()

    # Step 3: Estimate Freshness (Assume logic based on category)
    freshness = "Fresh" if food_category.lower() in ["apple", "banana", "carrot"] else "Processed"

    return {
        "food": food_category,
        "probability": classification_data.get("probability"),
        "calories": nutrition_data.get("calories", {}).get("value", "Unknown"),
        "freshness": freshness
    }
