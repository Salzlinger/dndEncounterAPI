# Readme

## Explanation of the Structure

    app/: Directory for your Flask application code.
        __init__.py: Initializes the Flask application.
        routes.py: Defines the routes/endpoints of your application.
        templates/: Directory for HTML templates (even though you're dealing with PDFs, templates might be useful).
        static/: Directory for static files like CSS and JavaScript.
    instance/: Configuration files specific to the instance of the application (e.g., database configuration).
        config.py: Configuration settings (optional, depending on your needs).
    venv/: Virtual environment directory.
    tests/: Directory for unit tests.
        __init__.py: Makes the directory a Python package.
        test_routes.py: Test cases for your routes.
    .gitignore: Git ignore file to exclude unnecessary files from version control.
    config.py: Configuration settings.
    requirements.txt: List of dependencies.
    run.py: The script to run the application.

## Setup:

´´´
pip install -r requirements.txt
´´´

´´´ cmd
venv\Scripts\activate
´´´

´´´ bash
source venv/Scripts/activate
´´´

## Running:

### Setting Env Vars

´´´´ cmd
set SECRET_KEY=your_secret_key
set DATABASE_URI=your_database_uri
´´´

´´´ bash
export SECRET_KEY=your_secret_key
export DATABASE_URI=your_database_uri

´´´

´´´
python run.py
´´´

### Run Tests

´´´´
python -m unittest discover -s tests
´´´

## Request example

´´´ bash
curl -X POST http://127.0.0.1:5000/api/generate-pdf \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "age": 30}' \
-o output.pdf
´´´

´´´ bash
curl -X POST http://127.0.0.1:5000/api/confirm-monster \
-H "Content-Type: application/json" \
-d '{
"name": "Ancient Red Dragon",
"type": "Dragon",
"alignment": "Chaotic Evil",
"armor_class": 22,
"hit_points": 546,
"hit_dice": "28d12+252",
"speed": {
"walk": 40,
"fly": 80,
"swim": 40
},
"ability_scores": {
"strength": 30,
"dexterity": 10,
"constitution": 29,
"intelligence": 18,
"wisdom": 15,
"charisma": 23
},
"challenge_rating": 24
}' \
-o output.pdf
´´´
