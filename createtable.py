#RUN THIS ONLY ONCE TO CREATE TABLE IN DATABASE BEFORE RUNNING THE main.py, IF YOU RUN THIS AGAIN ALL THE DATA IN
#THE DATABASE WILL BE GONE

from main import app, db

with app.app_context():
    db.create_all()
