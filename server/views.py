from flask import Blueprint, render_template
from models import db, Title, Image, title_images  # Import the SQLAlchemy objects

index = Blueprint('index', __name__)

@index.route('/')
def home():
    # Query the database to join titles with images
    # titles_with_images = db.session.query(Title, Image).join(title_images).all()
    titles_with_images = db.session.query(Title, Image).select_from(Title).join(title_images)

    # Create a dictionary to organize the data by title
    titles_data = {}
    for title, image in titles_with_images:
        if title.id not in titles_data:
            titles_data[title.id] = {'title_name': title.title_name, 'images': []}
        titles_data[title.id]['images'].append(image)

    return render_template('index.html', titles_data=titles_data)



