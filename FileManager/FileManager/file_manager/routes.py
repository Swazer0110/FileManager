from flask import render_template, redirect, url_for, flash, request, send_file, current_app
from flask_login import login_required
from FileManager import db
from FileManager.file_manager import file_manager
from FileManager.file_manager.forms import UploadForm
from FileManager.models import File
import os
import hashlib
from werkzeug.utils import secure_filename

@file_manager.route('/dashboard')
@login_required
def dashboard():
    form = UploadForm()
    files = File.query.all()
    return render_template('dashboard.html', files=files, form=form)


@file_manager.route('/upload', methods=['POST'])
@login_required
def upload():
    try:
        files = request.files.getlist('files')              
        
        if len(files) > current_app.config['MAX_FILES']:    # Comprobar el numero de ficheros subidos
            flash(f'Limite de archivos superado ({current_app.config["MAX_FILES"]})', 'danger')
            return redirect(url_for('file_manager.dashboard'))
        
        content_length_all = 0                              # Comprobar tamaño conjunto de ficheros subidos
        for file in files:
            if file:
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)
                content_length_all += file_size
        print('CONTENT:' + str(content_length_all))
        if content_length_all >= current_app.config['MAX_BYTES']:
            flash(f'Limite de peso de los archivos superado ({current_app.config["MAX_BYTES"]})', 'danger')
            return redirect(url_for('file_manager.dashboard'))
                
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                filename = filename.replace('_', '-')                 # Sanitizar nombre del archivo 
                
                filepath = os.path.join( current_app.config['UPLOAD_FOLDER'], filename)
                
                
                if os.path.exists(filepath):               # Comprobar si el nombre de archivo ya existe y cambiarlo
                    base, extension = filename.split('.')
                    counter = 1
                    while os.path.exists(filepath):
                        filename = f"{base}({counter}).{extension}"
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        counter += 1
                        
                        
                file.save(filepath)
                file.seek(0)
                file_hash = hashlib.sha256(file.read()).hexdigest()

                file_size = os.path.getsize(filepath)
                new_file = File(name=filename, path=filepath, sha256=file_hash, size=file_size)
                db.session.add(new_file)
                
        db.session.commit()
        flash('Ficheros subidos con exito', 'success')
        return redirect(url_for('file_manager.dashboard'))
    
    except Exception as e:
        flash('Error al subir archivos', 'danger')
        print(e)
    return redirect(url_for('file_manager.dashboard'))

@file_manager.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    return send_file(os.path.join(os.path.abspath(current_app.config['UPLOAD_FOLDER']), file.name), as_attachment=True)

@file_manager.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get(file_id)
    try:
        os.remove(file.path)
        db.session.delete(file)
        db.session.commit()
        flash('Fichero borrado con exito', 'success')
    except Exception as e:
        flash('Error al borrar el archivo', 'danger')
        print(e)
    return redirect(url_for('file_manager.dashboard'))
