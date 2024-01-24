import scrapy
import json
import time
from scrapy.http import JsonRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from flask_sqlalchemy import SQLAlchemy

# Replace these placeholders with your actual database information
db_user = os.environ.get('POSTGRES_USER', 'myuser')
db_password = os.environ.get('POSTGRES_PASSWORD', 'mypassword')
db_host = os.environ.get('POSTGRES_HOST', '127.0,0,1')
db_port = os.environ.get('POSTGRES_PORT', '5432')
db_name = os.environ.get('POSTGRES_DB', 'mydatabase')

# Construct the database URI using environment variables
db_uri = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
# Create a database engine
db = create_engine(db_uri)

# Create a session factory
Session = sessionmaker(bind=db)

# Create a session instance when you need to interact with the database
session = Session()


db = SQLAlchemy()

class Title(db.Model):
    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    title_name = db.Column(db.String(255), nullable=False)
    
    # Define the relationship with images
    images = db.relationship('Image', secondary='title_images', back_populates='titles')

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.LargeBinary, nullable=False)
    
    # Define the relationship with titles
    titles = db.relationship('Title', secondary='title_images', back_populates='images')

title_images = db.Table('title_images',
    db.Column('title_id', db.Integer, db.ForeignKey('titles.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('images.id'), primary_key=True)
)


class MySpider(scrapy.Spider):
    name = 'my_spider'

    # Define the base URL with query parameters
    base_url = 'https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&noredirect=1&category_type_cb=1&locality_region_id=10&per_page=10&tms='

    def start_requests(self):
        # Generate the current timestamp in milliseconds
        current_timestamp = int(time.time() * 1000)
        
        # Construct the URL with the timestamp
        url = self.base_url + str(current_timestamp)

        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
            data = json.loads(response.text)

            # Process the JSON data
            estates = data["_embedded"]["estates"]

            # Initialize SQLAlchemy session

            for estate in estates:
                title_name = estate["name"]
                image_urls = [image["href"] for image in estate["_links"]["images"]]

                title = Title(title_name=title_name)
                session.add(title)
                session.commit()

                for image_url in image_urls:
                    image_data = download_image(image_url)  # You'll need a function to download the image
                    if image_data:
                        image = Image(image_data=image_data)
                        title.images.append(image)
                        session.add(image)

            # Commit the changes to the database
            session.commit()
            session.close_all()

def download_image(image_url):
    # You can implement a function to download the image data here
    # This function should return the image data as bytes
    # Make sure to handle downloading and error checking appropriately
    # Example: Use requests library to download the image
    import requests

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        return None
