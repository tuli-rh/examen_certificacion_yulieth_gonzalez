from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/cine')
    return render_template('login_registro.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    session['nombre'] = request.form['nombre']
    return redirect('/cine')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email({'email': request.form['email']})
    if not usuario or not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Credenciales inválidas.", "login")
        return redirect('/')
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    return redirect('/cine')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')