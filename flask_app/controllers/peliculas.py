from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentarios import Comentarios

@app.route('/peliculas')
def mis_peliculas():
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario_id = session['usuario_id']
    mis_peliculas = Pelicula.get_mis_peliculas(usuario_id)
    peliculas_comunidad = Pelicula.get_peliculas_comunidad(usuario_id)
    
    # Esto te mostrará en la consola si hay libros recuperados de la DB
    print("MIS PELICULAS OBTENIDOS:", len(mis_peliculas))
    
    return render_template('peliculas.html', mis_peliculas=mis_peliculas, peliculas_comunidad=peliculas_comunidad)

@app.route('/peliculas/nuevo')
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nueva_pelicula.html')

@app.route('/peliculas/crear', methods=['POST'])
def crear_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')

    # 1. Imprimir los datos que llegan del formulario
    print("\n--- DATOS RECIBIDOS DEL FORMULARIO ---")
    print(request.form)

    # 2. Verificar la validación
    es_valido = Pelicula.validar_Pelicula(request.form)
    print("¿PASÓ LA VALIDACIÓN?:", es_valido)

    if not es_valido:
        print("---> Falló la validación, redirigiendo a /peliculas/nuevo\n")
        return redirect('/peliculas/nuevo')

    data = {
        'titulo': request.form['titulo'],
        'director': request.form['director'],
        'fecha_estreno': request.form['fecha_estreno'],
        'sinopsis': request.form['sinopsis'],
        'usuario_id': session['usuario_id']
    }
    
    # 3. Intentar guardar y ver el ID generado
    nuevo_id = Pelicula.save(data)
    print("RESULTADO DE LA INSERCIÓN EN MYSQL (ID/Status):", nuevo_id)
    print("---------------------------------------\n")

    return redirect('/peliculas')

@app.route('/peliculas/<int:id>')
def mostrar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if not pelicula:
        return redirect('/pwliculas')

    es_coment = Comentarios.es_comentario({'usuario_id': session['usuario_id'], 'pelicula_id': id})
    usuarios_coment = Comentarios.get_usuarios_comentario(id)

    return render_template('detalle_pelicula.html', pelicula=pelicula, es_comentario=es_coment, usuarios_coment=usuarios_coment)

@app.route('/peliculas/editar/<int:id>')
def editar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/peliculas')

    return render_template('editar_peli.html', pelicula=pelicula)

@app.route('/peliculas/actualizar/<int:id>', methods=['POST'])
def actualizar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.get_by_id(id)
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/peliculas')

    if not Pelicula.validar_pelicula(request.form):
        return redirect(f'/peliculas/editar/{id}')

    data = {
        'id': id,
        'titulo': request.form['titulo'],
        'director': request.form['director'],
        'fecha_estreno': request.form['fecha_estreno'],
        'sinopsis': request.form['sinopsis'],
        'usuario_id': session['usuario_id']
    }
    Pelicula.update(data)
    return redirect('/peliculas')

@app.route('/peliculas/borrar/<int:id>')
def borrar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    data = {
        'id': id,
        'usuario_id': session['usuario_id']
    }
    Pelicula.delete(data)
    return redirect('/peliculas')

@app.route('/comentarios/agregar/<int:pelicula_id>')
def agregar_comentario(pelicula_id):
    if 'usuario_id' not in session:
        return redirect('/')

    Comentarios.add_comentario({'usuario_id': session['usuario_id'], 'pelicula_id': pelicula_id})
    return redirect(f'/peliculas/{pelicula_id}')

@app.route('/comentarios')
def mis_comentarios():
    if 'usuario_id' not in session:
        return redirect('/')

    comentarios = Comentarios.get_comentarios_por_usuario(session['usuario_id'])
    return render_template('mis_comentarios.html', comentarios=comentarios)