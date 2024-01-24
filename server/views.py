import base64
from flask import Blueprint, render_template
from models import db, Title, Image, title_images  # Import the SQLAlchemy objects
from sqlalchemy import text


index = Blueprint('index', __name__)

@index.route('/')
def home():
    # titles_with_images = db.session.query(Title, Image).join(title_images).all()
    # titles_with_images = db.session.query(Title, Image).select_from(Title).join(title_images)
    # titles_with_images = db.session.query(Title, Image).select_from(Title).join(title_images, Title.id == title_images.c.title_id and Image.id == title_images.c.image_id).all()
    titles_with_images = db.session.execute (text("""SELECT titles.id, titles.title_name, images.image_data
FROM titles
JOIN title_images ON titles.id = title_images.title_id
JOIN images ON title_images.image_id = images.id;"""))



    titles_data = {}
    for titleid, title_name, image_data in titles_with_images:
        if titleid not in titles_data:
            titles_data[titleid] = {'title_name': title_name, 'images': []}

        # Encode the image data in Base64
        image_data_base64 = base64.b64encode(image_data).decode('utf-8')
        
        titles_data[titleid]['images'].append({'data': image_data_base64})

    return render_template('index.html', titles_data=titles_data)



