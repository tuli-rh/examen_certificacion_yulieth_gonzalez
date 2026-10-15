from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentarios import Comentario

@app.route('/cine')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    peliculas = Pelicula.get_all()
    return render_template('peliculas.html', peliculas=peliculas)

@app.route('/cine/nueva')
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nueva_pelicula.html')

@app.route('/cine/crear', methods=['POST'])
def crear_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')
    if not Pelicula.validar_pelicula(request.form):
        session['form_data'] = request.form
        return redirect('/cine/nueva')
    
    data = {
        'titulo': request.form['titulo'],
        'director': request.form['director'],
        'fecha_estreno': request.form['fecha_estreno'],
        'sinopsis': request.form['sinopsis'],
        'usuario_id': session['usuario_id']
    }
    Pelicula.save(data)
    session.pop('form_data', None)
    return redirect('/cine')

@app.route('/cine/<int:id>')
def ver_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    pelicula = Pelicula.get_by_id({'id': id})
    comentarios = Comentario.get_by_pelicula({'pelicula_id': id})
    return render_template('detalles_pelicula.html', pelicula=pelicula, comentarios=comentarios)

@app.route('/cine/editar/<int:id>')
def editar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    pelicula = Pelicula.get_by_id({'id': id})
    if pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')
    return render_template('editar_peli.html', pelicula=pelicula)

@app.route('/cine/actualizar/<int:id>', methods=['POST'])
def actualizar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    pelicula = Pelicula.get_by_id({'id': id})
    if pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')
    
    if not Pelicula.validar_pelicula(request.form, pelicula_id=id):
        session['form_data'] = request.form
        return redirect(f'/cine/editar/{id}')
    
    data = {
        'id': id,
        'titulo': request.form['titulo'],
        'director': request.form['director'],
        'fecha_estreno': request.form['fecha_estreno'],
        'sinopsis': request.form['sinopsis']
    }
    Pelicula.update(data)
    session.pop('form_data', None)
    return redirect('/cine')

@app.route('/cine/borrar/<int:id>')
def borrar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    pelicula = Pelicula.get_by_id({'id': id})
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        Pelicula.delete({'id': id})
    return redirect('/cine')

@app.route('/comentario/crear', methods=['POST'])
def crear_comentario():
    if 'usuario_id' not in session:
        return redirect('/')
    pelicula_id = request.form['pelicula_id']
    pelicula = Pelicula.get_by_id({'id': pelicula_id})
    
    if pelicula.usuario_id != session['usuario_id'] and len(request.form['comentario'].strip()) > 0:
        Comentario.save({
            'comentario': request.form['comentario'],
            'usuario_id': session['usuario_id'],
            'pelicula_id': pelicula_id
        })
    return redirect(f'/cine/{pelicula_id}')

@app.route('/comentario/borrar/<int:id>/<int:pelicula_id>')
def borrar_comentario(id, pelicula_id):
    if 'usuario_id' not in session:
        return redirect('/')
    Comentario.delete({'id': id, 'usuario_id': session['usuario_id']})
    return redirect(f'/cine/{pelicula_id}')