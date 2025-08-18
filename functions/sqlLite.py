import sqlite3

from datetime import datetime
from dateutil.relativedelta import relativedelta


class dbClub:
    def __init__(self):
        self.dbName = 'club.db'
        self.create_Table()
        self.crear_tabla_preguntas()

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
                "duracion": resultado[0][4],
                "fecha_inscripcion": resultado[0][5],
                "fecha_ultimo_pago": resultado[0][6],
                "fecha_caducidad_pago": resultado[0][6],
                "activo": 1 if resultado[0][6] >= datetime.now().date() else 0,
                "cantidad_pago": resultado[0][7]
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

    def crear_tabla_preguntas(self):
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preguntas_frecuentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pregunta TEXT NOT NULL,
                respuesta TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def agregar_pregunta(pregunta, respuesta):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO preguntas_frecuentes (pregunta, respuesta) VALUES (?, ?)", (pregunta, respuesta))
        conn.commit()
        conn.close()

    def obtener_preguntas():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT pregunta, respuesta FROM preguntas_frecuentes ORDER BY id DESC")
        datos = cursor.fetchall()
        conn.close()
        return datos