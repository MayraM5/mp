import crud
import requests
from model import connect_to_db, db
import os

SPOON_API_KEY = os.environ["SPOON_API_KEY"]

def get_database_recipe(user_id, recipe_id):
    """Retrieve recipe data from database"""

    recipe_data = crud.get_recipe_data(user_id, recipe_id)

    for recipe in recipe_data:
        title = recipe.title
        image = recipe.image
        instructions = recipe.instructions.split('.')
        servings = recipe.servings
        
    recipe_ingredients = crud.get_recipe_ingredients(recipe_id)
    ingredients_list = []
    for ingredient in recipe_ingredients:
        name = ingredient.ingredient_name
        amount = ingredient.amount
        unit = ingredient.units
        
        elements = {'name': name, 'amount' : amount, "unit" : unit}
        ingredients_list.append(elements)

    return { 
        "title": title,
        "instructions": instructions,
        "ingredients": ingredients_list,
        "image": image,
        "servings": servings,
        "ingredients" : ingredients_list,
    }


def get_spoonacular_recipe(recipe_id):

    url = 'https://api.spoonacular.com/recipes/informationBulk?'
    params = {'apiKey' : SPOON_API_KEY,
                'ids' : recipe_id,
                }

    response = requests.get(url, params)
    data = response.json()

    for recipe in data:
        id = recipe["id"]
        title = recipe['title']
        image = recipe["image"]
        servings = recipe["servings"]

        try:
            raw_instructions = recipe["instructions"]

            # if recipe["instructions"] is empty or None, use recipe["summary"]
        except KeyError:
            try:
                raw_instructions = recipe["summary"]
            except KeyError:
                raw_instructions = None
    
        #Remove extra tags
        tags_to_remove = ['<ol>', '</ol>', '</li>', '<span>', '</span>', '<p>', '</p>']
        try:
            for tag in tags_to_remove:
                raw_instructions = raw_instructions.replace(tag, '')
            #Convert in list to display every step in a row
            temp = raw_instructions.split('<li>')
            if len(temp) > 1:
                instructions = temp
            else:
                # Backup method if no <li>
                instructions = raw_instructions.split('.')

            # instructions = raw_instructions.split('<li>')

            for index, instruction in enumerate(instructions):
                if instruction == "":
                    instructions.pop(index)
            
            # for index in range(0, len(instructions)):
            #     if instructions[index] == "":
            #         instructions.pop(index)

        except AttributeError:
            instructions = None

        #Filter ingredients and add to list just what I need now
        ingredients = recipe['extendedIngredients']
        ingredients_list = []
        for item in ingredients:
            name = item['name']
            amount = item['amount']
            unit = item['unit']

            elements = {'name': name, 'amount' : amount, "unit" : unit}
            ingredients_list.append(elements)
        
        return { 
        "title": title,
        "instructions": instructions,
        "ingredients": ingredients_list,
        "image": image,
        "servings": servings,
        "ingredients" : ingredients_list,
    }







if __name__ == '__main__':
    from server import app
    connect_to_db(app, 'mealplanning')
