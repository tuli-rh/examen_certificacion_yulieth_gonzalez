from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Pelicula:
    db = 'esquema_peliculas'

    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creador = data.get('creador', '')

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id)
        VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM peliculas;"
        results = connectToMySQL(cls.db).query_db(query)
        peliculas = []
        for row in results:
            peliculas.append(cls(row))
        return peliculas

    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT peliculas.*, usuarios.nombre AS creador 
        FROM peliculas 
        JOIN usuarios ON peliculas.usuario_id = usuarios.id 
        WHERE peliculas.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
        UPDATE peliculas 
        SET titulo = %(titulo)s, director = %(director)s, fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s 
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_titulo(cls, data):
        query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validar_pelicula(data, pelicula_id=None):
        is_valid = True
        if len(data.get('titulo', '')) < 3:
            flash("El nombre de la película debe tener al menos 3 caracteres.", "pelicula")
            is_valid = False
        else:
            peli_existente = Pelicula.get_by_titulo({'titulo': data['titulo']})
            if peli_existente and (pelicula_id is None or str(peli_existente.id) != str(pelicula_id)):
                flash("El nombre de la película debe ser único.", "pelicula")
                is_valid = False

        if len(data.get('director', '')) < 3:
            flash("El director debe tener al menos 3 caracteres.", "pelicula")
            is_valid = False
        if not data.get('fecha_estreno'):
            flash("Debe proporcionar una fecha de estreno.", "pelicula")
            is_valid = False
        if len(data.get('sinopsis', '')) < 3:
            flash("La sinopsis debe tener al menos 3 caracteres.", "pelicula")
            is_valid = False
        return is_valid