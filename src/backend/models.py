import json
import os
from typing import List, Dict, Union

TaskDict = Dict[str, Union[str, bool]]

class Task:
    def __init__(self, description: str, completed: bool = False):
        self.description = description
        self.completed = completed

    def to_dict(self) -> TaskDict:
        return {"descricao": self.description, "concluida": self.completed}

    def __str__(self) -> str:
        status = "✔️" if self.completed else "❌"
        return f"{status} {self.description}"

class TodoList:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = self._load_tasks()

    def _load_tasks(self) -> List[Task]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)
            return [Task(t["descricao"], t["concluida"]) for t in tasks_data]
        except (json.JSONDecodeError, KeyError):
            return []

    def _save_tasks(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4, ensure_ascii=False)

    def add_task(self, description: str):
        if description:
            self.tasks.append(Task(description))
            self._save_tasks()

    def complete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self._save_tasks()

    def remove_task(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self._save_tasks()
            
    def get_all_tasks(self) -> List[Task]:
        return self.tasks
        
    def get_completed_tasks(self) -> List[Task]:
        return [task for task in self.tasks if task.completed]
        
    def get_pending_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.completed]