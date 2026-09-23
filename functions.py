import os
import pandas as pd
import streamlit as st 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(r"C:\Users\97335\Downloads\dsb3\Projects\llm.env")


def smart_chef(ingredients, restriction):
    #api_key = os.getenv("OPENAI_API_KEY")
    api_key = st.secrets['OPENAI_API_KEY']

    client = OpenAI(api_key=api_key)
    prompt = f"""
Create a simple recipe using these ingredients:
{ingredients}

Dietary restriction:
{restriction}

Give me:
1. Recipe name
2. Ingredients
3. Cooking instructions
"""
    response = client.responses.create( model="gpt-5.6-luna", input=prompt )
    return response.output_text




def add_recipe(recipes, name, ingredients, prep_mins, instructions, difficulty, category, servings, rating, hist):

    prep_hours = prep_mins / 60
    new_recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'ingredients': ingredients,
        'prep_mins': prep_mins,
        'prep_hours': prep_hours,
        'instructions': instructions,
        'difficulty': difficulty,
        'category': category,
        'servings': servings,
        'rating': rating,
        'cooking_history': hist }
    recipes.loc[len(recipes)] = new_recipe
    recipes.to_csv( r"C:\Users\97335\Documents\recipes.csv",index=False )
    return recipes



def search_by_ingredient(recipes, ingredient):
    def find_ing(recipe):
        for i in ingredient:
            if i.lower() in recipe.lower():
                return True
        return False
    result = recipes[recipes['ingredients'].apply(find_ing)]
    return result



def get_all_recipes(recipes):
    result = recipes.sort_values( by=['prep_mins', 'name'], ascending=[True, False] )
    return result



def get_random_recipe(recipes):
    random_recipe = recipes.sample(1)
    return random_recipe



def search_by_category(recipes, category):
    result = recipes[recipes['category'] == category]
    return result


def rate_recipe(recipes, choese, ratings):
    recipes.loc[recipes['name'] == choese, 'rating'] = ratings
    recipes.to_csv( r"C:\Users\97335\Documents\recipes.csv", index=False)
    result = recipes.sort_values( by='rating', ascending=False)
    return result



def shopping_list(recipes, selected_recipes):
    shopping_items = []

    for recipe in selected_recipes:
        selected = recipes[recipes['name'] == recipe]
        if selected.empty:
            continue
        ingredients = selected.iloc[0]['ingredients']
        if pd.isna(ingredients):
            continue
        for ingredient in str(ingredients).split(','):
            ingredient = ingredient.strip()
            if ingredient:
                shopping_items.append(ingredient)
    return shopping_items


def cook_history(recipes):
    result = recipes.sort_values( by='cooking_history', ascending=True )
    return result



