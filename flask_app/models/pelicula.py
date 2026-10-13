from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, date

class Pelicula:
    DB = "esquema_peliculas"

    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creador_nombre = data.get('creador_nombre', '')

    @classmethod
    def save(cls, data):
        query = "INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id) VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_mis_peliculas(cls, usuario_id):
        query = """
            SELECT l.*, u.nombre AS creador_nombre,
                COUNT(f.usuario_id) AS total_favoritos
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            LEFT JOIN favoritos f ON l.id = f.libro_id
            WHERE l.usuario_id = %(usuario_id)s
            GROUP BY l.id
            ORDER BY l.created_at DESC;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'usuario_id': usuario_id})
        peliculas = []
        if results and isinstance(results, list):
            for row in results:
                peliculas.append(cls(row))
        return peliculas

    @classmethod
    def get_peliculas_comunidad(cls, usuario_id):
        query = """
            SELECT l.*, u.nombre AS creador_nombre,
                COUNT(f.usuario_id) AS total_favoritos
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            LEFT JOIN favoritos f ON l.id = f.libro_id
            WHERE l.usuario_id != %(usuario_id)s
            GROUP BY l.id
            ORDER BY l.created_at DESC;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'usuario_id': usuario_id})
        peliculas = []
        if results and isinstance(results, list):
            for row in results:
                peliculas.append(cls(row))
        return peliculas
    
    @classmethod
    def get_by_id(cls, pelicula_id):
        query = """
            SELECT l.*, u.nombre AS creador_nombre
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'id': pelicula_id})
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE libros 
            SET titulo = %(titulo)s, director = %(director)s, 
                fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM peliculas WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validar_pelicula(pelicula):
        is_valid = True

        if len(pelicula.get('titulo', '').strip()) < 2:
            flash("El título debe tener al menos 2 caracteres.", "pelicla")
            is_valid = False

        if len(pelicula.get('director', '').strip()) < 2:
            flash("El nombre del director debe tener al menos 2 caracteres.", "pelicula")
            is_valid = False

        if not pelicula.get('fecha_estreno'):
            flash("Debe ingresar una fecha de publicación.", "libro")
            is_valid = False
        else:
            try:
                fecha_ingresada = datetime.strptime(pelicula['fecha_estreno'], "%Y-%m-%d").date()
                if fecha_ingresada > date.today():
                    flash("La fecha de esttreno no puede ser una fecha futura.", "pelicula")
                    is_valid = False
            except ValueError:
                flash("Formato de fecha no válido.", "pelicula")
                is_valid = False

        if len(pelicula.get('sinopsis', '').strip()) < 10:
            flash("La sinopsis debe tener al menos 10 caracteres.", "pelicula")
            is_valid = False

        return is_valid

