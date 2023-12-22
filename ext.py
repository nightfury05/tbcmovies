from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "TXH0NWE6dw6c;@MS~+dKJfWs"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


