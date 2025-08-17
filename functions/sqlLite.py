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

    def guardar_inscripcion(self, telefono, nombre, plan, inscrito):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute(
            "INSERT INTO inscripciones (telefono, nombre, plan, inscrito) VALUES (?, ?, ?, ?)",
            (telefono, nombre, plan, inscrito)
        )
        conn.commit()
        conn.close()

    def buscar_inscripcion(self, telefono):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("SELECT * FROM inscripciones WHERE telefono = ?", (telefono,))
        resultado = c.fetchall()
        conn.close()
        
        # Retornar valores
        if len(resultado) > 0:
            return {
                "telefono": resultado[0][1],
                "nombre": resultado[0][2],
                "plan": resultado[0][3],
                "inscrito": resultado[0][4]
            }
        return None

    def limpiar_base(self):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("DELETE * FROM inscripciones")
        conn.commit()
        conn.close()