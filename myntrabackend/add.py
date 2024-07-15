

from flask import Flask
from models import db, User, Pin,Board,Product# Import your Flask app instance and models
from datetime import datetime
import os

# Create a function to add data
def add_data():
    # Create a user
    
    # Add 20 pins for the user
    img=[
    "https://i.pinimg.com/originals/93/9c/58/939c58557e8f944b14b47fd80fc9048f.jpg"]
# add.py\
    c=0
    for img_url in img:
        product=Product(id=569,name='Fashion3 Pin',description="this is so good",price=300,image_url=img_url)
        
        c+=1
        db.session.add(product)
        
    db.session.commit()
    print("Data added successfully.")

# Ensure this script is executed only when run directly
if __name__ == '__main__':
    # Create Flask application instance
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set your Flask app configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')  # Replace with your actual database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable SQLAlchemy event system

    # Initialize SQLAlchemy with your Flask app
    db.init_app(app)

    # Use application context to execute the add_data function
    with app.app_context():
        add_data()
    app = Flask(__name__)
    app.config.from_object('config')  # Load your Flask app configuration

    # Initialize SQLAlchemy with your Flask app
    db.init_app(app)

    # Use application context to execute the add_data function
    with app.app_context():
        add_data()
