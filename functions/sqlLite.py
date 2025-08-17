import sqlite3

class dbClub:
    def __init__(self):
        self.dbName = 'club.db'
        self.create_Table()

    def create_Table(self):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS inscripciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telefono TEXT,
                nombre TEXT,
                plan INTEGER,
                inscrito BOOLEAN
            )
        ''')
        conn.commit()
        conn.close()

    def guardar_inscripcion(self, telefono, nombre, plan):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute(
            "INSERT INTO inscripciones (telefono, nombre, plan, inscrito) VALUES (?, ?, ?, ?)",
            (telefono, nombre, plan)
        )
        conn.commit()
        conn.close()

    def buscar_inscripcion(self, telefono):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("SELECT * FROM inscripciones WHERE telefono = ?", (telefono,))
        resultado = c.fetchone()
        conn.close()
        return resultado