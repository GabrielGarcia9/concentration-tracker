import json
import os


class ConfigManager:
    def __init__(self, config_file="config_time.json", db=None):
        self.config_file = config_file
        self.db = db
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            print(f"Config file {self.config_file} not found. Creating default config.")
            self.config = self.get_config_from_db()
            self.save_config()
        else:
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading JSON config: {e}. Loading from database.")
                self.config = self.get_config_from_db()
                self.save_config()
        return self.config

    def get_config_from_db(self):
        # Cargar las configuraciones de tiempos desde la base de datos
        config = {}
        concentration_types = self.db.get_table_concentration_types()
        for index, row in concentration_types.iterrows():
            config[row["name_type"]] = (
                1500  # Podrías ajustar los tiempos iniciales o preguntar al usuario
            )
        return config

    def save_config(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()
