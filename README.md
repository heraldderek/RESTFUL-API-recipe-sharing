# RECIPE SHARING PLATFORM API

A RESTful API using Python that allows users to share, rate, and comment on recipes. The data should be stored in an MSSQL database, and the entire application should be containerized using Docker.


## Contents
**main.py** - a Flask web application that serves as a Recipe Sharing Platform. It allows users to perform various actions related to recipes, including creating, viewing, updating, and deleting recipes. Users can also rate recipes and leave comments. Additionally, there are search functionalities to find recipes by name or ingredient. Running this will start the server

**createtable.py** - create necessary tables where the data will be stored

**testing.py** - set of functions to interact with a Flask-based Recipe Management API.
You can use these functions to perform various actions such as adding, updating, and deleting recipes,
rating recipes, adding comments, and searching for recipes by name or ingredient.

**unittests.py** - These unit tests cover various functionalities of the Recipe Management API, including creating, retrieving, updating, and deleting recipes,
rating recipes, adding comments, and searching for recipes by name or ingredient.
NOTE:RUNNING THIS UNIT TEST WILL DELETE ALL TABLES, THUS YOU HAVE TO RUN THE createtable.py AGAIN CREATING NEW TABLES

**requirements.txt** - specifies the Python packages required for this project. 

**Dockerfile** - This file defines the Docker image for the Python-based Flask web application

**docker-compose.yml** - Defines the Docker Compose configuration for this project.This configuration enables to run both the Flask API and the SQL Server database as separate Docker services, ensuring that they can communicate with each other. 


## Instructions

1.run "createtable.py"
2.run "main.py"
3.test the functionalities of RECIPE SHARING PLATFORM API by running the functions from "testing.py" for ex: add a recipe,delete a recipe,etc,...
4.Open a terminal at python and run "docker-compose up --build"
