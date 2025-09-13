import tkinter as tk
from typing import List
from src.backend.models import Task
from src.ui.style import Style

class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Style.COLORS["bg_list"])
        self.controller = controller

class TaskListBox(tk.Listbox):
    def __init__(self, parent, tasks: List[Task]):
        super().__init__(parent, width=40, height=15, font=Style.FONTS["default"],
                         bg=Style.COLORS["bg_list"], bd=0, highlightthickness=0,
                         selectbackground=Style.COLORS["select"])
        self.pack(pady=10, padx=10)
        self.update_tasks(tasks)

    def update_tasks(self, tasks: List[Task]):
        self.delete(0, tk.END)
        if not tasks:
            self.insert(tk.END, "Nenhuma tarefa encontrada.")
        else:
            for task in tasks:
                self.insert(tk.END, str(task))