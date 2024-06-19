from datetime import timedelta
import os
import shutil
import bcrypt
from FileManager import create_app, db
from FileManager.models import User

class Config:
    SECRET_KEY = 'D!!v$P7&2^Zk4tLEFq5injTtq'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    UPLOAD_FOLDER = 'uploads'               # Nombre de la carpeta a la que se suben los ficheros
    MAX_FILES = 10                          # Maximos numero de ficheros que subir a la vez
    MAX_BYTES = 100 * 1024 * 1024           # Maximo tamaño conjunto de los ficheros que se quieren subir (100*1024*1024 = 100 MB) 
    DEBUG = True                            # Activar modo debug de Flask
    NEW_DB = True                          # Crear nueva base de datos y borrar archivos de carpeta de subida
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)     #Timeout de la sesion de usuario
    
app = create_app(Config)

def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        if not os.path.exists(Config.UPLOAD_FOLDER):                    # Crear carpeta de subida si no existe
            os.makedirs(Config.UPLOAD_FOLDER)
        
        for filename in os.listdir(Config.UPLOAD_FOLDER):               # Borrar todos los archivos de la carpeta
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            # Comprobar si existe fichero o symlink
            if os.path.isfile(file_path) or os.path.islink(file_path):  
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
        # Crear usuario CEO
        admin = User(id=1, username='CEO', password_hash=bcrypt.hashpw(b'2*CdG2Aup$nHu5T', bcrypt.gensalt()))
        db.session.add(admin)
        
        db.session.commit()

if __name__ == '__main__':
    if Config.NEW_DB:
        populate_db()
    app.run(debug=Config.DEBUG)
