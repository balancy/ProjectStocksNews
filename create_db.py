from flaskr import db, create_app

db.create_all(app=create_app())