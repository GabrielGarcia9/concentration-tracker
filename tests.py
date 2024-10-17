import unittest
from src.database.database import TemporizadorDB
from datetime import datetime
import pandas as pd
import sqlite3
from unittest.mock import MagicMock
import json
import os
from src.config import ConfigManager


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        # Simula la base de datos
        self.mock_db = MagicMock()

        # Simula la tabla de tipos de concentración
        self.mock_db.get_table_concentration_types.return_value = pd.DataFrame(
            {"id": [1, 2], "name_type": ["Estudio", "Lectura"]}
        )

        # Simula el archivo de configuración JSON en memoria
        self.config_file = "test_config_time.json"

        # Inicializa ConfigManager con la base de datos simulada y el archivo de configuración
        self.config_manager = ConfigManager(
            config_file=self.config_file, db=self.mock_db
        )

    def tearDown(self):
        # Elimina el archivo de configuración simulado si existe
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_load_config_no_file(self):
        # Prueba que cuando no hay archivo, se cargue la configuración desde la base de datos
        config = self.config_manager.load_config()
        self.mock_db.get_table_concentration_types.assert_called_once()
        self.assertEqual(config["Estudio"], 1500)
        self.assertEqual(config["Lectura"], 1500)

    def test_load_config_with_file(self):
        # Simula un archivo de configuración existente
        config_data = {"Estudio": 1800, "Lectura": 600}
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

        config = self.config_manager.load_config()

        # Verifica que la configuración se haya cargado desde el archivo
        self.assertEqual(config["Estudio"], 1800)
        self.assertEqual(config["Lectura"], 600)

    def test_update_config(self):
        # Actualiza la configuración y verifica que se guarde correctamente
        self.config_manager.update_config("Estudio", 2000)

        # Verifica que el archivo contenga la nueva configuración
        with open(self.config_file, "r") as f:
            config = json.load(f)

        self.assertEqual(config["Estudio"], 2000)


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
        self.db.add_type_concentration("Estudio")
        result = self.db.get_table_concentration_types()
        self.assertEqual(len(result), 1)
        concentration_type_id = int(result["id"][0])

        self.db.add_type_subconcentration("Lectura", concentration_type_id)
        self.db.add_type_subconcentration("Resumir", concentration_type_id)
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(len(subtypes_result), 2)

        self.db.delete_type_concentration(concentration_type_id)
        result = self.db.get_table_concentration_types()
        self.assertEqual(len(result), 0)  # El tipo debería ser eliminado
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(
            len(subtypes_result), 0
        )  # Los subtipos también deberían ser eliminados

    def test_delete_subtype_concentration(self):
        self.db.add_type_concentration("Estudio")
        result = self.db.get_table_concentration_types()
        concentration_type_id = int(result["id"][0])

        self.db.add_type_subconcentration("Lectura", concentration_type_id)
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(len(subtypes_result), 1)
        subtype_id = int(subtypes_result["id"][0])

        self.db.delete_subtype_concentration(subtype_id)
        subtypes_result = self.db.get_table_subconcentration_types()
        self.assertEqual(len(subtypes_result), 0)  # El subtipo debería ser eliminado


if __name__ == "__main__":
    unittest.main()
