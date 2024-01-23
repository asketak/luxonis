from flask_sqlalchemy import SQLAlchemy

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
