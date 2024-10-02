import sqlite3
import pandas as pd

class TemporizadorDB:
    def __init__(self, db_name="RegistroSesionesConcentracion.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS concentration_types (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS subconcentration_types (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    concentration_type_id INTEGER NOT NULL,
                                    FOREIGN KEY (concentration_type_id) REFERENCES concentration_types(id)
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS concentration_sessions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    start_time DATETIME NOT NULL,
                                    end_time DATETIME NOT NULL,
                                    concentration_type_id INTEGER NOT NULL,
                                    subconcentration_type_id INTEGER,
                                    FOREIGN KEY (concentration_type_id) REFERENCES concentration_types(id),
                                    FOREIGN KEY (subconcentration_type_id) REFERENCES subconcentration_types(id)
                              )''')

    def add_session(self, start_time, end_time, concentration_type_id, subconcentration_type_id):
        with self.conn:
            self.conn.execute('''INSERT INTO concentration_sessions (start_time, end_time, concentration_type_id, subconcentration_type_id)
                                 VALUES (?, ?, ?, ?)''', (start_time, end_time, concentration_type_id, subconcentration_type_id))

    def get_sessions_with_label(self):
        query = '''
            SELECT cs.start_time, cs.end_time, ct.name AS concentration_type, st.name AS subconcentration_type
            FROM concentration_sessions cs
            LEFT JOIN concentration_types ct ON cs.concentration_type_id = ct.id
            LEFT JOIN subconcentration_types st ON cs.subconcentration_type_id = st.id
        '''
        data = pd.read_sql_query(query, self.conn)
        return data


    def close(self):
        self.conn.close()


########################################################################################################################
    # def insert_concentration_types(self):
    #     concentration_types = [('Estudio',), ('Meditación',), ('Ejercicio Físico',), ('Trabajo',)]
    #     subconcentration_types = [
    #         ('Idiomas', 1), 
    #         ('Desarrollo de software', 1),
    #         ('Vipassana', 2),  
    #         ('Mindfulness', 2),
    #         ('Cardio', 3), 
    #         ('Fuerza', 3),
    #         ('Para mi', 4),
    #         ('Para otro', 4),
    #         ('Inteligencia Artificial y Aprendizaje Automático', 1),
    #         ('Matemáticas aplicadas', 1),
    #         ('Otros', 1)
    #         ]
        
    #     with self.conn:
    #         self.conn.executemany('INSERT INTO concentration_types (name) VALUES (?)', concentration_types)
    #         self.conn.executemany('INSERT INTO subconcentration_types (name, concentration_type_id) VALUES (?, ?)', subconcentration_types)



    # def migrate_data(self): 
    #     tipe_mapping = {
    #         'concentration': (1, None), 
    #         'meditation': (2, None)       
    #     }

    #     with self.conn:
    #         old_sessions = self.conn.execute('SELECT start_time, end_time, tipe FROM focus_sessions').fetchall()

    #         for start_time, end_time, tipe in old_sessions:
    #             concentration_type_id, subconcentration_type_id = tipe_mapping.get(tipe, (None, None))
    #             self.conn.execute('''INSERT INTO concentration_sessions 
    #                                 (start_time, end_time, concentration_type_id, subconcentration_type_id) 
    #                                 VALUES (?, ?, ?, ?)''', 
    #                                 (start_time, end_time, concentration_type_id, subconcentration_type_id))


    # def drop_old_table(self):
    #     with self.conn:
    #         self.conn.execute('DROP TABLE IF EXISTS focus_sessions')

