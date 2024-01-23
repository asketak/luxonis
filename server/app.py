from flask import Flask
from views import index  
from models import db
import os


app = Flask(__name__)
db_user = os.environ.get('POSTGRES_USER', 'myuser')
db_password = os.environ.get('POSTGRES_PASSWORD', 'mypassword')
db_host = os.environ.get('POSTGRES_HOST', 'postgres')
db_port = os.environ.get('POSTGRES_PORT', '5432')
db_name = os.environ.get('POSTGRES_DB', 'mydatabase')

# Construct the database URI using environment variables
db_uri = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
print(db_uri)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@127.0.0.1:5432/mydatabase'
app.register_blueprint(index)
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
