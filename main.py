
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from sqlalchemy import func

db = SQLAlchemy()

#Create Class for Recipe
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(1000), nullable=False)
    steps = db.Column(db.String(2000), nullable=False)
    preparation_time = db.Column(db.Integer, nullable=False)
    ratings = db.relationship('Rating', backref='recipe', lazy=True)
    comments = db.relationship('Comment', backref='recipe', lazy=True)

#Create Class for Rating
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

#Create Class for Comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server&server=MSI\\Herald@localhost&database=practice1'

db.init_app(app)

#Create homepage
@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to the Recipe Sharing Platform Homepage!"

# Create a new recipe
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.json
    new_recipe = Recipe(
        name=data['name'],
        ingredients=data['ingredients'],
        steps=data['steps'],
        preparation_time=data['preparation_time']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "Recipe created successfully"}), 201

# Retrieve a list of all recipes, sorted by most recent
@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.order_by(Recipe.id.desc()).all()
    recipe_list = []
    for recipe in recipes:
        num_ratings = db.session.query(func.count(Rating.id)).filter_by(recipe_id=recipe.id).scalar()
        num_comments = db.session.query(func.count(Comment.id)).filter_by(recipe_id=recipe.id).scalar()
        recipe_list.append({
            "id": recipe.id,
            "name": recipe.name,
            "ingredients": recipe.ingredients,
            "preparation_time": recipe.preparation_time,
            "steps": recipe.steps,
            "num_ratings": num_ratings,
            "num_comments": num_comments
        })
    return jsonify(recipe_list)

# Retrieve details of a specific recipe by its ID
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    num_ratings = db.session.query(func.count(Rating.id)).filter_by(recipe_id=recipe.id).scalar()
    num_comments = db.session.query(func.count(Comment.id)).filter_by(recipe_id=recipe.id).scalar()
    return jsonify({
        "id": recipe.id,
        "name": recipe.name,
        "ingredients": recipe.ingredients,
        "preparation_time": recipe.preparation_time,
        "steps": recipe.steps,
        "num_ratings": num_ratings,
        "num_comments": num_comments
    })

# Update a specific recipe by its ID
@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.json
    recipe.name = data['name']
    recipe.ingredients = data['ingredients']
    recipe.steps = data['steps']
    recipe.preparation_time = data['preparation_time']
    db.session.commit()
    return jsonify({"message": "Recipe updated successfully"})

# Delete a specific recipe by its ID
@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"})

# Rate a specific recipe
@app.route('/recipes/<int:id>/ratings', methods=['POST'])
def rate_recipe(id):
    data = request.json
    if 'value' not in data or not isinstance(data['value'], int) or data['value'] < 1 or data['value'] > 5:
        return jsonify({"error": "Invalid rating value. It should be an integer between 1 and 5"}), 400
    recipe = Recipe.query.get_or_404(id)
    new_rating = Rating(value=data['value'], recipe_id=id)
    db.session.add(new_rating)
    db.session.commit()
    return jsonify({"message": "Rating added successfully"}), 201

# Retrieve ratings for a specific recipe
@app.route('/recipes/<int:id>/ratings', methods=['GET'])
def get_ratings_for_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    ratings = Rating.query.filter_by(recipe_id=id).all()
    rating_list = [{"id": rating.id, "value": rating.value} for rating in ratings]
    return jsonify(rating_list)

# Comment on a specific recipe
@app.route('/recipes/<int:id>/comments', methods=['POST'])
def comment_recipe(id):
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "Comment text is required"}), 400
    recipe = Recipe.query.get_or_404(id)
    new_comment = Comment(text=data['text'], recipe_id=id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully"}), 201

# Retrieve all comments for a specific recipe
@app.route('/recipes/<int:id>/comments', methods=['GET'])
def get_comments_for_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    comments = recipe.comments
    comment_list = [{"id": comment.id, "text": comment.text} for comment in comments]
    return jsonify(comment_list)


# Search recipes by name
@app.route('/recipes/search', methods=['GET'])
def search_recipes_by_name():
    query = request.args.get('name', '').lower()

    if not query:
        return jsonify({"error": "Name parameter is required"}), 400

    recipes = Recipe.query.filter(Recipe.name.ilike(f"%{query}%")).all()

    if not recipes:
        return jsonify({"message": "No matching recipes found"})

    result = [{
        "id": recipe.id,
        "name": recipe.name,
        "ingredients": recipe.ingredients,
        "preparation_time": recipe.preparation_time,
        "steps": recipe.steps,
        "num_ratings": len(recipe.ratings),
        "num_comments": len(recipe.comments)
    } for recipe in recipes]

    return jsonify(result)


# Search recipes by ingredient
@app.route('/recipes/searchByIngredient', methods=['GET'])
def search_recipes_by_ingredient():
    query = request.args.get('ingredient', '').lower()

    if not query:
        return jsonify({"error": "Ingredient parameter is required"}), 400

    # Modify the query to search for recipes by ingredients
    recipes = Recipe.query.filter(Recipe.ingredients.ilike(f"%{query}%")).all()

    if not recipes:
        return jsonify({"message": "No matching recipes found"})

    result = [{
        "id": recipe.id,
        "name": recipe.name,
        "ingredients": recipe.ingredients,
        "preparation_time": recipe.preparation_time,
        "steps": recipe.steps,
        "num_ratings": len(recipe.ratings),
        "num_comments": len(recipe.comments)
    } for recipe in recipes]

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
