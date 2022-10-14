from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Show:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.descr = data['descr']
        self.release_date = data['release_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title'])<3:
            flash("The name cannot be shorter than 3.")
            is_valid = False
        if len(show['descr'])<3:
            flash("The description cannot be shorter than 3.")
            is_valid = False
        if len(show['release_date'])<3:
            flash("The release date cannot be empty.")
            is_valid = False
        return is_valid
        

    @classmethod
    def get_all_shows(cls, data):
        query = "SELECT id, title, network, release_date, descr,shows.user_id, b.user_id AS liker_id, shows.created_at, shows.updated_at FROM tv_shows_schema.shows LEFT JOIN (SELECT * FROM likes WHERE likes.user_id = %(id)s) AS b ON shows.id = b.show_id;"
        results = connectToMySQL('tv_shows_schema').query_db(query, data)
        shows = []
        for show in results:
            shows.append(show)
        return shows

    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (title, network, descr, release_date, user_id) value (%(title)s, %(network)s, %(descr)s, %(release_date)s, %(user_id)s);"
        return connectToMySQL("tv_shows_schema").query_db(query, data)

    @classmethod
    def edit(cls, data):
        if Show.get_liker_count(data):
            query = "DELETE FROM likes WHERE show_id = %(r_id)s"
            connectToMySQL("tv_shows_schema").query_db(query, data)
            query = "UPDATE shows SET title = %(title)s, network =%(network)s, descr = %(descr)s, release_date = %(release_date)s  WHERE id =%(r_id)s;"
            result = connectToMySQL("tv_shows_schema").query_db(query, data)       
            query = "INSERT INTO likes (user_id, show_id) values  (%(user_id)s, %(r_id)s);"
            connectToMySQL("tv_shows_schema").query_db(query, data)
        query = "UPDATE shows SET title = %(title)s, network =%(network)s, descr = %(descr)s, release_date = %(release_date)s  WHERE id =%(r_id)s;"
        result = connectToMySQL("tv_shows_schema").query_db(query, data) 
        return result
    
    @classmethod
    def delete(cls, data):
        print('-----------thisis delete',data)
        query = "DELETE FROM likes WHERE show_id = %(id)s"
        connectToMySQL("tv_shows_schema").query_db(query, data)
        query = "DELETE FROM shows WHERE id = %(id)s"
        return connectToMySQL("tv_shows_schema").query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL('tv_shows_schema').query_db(query, data)
        # print("__________",data, query, results)
        if not results:
            return False
        return results[0]

    @classmethod
    def get_liker_count(cls, data):
        query = "SELECT count(*) as count from tv_shows_schema.users LEFT JOIN likes ON users.id = likes.user_id WHERE show_id = %(r_id)s;"
        results = connectToMySQL('tv_shows_schema').query_db(query, data)
        # print("__________",data, query, results)
        if not results:
            return False
        return results[0]['count']

        