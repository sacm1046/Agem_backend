import os
from flask import Flask, render_template, jsonify, request, Blueprint, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, get_jwt_identity
from datetime import timedelta
from models import db, Worker, Product, Client, Reservation, ROperation, MOperation 
from routes.workers import worker_route
from routes.clients import client_route
from routes.moperations import moperation_route
from routes.roperations import roperation_route
from routes.reservations import reservation_route
from routes.products import product_route
from routes.email import email_route

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#JWT configuration
app.config['JWT_SECRET_KEY'] = 'super-secrets'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1000)
#Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
#'cucvzvrozvacrcpc' 'cm.seb90@gmail.com'
#Forget Password configuration
app.config['SECRET_KEY'] = 'my_precious'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'

jwt = JWTManager(app)
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
CORS(app)

@app.route('/')
def home():
    print(app.config['MAIL_PASS'])
    return render_template('index.html', name = 'home')

app.register_blueprint(worker_route)
app.register_blueprint(client_route)
app.register_blueprint(moperation_route)
app.register_blueprint(roperation_route)
app.register_blueprint(reservation_route)
app.register_blueprint(product_route)
app.register_blueprint(email_route)

if __name__ == '__main__':
    manager.run()