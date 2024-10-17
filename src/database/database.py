import sqlite3
import pandas as pd


class TemporizadorDB:
    def __init__(self, db_name="RegisterSessionsConcentration.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS concentration_types (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name_type TEXT NOT NULL
                                )"""
            )
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS subconcentration_types (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name_subtype TEXT NOT NULL,
                                    concentration_type_id INTEGER NOT NULL,
                                    FOREIGN KEY (concentration_type_id) REFERENCES concentration_types(id)
                                )"""
            )

            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS concentration_sessions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    start_time DATETIME NOT NULL,
                                    end_time DATETIME NOT NULL,
                                    concentration_type_id INTEGER NOT NULL,
                                    subconcentration_type_id INTEGER INTEGER NOT NULL,
                                    FOREIGN KEY (concentration_type_id) REFERENCES concentration_types(id),
                                    FOREIGN KEY (subconcentration_type_id) REFERENCES subconcentration_types(id)
                              )"""
            )

    def add_session(
        self, start_time, end_time, concentration_type_id, subconcentration_type_id
    ):
        with self.conn:
            self.conn.execute(
                """INSERT INTO concentration_sessions (start_time, end_time, concentration_type_id, subconcentration_type_id)
                                 VALUES (?, ?, ?, ?)""",
                (start_time, end_time, concentration_type_id, subconcentration_type_id),
            )

    def add_type_concentration(self, new_type: str):
        with self.conn:
            self.conn.execute(
                """INSERT INTO concentration_types (name_type)
            VALUES (?)""",
                (new_type,),
            )

    def add_type_subconcentration(self, new_subtype: str, id_type):
        with self.conn:
            self.conn.execute(
                """INSERT INTO subconcentration_types (name_subtype, concentration_type_id)
                              VALUES (?, ?)""",
                (
                    new_subtype,
                    id_type,
                ),
            )

    def get_table_concentration_sessions(self):
        query = """
            SELECT cs.start_time, cs.end_time, ct.name_type, st.name_subtype
            FROM concentration_sessions cs
            LEFT JOIN concentration_types ct ON cs.concentration_type_id = ct.id
            LEFT JOIN subconcentration_types st ON cs.subconcentration_type_id = st.id
        """
        return pd.read_sql_query(query, self.conn)

    def get_table_concentration_types(self):
        query = """
            SELECT id, name_type 
            FROM concentration_types
        """
        return pd.read_sql_query(query, self.conn)

    def get_table_subconcentration_types(self):
        query = """
            SELECT st.id, ct.name_type, st.name_subtype
            FROM subconcentration_types st
            JOIN concentration_types ct ON st.concentration_type_id = ct.id
        """
        return pd.read_sql_query(query, self.conn)

    def delete_type_concentration(self, id_type_concentration):
        with self.conn:
            self.conn.execute(
                """
                DELETE FROM subconcentration_types
                WHERE concentration_type_id = ?""",
                (id_type_concentration,),
            )
            self.conn.execute(
                """
                DELETE FROM concentration_types
                WHERE id = ?""",
                (id_type_concentration,),
            )

    def delete_subtype_concentration(self, id_type_subconcentration):
        with self.conn:
            self.conn.execute(
                """DELETE FROM subconcentration_types
                WHERE id = ?""",
                (id_type_subconcentration,),
            )

    def close(self):
        self.conn.close()


##########################################################################################################################
# Probando
# from datetime import datetime

# db = TemporizadorDB()
# db.add_type_concentration("Estúdio")
# db.add_type_subconcentration("Lectura", 1)

# start_time = datetime(2024, 10, 10, 9, 0, 0)
# end_time = datetime(2024, 10, 10, 10, 0, 0)

# db.add_session(start_time, end_time, 1, 1)

# # ------------------------------------------
# db.add_type_subconcentration("Resumir", 1)

# start_time = datetime(2024, 10, 10, 10, 0, 0)
# end_time = datetime(2024, 10, 10, 11, 0, 0)

# db.add_session(start_time, end_time, 1, 2)
# # ------------------------------------------
# db.add_type_concentration("Ejercitarse físicamente")
# db.add_type_subconcentration("Cárdio", 2)

# start_time = datetime(2024, 10, 10, 11, 0, 0)
# end_time = datetime(2024, 10, 10, 12, 0, 0)

# db.add_session(start_time, end_time, 2, 3)
# # ------------------------------------------


# table_types = db.get_table_concentration_types()
# table_subtypes = db.get_table_subconcentration_types()
# table_sessions = db.get_table_concentration_sessions()

# db.close()

# print("table_types\n")
# print(table_types)
# print("table_subtypes\n")
# print(table_subtypes)
# print("table_sessions\n")
# print(table_sessions)


########################################################################################################################
