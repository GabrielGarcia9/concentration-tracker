import json
import os

class ConfigManager:
    def __init__(self, config_file="config_time.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def default_config(self):
            # Devuelve una configuración por defecto
            return {
                "study_duration": 1500,  
                "meditation_duration": 300, 
                "exercise_physical_duration": 900,
                "work_duration": 3000 
            }

    def load_config(self):
        if not os.path.exists(self.config_file):
            print(f"Config file {self.config_file} not found. Creating default config.")
            self.config = self.default_config()
            self.save_config()
        else:
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading JSON config: {e}. Loading default config.")
                self.config = self.default_config()
                self.save_config()
        return self.config

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()

  
# Ejemplo de uso
# if __name__ == "__main__":
#     config_manager = ConfigManager()
#     concentration_duration = config_manager.config['concentration_duration']  # Mostrar la configuración cargada
#     print(type(concentration_duration))