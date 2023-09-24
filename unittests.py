#NOTE: RUNNING THIS UNIT TEST WILL DELETE ALL TABLES, THUS YOU HAVE TO RUN THE createtable.py AGAIN CREATING NEW TABLES
"""
Unit Tests for Recipe Management API

These unit tests cover various functionalities of the Recipe Management API, including creating, retrieving, updating, and deleting recipes,
rating recipes, adding comments, and searching for recipes by name or ingredient.

To run these tests, make sure the Flask application is running, and then execute this script.
"""

import unittest
import json
from main import app, db, Recipe, Rating, Comment

class TestRecipeAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()  # Establish the application context
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # Remove the application context


    def test_create_recipe(self):
        data = {
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'steps': '1. Step 1\n2. Step 2',
            'preparation_time': 45
        }
        response = self.app.post('/recipes', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_all_recipes(self):
        response = self.app.get('/recipes')
        self.assertEqual(response.status_code, 200)

    def test_get_recipe_by_id(self):
        recipe = Recipe(name='Test Recipe', ingredients='Ingredient 1, Ingredient 2', steps='1. Step 1\n2. Step 2', preparation_time=45)
        db.session.add(recipe)
        db.session.commit()

        response = self.app.get(f'/recipes/{recipe.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_recipe(self):
        recipe = Recipe(name='Test Recipe', ingredients='Ingredient 1, Ingredient 2', steps='1. Step 1\n2. Step 2', preparation_time=45)
        db.session.add(recipe)
        db.session.commit()

        data = {
            'name': 'Updated Recipe',
            'ingredients': 'Ingredient 3, Ingredient 4',
            'steps': '1. New Step 1\n2. New Step 2',
            'preparation_time': 30
        }
        response = self.app.put(f'/recipes/{recipe.id}', json=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe(self):
        recipe = Recipe(name='Test Recipe', ingredients='Ingredient 1, Ingredient 2', steps='1. Step 1\n2. Step 2', preparation_time=45)
        db.session.add(recipe)
        db.session.commit()

        response = self.app.delete(f'/recipes/{recipe.id}')
        self.assertEqual(response.status_code, 200)

    def test_rate_recipe(self):
        recipe = Recipe(name='Test Recipe', ingredients='Ingredient 1, Ingredient 2', steps='1. Step 1\n2. Step 2', preparation_time=45)
        db.session.add(recipe)
        db.session.commit()

        data = {'value': 4}
        response = self.app.post(f'/recipes/{recipe.id}/ratings', json=data)
        self.assertEqual(response.status_code, 201)

    def test_comment_recipe(self):
        recipe = Recipe(name='Test Recipe', ingredients='Ingredient 1, Ingredient 2', steps='1. Step 1\n2. Step 2', preparation_time=45)
        db.session.add(recipe)
        db.session.commit()

        data = {'text': 'Test comment'}
        response = self.app.post(f'/recipes/{recipe.id}/comments', json=data)
        self.assertEqual(response.status_code, 201)

    def test_search_recipes_by_name(self):
        recipe1 = Recipe(name='Test Recipe 1', ingredients='Ingredient 1, Ingredient 2', steps='1. Step 1\n2. Step 2', preparation_time=45)
        recipe2 = Recipe(name='Test Recipe 2', ingredients='Ingredient 3, Ingredient 4', steps='1. Step 1\n2. Step 2', preparation_time=30)
        db.session.add_all([recipe1, recipe2])
        db.session.commit()

        response = self.app.get('/recipes/search?name=Test Recipe 1')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Recipe 1')

    def test_search_recipes_by_ingredient(self):
        recipe1 = Recipe(name='Test Recipe 1', ingredients='Ingredient 1, Ingredient 2', steps='1. Step 1\n2. Step 2', preparation_time=45)
        recipe2 = Recipe(name='Test Recipe 2', ingredients='Ingredient 3, Ingredient 4', steps='1. Step 1\n2. Step 2', preparation_time=30)
        db.session.add_all([recipe1, recipe2])
        db.session.commit()

        response = self.app.get('/recipes/searchByIngredient?ingredient=Ingredient 3')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Recipe 2')

if __name__ == '__main__':
    unittest.main()
