import json
import os
from data_generation.random_data_generator import DataGenerator

# Obtener la ruta absoluta del archivo de configuración basado en la ubicación de extraction.py
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

# Cargar la ubicacion de la carpeta output
with open(config_path) as config_file:
    config = json.load(config_file)
output_path = config["output_path"]

# Generacion de los datos aleatorios
generator = DataGenerator()
data = generator.generate_sample_data(num_projects=5, num_tasks=20, num_events=50)

# Guardar los datos como un archivo JSON
with open(output_path + '/data.json', 'w') as f:
    json.dump(data, f)

print("Datos extraídos y guardados en 'data.json'.")


