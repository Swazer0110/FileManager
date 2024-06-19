from flask import Blueprint

auth = Blueprint('auth', __name__)

from FileManager.auth import routes
