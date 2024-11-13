import psycopg2
import json
import os
from datetime import datetime

# Obtener la ruta absoluta del archivo de configuración basado en la ubicación de extraction.py
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

# Cargar la configuracion para conectarse a la base de datos PostgreSQL y a los datos aleatorios
with open(config_path) as config_file:
    config = json.load(config_file)

# Configuracion de la ruta del archivo de datos aleatorios
output_path = config["output_path"]

# Cargar configuración de la base de datos desde variables de entorno
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

try:
    cursor = conn.cursor()

    # Creacion de las tablas
    cursor.execute('''CREATE TABLE IF NOT EXISTS Projects (
            id TEXT PRIMARY KEY,
            name TEXT,
            color TEXT,
            parent_id TEXT,
            child_order INTEGER,
            collapsed BOOLEAN,
            shared BOOLEAN,
            can_assign_tasks BOOLEAN,
            is_deleted BOOLEAN,
            is_archived BOOLEAN,
            is_favorite BOOLEAN,
            sync_id TEXT,
            inbox_project BOOLEAN,
            team_inbox BOOLEAN,
            view_style TEXT
        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            project_id TEXT REFERENCES Projects(id),
            content TEXT,
            description TEXT,
            priority INTEGER,
            parent_id TEXT,
            child_order INTEGER,
            section_id TEXT,
            day_order INTEGER,
            collapsed BOOLEAN,
            labels TEXT,
            added_by_uid TEXT,
            assigned_by_uid TEXT,
            responsible_uid TEXT,
            checked BOOLEAN,
            is_deleted BOOLEAN,
            sync_id TEXT,
            created_at TIMESTAMP,
            due_date DATE,
            due_is_recurring BOOLEAN,
            due_datetime TIMESTAMP,
            due_string TEXT,
            due_timezone TEXT,
            duration_amount INTEGER,
            duration_unit TEXT,
            completed_at TIMESTAMP
        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Activities (
            id TEXT PRIMARY KEY,
            object_type TEXT,
            object_id TEXT,
            event_type TEXT,
            event_date TIMESTAMP,
            parent_project_id TEXT REFERENCES Projects(id),
            initiator_id TEXT
        )''')

    # Lectura de los datos aleatorios
    with open(output_path + '/data.json', 'r') as f:
        data = json.load(f)

    # Insertar los datos en la tabla Projects
    for project in data["projects"]:
        cursor.execute('''INSERT INTO Projects (id, name, color, parent_id, child_order, collapsed, shared,
                                  can_assign_tasks, is_deleted, is_archived, is_favorite,
                                  sync_id, inbox_project, team_inbox, view_style)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING''', (
            project["id"], project["name"], project["color"], project["parent_id"],
            project["child_order"], project["collapsed"], project["shared"],
            project["can_assign_tasks"], project["is_deleted"], project["is_archived"],
            project["is_favorite"], project["sync_id"], project["inbox_project"],
            project["team_inbox"], project["view_style"]
        ))

    # Insertar los datos en la tabla Tasks
    for task in data["tasks"]:
        labels = ','.join(task["labels"]) if task["labels"] else None
        cursor.execute('''INSERT INTO Tasks (id, user_id, project_id, content, description, priority, parent_id,
                               child_order, section_id, day_order, collapsed, labels, added_by_uid,
                               assigned_by_uid, responsible_uid, checked, is_deleted, sync_id,
                               created_at, due_date, due_is_recurring, due_datetime, due_string,
                               due_timezone, duration_amount, duration_unit, completed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING''', (
            task["id"], task["user_id"], task["project_id"], task["content"],
            task["description"], task["priority"], task["parent_id"],
            task["child_order"], task["section_id"], task["day_order"],
            task["collapsed"], labels, task["added_by_uid"],
            task["assigned_by_uid"], task["responsible_uid"], task["checked"],
            task["is_deleted"], task["sync_id"], task["created_at"],
            task["due"]["date"], task["due"]["is_recurring"],
            task["due"]["datetime"], task["due"]["string"],
            task["due"]["timezone"], task["duration"]["amount"],
            task["duration"]["unit"], task["completed_at"]
        ))

    # Insertar los datos en la tabla Activities
    for activity in data["activities"]:
        cursor.execute('''INSERT INTO Activities (id, object_type, object_id, event_type, event_date, parent_project_id, initiator_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING''', (
            activity["id"], activity["object_type"], activity["object_id"],
            activity["event_type"], activity["event_date"], activity["parent_project_id"],
            activity["initiator_id"]
        ))

    # Commit changes and close connection
    conn.commit()
    print("Datos de Projects, Tasks y Activities cargados correctamente en PostgreSQL.")

except Exception as e:
    print("Error durante la carga de los datos:", e)

finally:
    cursor.close()
    conn.close()
