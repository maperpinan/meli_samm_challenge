from faker import Faker
import random
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta, date
import pytz

class DataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.project_colors = [
            "berry_red", "red", "orange", "yellow", "olive_green", 
            "lime_green", "green", "mint_green", "teal", "sky_blue", 
            "light_blue", "blue", "grape", "violet", "lavender",
            "magenta", "salmon", "charcoal", "grey", "taupe"
        ]
        self.view_styles = ["list", "board"]
        self.task_labels = [
            "Food", "Shopping", "Work", "Personal", "Health", 
            "Family", "Education", "Finance", "Travel", "Home"
        ]
        self.task_contents = [
            "Buy Milk", "Schedule meeting", "Call doctor", "Pay bills",
            "Send email", "Review document", "Prepare presentation",
            "Clean house", "Go grocery shopping", "Exercise"
        ]
        self.time_zones = [
            "Europe/Moscow", "America/New_York", "Asia/Tokyo",
            "Europe/London", "Australia/Sydney", "Pacific/Auckland"
        ]
        self.duration_units = ["minute", "hour", "day"]
        self.event_types = ["added", "updated", "completed", "uncompleted", "deleted"]

    def generate_projects(self, num_projects: int) -> List[Dict[str, Any]]:
        projects = []
        for _ in range(num_projects):
            project_id = str(self.fake.unique.random_number(digits=10))
            project = {
                "id": project_id,
                "name": self.fake.catch_phrase(),
                "color": random.choice(self.project_colors),
                "parent_id": None,
                "child_order": random.randint(1, 100),
                "collapsed": random.choice([True, False]),
                "shared": random.choice([True, False]),
                "can_assign_tasks": random.choice([True, False]),
                "is_deleted": random.choice([True, False]),
                "is_archived": random.choice([True, False]),
                "is_favorite": random.choice([True, False]),
                "sync_id": None,
                "inbox_project": random.choice([True, False]),
                "team_inbox": random.choice([True, False]),
                "view_style": random.choice(self.view_styles),
            }
            
            if random.random() < 0.2 and len(projects) > 0:
                parent = random.choice(projects)
                project["parent_id"] = parent["id"]
            
            projects.append(project)
        
        return projects

    def generate_tasks(self, num_tasks: int, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        tasks = []
        
        # Define las fechas de inicio y fin como objetos date para limitar el rango a solo desdes Agosto
        start_date = date(2024, 6, 1)
        end_date = date(2024, 11, 10)
        
        for _ in range(num_tasks):
            task_id = str(self.fake.unique.random_number(digits=10))
            project = random.choice(projects)
            
            # Generar la fecha de creación aleatoria entre start_date y end_date
            created_at = self.fake.date_time_between(
                start_date=start_date,
                end_date=end_date,
                tzinfo=pytz.UTC
            ).strftime("%Y-%m-%dT%H:%M:%S.000000Z")
            
            # Generar la fecha de vencimiento aleatoria entre start_date y end_date
            due_date = self.fake.date_between(
                start_date=start_date,
                end_date=end_date
            ).strftime("%Y-%m-%d")
            
            due_datetime = (datetime.strptime(due_date, "%Y-%m-%d") + 
                            timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59)))
            
            num_labels = random.randint(1, 3)
            labels = random.sample(self.task_labels, num_labels)
            
            task = {
                "id": task_id,
                "user_id": str(self.fake.random_number(digits=7)),
                "project_id": project["id"],
                "content": random.choice(self.task_contents),
                "description": self.fake.text(max_nb_chars=100) if random.random() > 0.5 else "",
                "priority": random.randint(1, 4),
                "parent_id": None,
                "child_order": random.randint(1, 100),
                "section_id": str(random.randint(1000, 9999)),
                "day_order": random.randint(1, 50),
                "collapsed": random.choice([True, False]),
                "labels": labels,
                "added_by_uid": str(self.fake.random_number(digits=7)),
                "assigned_by_uid": str(self.fake.random_number(digits=7)),
                "responsible_uid": str(self.fake.random_number(digits=7)),
                "checked": random.choice([True, False]),
                "is_deleted": random.choice([True, False]),
                "sync_id": None,
                "created_at": created_at,
                "due": {
                    "date": due_date,
                    "is_recurring": random.choice([True, False]),
                    "datetime": due_datetime.strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
                    "string": f"on {due_date}",
                    "timezone": random.choice(self.time_zones)
                },
                "duration": {
                    "amount": random.randint(5, 120),
                    "unit": random.choice(self.duration_units)
                },
            }
            
            # Define `completed_at` basándose en `task["checked"]`
            task["completed_at"] = created_at if task["checked"] else None
            
            if random.random() < 0.2 and len(tasks) > 0:
                parent = random.choice(tasks)
                task["parent_id"] = parent["id"]
            
            tasks.append(task)
        
        return tasks

    def generate_activity(self, tasks: List[Dict[str, Any]], projects: List[Dict[str, Any]], num_events: int) -> List[Dict[str, Any]]:
        activities = []
        
        # Define las fechas de inicio y fin para limitar el rango de eventos
        start_date = datetime.now() - timedelta(days=90)
        end_date = datetime.now()
        
        for _ in range(num_events):
            # Selecciona aleatoriamente una tarea o proyecto para el evento
            task_type = random.choice(["task", "project"])
            if task_type == "task":
                task = random.choice(tasks)
            else:
                task = random.choice(projects)
                
            activity = {
                "id": str(self.fake.unique.random_number(digits=10)),
                "object_type": task_type,
                "object_id": task["id"],
                "event_type": random.choice(self.event_types),
                "event_date": self.fake.date_time_between(
                    start_date=start_date,
                    end_date=end_date,
                    tzinfo=pytz.UTC
                ).strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
                "parent_project_id": task.get("project_id") if task_type == "task" else task["id"],
                "initiator_id": str(self.fake.random_number(digits=7))
            }
            
            activities.append(activity)
        
        return activities

    def generate_sample_data(self, num_projects: int = 10, num_tasks: int = 20, num_events: int = 50):
        projects = self.generate_projects(num_projects)
        tasks = self.generate_tasks(num_tasks, projects)
        activities = self.generate_activity(tasks, projects, num_events)
        
        return {
            "projects": projects,
            "tasks": tasks,
            "activities": activities
        }