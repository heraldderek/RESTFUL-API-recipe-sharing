import requests

# Define the base URL of your Flask application
base_url = 'http://127.0.0.1:5000'

#Function to add recipe
def add_recipe(recipe_data):
    # Make a POST request to create the new recipe
    response = requests.post(f'{base_url}/recipes', json=recipe_data)
    # Check the response
    if response.status_code == 201:
        print("Recipe created successfully")
    else:
        print("Failed to create recipe")

#Function to update recipe
def update_recipe(recipe_id, updated_recipe_data):
    # Make a PUT request to update the recipe
    response = requests.put(f'{base_url}/recipes/{recipe_id}', json=updated_recipe_data)

    if response.status_code == 200:
        print("Recipe updated successfully")
    else:
        print("Failed to update recipe")

#Function to delete recipe
def delete_recipe(recipe_id):
    # Make a DELETE request to delete the recipe
    response = requests.delete(f'{base_url}/recipes/{recipe_id}')
    # Check the response
    if response.status_code == 200:
        print("Recipe deleted successfully")
    else:
        print("Failed to delete recipe")

#Function to show all recipe
def get_all_recipes():
    # Make a GET request to retrieve all recipes
    response = requests.get(f'{base_url}/recipes')
    if response.status_code == 200:
        print("Recipes retrieved successfully")
        recipes = response.json()
        for recipe in recipes:
            print(f"Recipe ID: {recipe['id']}")
            print(f"Name: {recipe['name']}")
            print(f"Ingredients: {recipe['ingredients']}")
            print(f"Steps: \n{recipe['steps']}")
            print(f"Preparation Time: {recipe['preparation_time']} minutes")
            print()
    else:
        print("Failed to retrieve recipes")

#Function to rate recipe
def rate_recipe(recipe_id, rating_value):
    # Define the data for rating the recipe
    rate_recipe_data = {
        "value": rating_value
    }

    # Make a POST request to rate the recipe
    response = requests.post(f'{base_url}/recipes/{recipe_id}/ratings', json=rate_recipe_data)

    if response.status_code == 201:
        print("Recipe rated successfully")
    else:
        print("Failed to rate recipe")

#Function to show all ratings for a specific recipe
def get_ratings_for_recipe(recipe_id):
    # Send a GET request to retrieve ratings for the recipe
    response = requests.get(f'{base_url}/recipes/{recipe_id}/ratings')

    if response.status_code == 200:
        ratings = response.json()
        for rating in ratings:
            print(f"Rating ID: {rating['id']}, Value: {rating['value']}")
    else:
        print("Failed to retrieve ratings")

#Function to comment on a recipe
def comment_on_recipe(recipe_id, comment_text):
    # Define the comment data
    comment_data = {
        "text": comment_text
    }

    # Make a POST request to add a comment to the recipe
    response = requests.post(f'{base_url}/recipes/{recipe_id}/comments', json=comment_data)

    if response.status_code == 201:
        print("Comment added successfully")
    else:
        print("Failed to add comment")

#Function to show all comments for a specific recipe
def get_comments_for_recipe(recipe_id):
    # Send a GET request to retrieve comments for the recipe
    response = requests.get(f'{base_url}/recipes/{recipe_id}/comments')

    if response.status_code == 200:
        comments = response.json()
        for comment in comments:
            print(f"Comment ID: {comment['id']}, Text: {comment['text']}")
    else:
        print("Failed to retrieve comments")

#Function to search a recipe by name
def search_recipes_by_name(query):
    # Send a GET request to search recipes by name
    response = requests.get(f'{base_url}/recipes/search', params={'name': query})

    if response.status_code == 200:
        recipes = response.json()
        if isinstance(recipes, list):
            for recipe in recipes:
                print(f"Recipe ID: {recipe['id']}")
                print(f"Name: {recipe['name']}")
                print(f"Ingredients: {recipe['ingredients']}")
                print(f"Preparation Time: {recipe['preparation_time']} minutes")
                print()
        else:
            print("No matching recipes found")
    else:
        print("Failed to retrieve recipes")


# Function to search all recipes by an ingredient
def search_recipes_by_ingredient(query):
    # Send a GET request to search recipes by ingredient
    response = requests.get(f'{base_url}/recipes/searchByIngredient', params={'ingredient': query})

    if response.status_code == 200:
        try:
            recipes = response.json()
            if isinstance(recipes, list):
                for recipe in recipes:
                    print(f"Recipe ID: {recipe['id']}")
                    print(f"Name: {recipe['name']}")
                    print(f"Ingredients: {recipe['ingredients']}")
                    print(f"Preparation Time: {recipe['preparation_time']} minutes")
                    print()
            else:
                print("No matching recipes found")
        except ValueError:
            print("Error parsing JSON: Response is not in valid JSON format")
    else:
        print("Failed to retrieve recipes")



#REMOVE COMMENT/TRIPLE QUOTATION TO USE THE EXAMPLE USAGE OF FUNCTIONS


# Example usage to add a recipe
"""new_recipe_data = {
    "name": "Hotdog Sandwich",
    "ingredients": "Hotdog, bread",
    "steps": "1. Cook hotdog. 2. Put hotdog on bread.",
    "preparation_time": 5
}
add_recipe(new_recipe_data)
"""

# Example usage to update a recipe, update_recipe(id of recipe to change ,updated_recipe)
"""updated_recipe_data = {
     "name": "Updated Recipe Name",
     "ingredients": "Updated Ingredients",
     "steps": "Updated Steps",
     "preparation_time": 30
}
update_recipe(11, updated_recipe_data)  # Update the recipe with ID 11
"""

# Example usage to delete a recipe by its ID
"""recipe_id_to_delete = 11  # Change this to the ID of the recipe you want to delete
delete_recipe(recipe_id_to_delete)"""

# Example usage to get all recipes
#get_all_recipes()

# Example usage to rate a recipe and get its ratings
#rate_recipe(1, 4)  # Rate the recipe with ID 2 with a value of 4

# Example usage to get ratings of recipe
#get_ratings_for_recipe(2)  # Get ratings for the recipe with ID 2

# Example usage to add a comment to a recipe
#comment_on_recipe(3, "This recipe is amazing!")  # Add a comment to the recipe with ID 3

# Example usage to retrieve comments for a recipe
#get_comments_for_recipe(2)  # Retrieve comments for the recipe with ID 2

# Example usage to search recipes by name
#search_recipes_by_name("pizza")    #Retrive recipe with a "pizza" on its name

# Example usage to search recipes by ingredient
#search_recipes_by_ingredient("pepper")





