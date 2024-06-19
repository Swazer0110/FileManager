# FileManager - Miguel Álvarez

## Instrucciones para iniciar un entorno virtual (venv) en python 

    1. Abre una terminal o línea de comandos.
    2. Navega al directorio del proyecto: cd path/to/your/project
    3. Crea un entorno virtual:    python -m venv venv
    4. Activa el entorno virtual:
        - En Windows:  Primero necesitas activar la politica de ejecución en powershell: Set-ExecutionPolicy RemoteSigned 
                       .\venv\Scripts\activate
        - En macOS y Linux:  source venv/bin/activate

## Instalación de dependencias
    
    pip install -r requirements.txt

## Iniciar aplicación:

    python main.py

    Dentro de main.py se encuentran todas las configuraciones del servidor:

        SECRET_KEY                              
        SQLALCHEMY_DATABASE_URI                 
        UPLOAD_FOLDER = 'uploads'               # Nombre de la carpeta a la que se suben los ficheros
        MAX_FILES = 10                          # Maximos numero de ficheros que subir a la vez
        MAX_BYTES = 100 * 1024 * 1024           # Maximo tamaño de los ficheros que se quieren subir (100*1024*1024 = 100 MB) 
        DEBUG = True                            # Activar modo debug de Flask
        NEW_DB = False                          # Crear nueva base de datos y borrar archivos de la carpeta de subida

    La aplicación está configurada para crear un usuario CEO con contraseña ´%VsL&J9&9NLa$P^´ por defecto

    El servidor se abre en local en http://127.0.0.1:5000/