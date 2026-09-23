import streamlit as st 
import pandas as pd
from functions import add_recipe, search_by_ingredient, get_all_recipes, get_random_recipe, search_by_category, rate_recipe, shopping_list,cook_history, smart_chef
from api import recipe_api

st.title('Recipe Manager')

recipes = pd.read_csv(r"C:\Users\97335\Documents\recipes.csv")

option = st.selectbox('What would you like to do?',
                      ['Add a new recipe',
                       'Search by ingredient', 
                       'View all recipes',
                       'Random recipe',
                      'Search by category',
                      'Rate a recipe',
                      'Shopping List',])
    
        
if option == 'Add a new recipe':
    method  = st.radio('How ypu like to add the recipe !', ['Manually','Import from API'])
    if method == "Import from API":
        recipe_name = st.text_input("Enter recipe name:")
        if st.button("Search API"):
            data = recipe_api(recipe_name)
            if data["meals"]:
                meal = data["meals"][0]
                st.subheader(meal["strMeal"])
                st.write("Category:", meal["strCategory"])
                st.write("Instructions:", meal["strInstructions"])
    elif method == 'Manually':
        name = st.text_input('Recipe name')
        ingredients = st.text_input('Ingredients separated by commas')
        prep_mins = st.number_input( 'Preparation min ')
        instructions = st.text_input('Cooking instructions')
        difficulty = st.selectbox('difficulty', ['Easy', 'Medium', 'Hard'])
        category = st.selectbox( 'category', ['Breakfast', 'Lunch', 'Dinner', 'Dessert'])
        servings = st.number_input( 'Number of servings')
        rating = st.number_input("Rating")
        hist = st.number_input( 'cooking history')
        if st.button('Add a new recipe'):
            recipes = add_recipe(recipes, name, ingredients, prep_mins,  instructions, difficulty, category, servings, rating, hist  )
            st.dataframe(recipes)


elif option == 'Search by ingredient':
    ingredient = st.multiselect('Choose your ingredient:',
                                ['chicken', 'pasta','rice', 
                                 'eggs', 'tomato', 'cheese', 'flour'] )
    if ingredient:
           result = search_by_ingredient(recipes, ingredient)
           st.write('Recipes you can make:')
           st.dataframe(result[['name', 'ingredients']])


elif option == 'View all recipes':
    result = get_all_recipes(recipes)
    st.dataframe(result[['name', 'prep_mins']] )


elif option == 'Random recipe':
    random_recipe = get_random_recipe(recipes)
    st.write('Your random recipe is :')
    st.write(random_recipe)


elif option == 'Search by category':
    category = st.selectbox('Choose a category:', ['Breakfast', 'Lunch', 'Dinner', 'Dessert'] )
    result = search_by_category(recipes, category)
    st.dataframe(result[['name', 'instructions', 'ingredients']])


elif option == 'Rate a recipe':
    choese = st.selectbox('chose a recipe: ', recipes['name'])
    ratings = st.number_input('your rating:')
    if st.button('Rate recipe'):
        result = rate_recipe( recipes, choese, ratings)
        st.write('Recipes sorted by rating:')
        st.dataframe( result[['name', 'rating']])


elif option == 'Shopping List':
    select = st.multiselect('Choose recipes:', recipes['name'])
    if st.button('Your Shopping List'):
        shopping_slist = shopping_list(recipes, select)
        st.write('Shopping List:')
        for item in shopping_slist:
            st.write(item)


elif option == 'Cooking History':
    result = cook_history(recipes)
    st.write('Recipes you have not made recently:')
    st.dataframe(result[['name', 'cooking_history']] )



st.title('Use Smart Chef')
ingredients = st.text_input('What ingredients do you have?')
restriction = st.selectbox( 'Dietary restriction',['No restrictions', 'Vegan', 'Vegetarian'])
if st.button("Generate Recipe"):
    if ingredients:
        result = smart_chef( ingredients, restriction )
        st.write(result)
    else:
        st.warning( 'Please enter your ingredients' )


