import sqlite3

class DatabaseManager:
    def __init__(self, db_path="app.db"):
        self.db_path = db_path

    def connect(self):
        #Apre la connessione al db

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_query(self, query, params=(), fetchone=False, commit=False):
        #Esegue una query
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)

        result = None

        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

        if commit:
            conn.commit()
        conn.close()
        return result