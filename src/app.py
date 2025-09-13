import tkinter as tk
from src.backend.models import TodoList
from src.ui.frames import MenuFrame, ListTasksFrame, AddTaksFrame, CompleteTaskFrame, RemoveTaskFrame

class TodoAppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.todo_list = TodoList()

        self.title("💗 Minha Lista de Tarefas")
        self.geometry("400x500")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuFrame, ListTasksFrame, AddTaksFrame, CompleteTaskFrame, RemoveTaskFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuFrame")

    def show_frame(self, frame_name, *args):
        frame = self.frames[frame_name]
        if hasattr(frame, 'on_show'):
            frame.on_show(*args)
        frame.tkraise()