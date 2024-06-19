from flask import Blueprint

file_manager = Blueprint('file_manager', __name__)

from FileManager.file_manager import routes