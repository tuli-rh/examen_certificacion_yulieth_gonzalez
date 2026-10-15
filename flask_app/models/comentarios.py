from flask_app.config.mysqlconnection import connectToMySQL

class Comentario:
    db = 'esquema_peliculas'

    def __init__(self, data):
        self.id = data['id']
        self.comentario = data['comentario']
        self.usuario_id = data['usuario_id']
        self.pelicula_id = data['pelicula_id']
        self.created_at = data['created_at']
        self.autor = data.get('autor', '')

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO comentarios (comentario, usuario_id, pelicula_id)
        VALUES (%(comentario)s, %(usuario_id)s, %(pelicula_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_pelicula(cls, data):
        query = """
        SELECT comentarios.*, usuarios.nombre AS autor 
        FROM comentarios 
        JOIN usuarios ON comentarios.usuario_id = usuarios.id 
        WHERE pelicula_id = %(pelicula_id)s 
        ORDER BY comentarios.created_at DESC;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        comentarios = []
        for row in results:
            comentarios.append(cls(row))
        return comentarios

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM comentarios WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)