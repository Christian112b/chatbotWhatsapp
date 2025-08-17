import sqlite3

from datetime import datetime
from dateutil.relativedelta import relativedelta


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
                duracion INTEGER,
                fecha_inscripcion DATE,
                fecha_ultimo_pago DATE,
                fecha_caducacidad_pago DATE,
                cantidad_pago INTEGER
                )
            ''')
        conn.commit()
        conn.close()

    def guardar_inscripcion(self, userdict):
        telefono = userdict['telefono']
        nombre = userdict['nombre']
        plan = userdict['plan']
        duracion = userdict['duracion']
        total = userdict['total']
        fecha_inscripcion = datetime.now().date()
        fecha_ultimo_pago = fecha_inscripcion
        fecha_caducidad_pago = fecha_ultimo_pago + relativedelta(months=int(duracion))

        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()

        c.execute('''
            INSERT INTO inscripciones (
                telefono, 
                nombre, 
                plan, 
                duracion, 
                fecha_inscripcion,
                fecha_ultimo_pago,
                fecha_caducacidad_pago,
                cantidad_pago
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            telefono,
            nombre,
            plan,
            duracion,
            fecha_inscripcion.isoformat(),       # Convertir a string
            fecha_ultimo_pago.isoformat(),
            fecha_caducidad_pago.isoformat(),
            total
        ))

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
                "duracion": resultado[0][4]
            }
        return None

    def limpiar_base(self):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("DELETE * FROM inscripciones")
        conn.commit()
        conn.close()

    def borrar_tabla(self):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS inscripciones")
        conn.commit()
        conn.close()
