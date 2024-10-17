import unittest
from src.database.database import TemporizadorDB
from datetime import datetime
import pandas as pd
import sqlite3


class TestTemporizadorDB(unittest.TestCase):
    def setUp(self):
        self.db = TemporizadorDB(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_type_concentration(self):
        self.db.add_type_concentration("Estudio")
        result = self.db.get_table_concentration_types()
        self.assertEqual(len(result), 1)
        self.assertEqual(result["name_type"][0], "Estudio")

    def test_add_type_subconcentration(self):
        self.db.add_type_concentration("Estudio")
        table_concentration_types = self.db.get_table_concentration_types()
        self.assertEqual(table_concentration_types["name_type"][0], "Estudio")
        concentration_type_id = int(table_concentration_types["id"][0])
        self.db.add_type_subconcentration("Lectura", concentration_type_id)
        table_subconcentration_types = self.db.get_table_subconcentration_types()
        self.assertEqual(table_subconcentration_types["name_subtype"][0], "Lectura")
        self.assertEqual(table_subconcentration_types["name_type"][0], "Estudio")

    def test_add_session(self):
        self.db.add_type_concentration("Estudio")
        table_concentration_types = self.db.get_table_concentration_types()

        concentration_type_id = int(table_concentration_types["id"][0])

        self.db.add_type_subconcentration("Lectura", concentration_type_id)
        self.db.add_type_subconcentration("Resumir", concentration_type_id)
        table_subconcentration_types = self.db.get_table_subconcentration_types()

        subconcentration_type_id_1 = int(table_subconcentration_types["id"][0])
        subconcentration_type_id_2 = int(table_subconcentration_types["id"][1])

        start_time = datetime(2024, 10, 10, 9, 0, 0)
        end_time = datetime(2024, 10, 10, 10, 0, 0)
        self.db.add_session(
            start_time, end_time, concentration_type_id, subconcentration_type_id_1
        )

        sessions_result = self.db.get_table_concentration_sessions()

        self.assertEqual(len(sessions_result), 1)
        self.assertEqual(sessions_result["name_type"][0], "Estudio")
        self.assertEqual(sessions_result["name_subtype"][0], "Lectura")

        start_time = datetime(2024, 10, 10, 11, 0, 0)
        end_time = datetime(2024, 10, 10, 12, 0, 0)
        self.db.add_session(
            start_time, end_time, concentration_type_id, subconcentration_type_id_2
        )

        sessions_result = self.db.get_table_concentration_sessions()
        self.assertEqual(len(sessions_result), 2)
        self.assertEqual(sessions_result["name_type"][1], "Estudio")
        self.assertEqual(sessions_result["name_subtype"][1], "Resumir")

    def test_delete_type_concentration(self):
        # Añadir un tipo de concentración
        self.db.add_type_concentration("Estudio")
        result = self.db.get_table_concentration_types()
        self.assertEqual(len(result), 1)
        concentration_type_id = int(result["id"][0])

        # Añadir subtipos de concentración relacionados
        self.db.add_type_subconcentration("Lectura", concentration_type_id)
        self.db.add_type_subconcentration("Resumir", concentration_type_id)
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(len(subtypes_result), 2)

        # Eliminar tipo de concentración y verificar que se eliminan también los subtipos relacionados
        self.db.delete_type_concentration(concentration_type_id)
        result = self.db.get_table_concentration_types()
        self.assertEqual(len(result), 0)  # El tipo debería ser eliminado
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(
            len(subtypes_result), 0
        )  # Los subtipos también deberían ser eliminados

    def test_delete_subtype_concentration(self):
        # Añadir un tipo de concentración
        self.db.add_type_concentration("Estudio")
        result = self.db.get_table_concentration_types()
        concentration_type_id = int(result["id"][0])

        # Añadir subtipo de concentración
        self.db.add_type_subconcentration("Lectura", concentration_type_id)
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(len(subtypes_result), 1)
        subtype_id = int(subtypes_result["id"][0])

        # Eliminar subtipo de concentración y verificar que se elimina
        self.db.delete_subtype_concentration(subtype_id)
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(len(subtypes_result), 0)  # El subtipo debería ser eliminado


if __name__ == "__main__":
    unittest.main()
