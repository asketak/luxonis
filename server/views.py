import base64
from flask import Blueprint, render_template
from models import db, Title, Image, title_images  # Import the SQLAlchemy objects


index = Blueprint('index', __name__)

@index.route('/')
def home():
    # titles_with_images = db.session.query(Title, Image).join(title_images).all()
    # titles_with_images = db.session.query(Title, Image).select_from(Title).join(title_images)
    titles_with_images = db.session.query(Title, Image).join(title_images, Title.id == title_images.c.title_id).all()


    titles_data = {}
    for title, image in titles_with_images:
        if title.id not in titles_data:
            titles_data[title.id] = {'title_name': title.title_name, 'images': []}

        # Encode the image data in Base64
        image_data_base64 = base64.b64encode(image.image_data).decode('utf-8')
        
        titles_data[title.id]['images'].append({'data': image_data_base64})

    return render_template('index.html', titles_data=titles_data)



