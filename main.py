import tkinter as tk
from tkinter import messagebox, font
import json
import os
from typing import List, Dict, Union, Callable


TaskDict = Dict[str, Union[str, bool]]

class Task:
    """Representa uma única tarefa."""
    def __init__(self, description: str, completed: bool = False):
        self.description = description
        self.completed = completed

    def to_dict(self) -> TaskDict:
        """Converte a tarefa para um dicionário para salvar em JSON."""
        return {"descricao": self.description, "concluida": self.completed}

    def __str__(self) -> str:
        """Representação em string da tarefa."""
        status = "✔️" if self.completed else "❌"
        return f"{status} {self.description}"

class TodoList:
    """Gerencia a coleção de tarefas (carregar, salvar, adicionar, etc.)."""
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = self._load_tasks()

    def _load_tasks(self) -> List[Task]:
        """Carrega tarefas do arquivo JSON."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)
            return [Task(t["descricao"], t["concluida"]) for t in tasks_data]
        except (json.JSONDecodeError, KeyError):
            return []

    def _save_tasks(self):
        """Salva a lista de tarefas atual no arquivo JSON."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4, ensure_ascii=False)

    def add_task(self, description: str):
        """Adiciona uma nova tarefa à lista."""
        if description:
            self.tasks.append(Task(description))
            self._save_tasks()

    def complete_task(self, index: int):
        """Marca uma tarefa como concluída."""
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self._save_tasks()

    def remove_task(self, index: int):
        """Remove uma tarefa da lista."""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self._save_tasks()


class TodoAppGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.todo_list = TodoList()  

        self._setup_styles()
        self._setup_main_window()

        self.frames = {}
        self._create_frames()
        self.show_frame("menu")

    def _setup_styles(self):
        """Centraliza a configuração de fontes e cores."""
        self.colors = {
            "bg_main": "#fce4ec",
            "bg_list": "#fff3f9",
            "button_primary": "#ce93d8",
            "button_danger": "#ef9a9a",
            "button_success": "#aed581",
            "button_active": "#f8bbd0",
            "text": "black"
        }
        self.fonts = {
            "title": font.Font(family="Arial", size=16, weight="bold"),
            "default": font.Font(family="Arial", size=13, weight="bold")
        }

    def _setup_main_window(self):
        """Configura a janela principal."""
        self.root.title("💗 Minha Lista de Tarefas")
        self.root.geometry("400x500")
        self.root.configure(bg=self.colors["bg_main"])
        self.root.resizable(False, False)

    def _create_frames(self):
        """Cria todos os 'painéis' (telas) da aplicação."""
        self.frames["menu"] = self._create_menu_frame()
        self.frames["ver_tarefas"] = self._create_list_frame("Todas as Tarefas", self.todo_list.tasks)
        self.frames["concluidas"] = self._create_list_frame("Tarefas Concluídas", [t for t in self.todo_list.tasks if t.completed])
        self.frames["pendentes"] = self._create_list_frame("Tarefas Pendentes", [t for t in self.todo_list.tasks if not t.completed])
        self.frames["adicionar"] = self._create_add_frame()
        self.frames["concluir"] = self._create_edit_frame("Marcar como Concluída", self._complete_selected_task)
        self.frames["remover"] = self._create_edit_frame("Remover Tarefa", self._remove_selected_task)

    def show_frame(self, frame_name: str):
        """Mostra um painel específico e esconde os outros."""
        frame = self.frames[frame_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

    def _create_menu_frame(self) -> tk.Frame:
        """Cria o painel do menu principal."""
        frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        
        tk.Label(frame, text="O que você quer fazer hoje?", font=self.fonts["title"], bg=self.colors["bg_main"]).pack(pady=20)

        menu_options = [
            ("📋 Ver todas as tarefas", lambda: self.show_frame("ver_tarefas")),
            ("➕ Adicionar tarefa", lambda: self.show_frame("adicionar")),
            ("✔️ Marcar como concluída", lambda: self.show_frame("concluir")),
            ("🗑️ Remover tarefa", lambda: self.show_frame("remover")),
            ("✅ Ver concluídas", lambda: self.show_frame("concluidas")),
            ("⏳ Ver pendentes", lambda: self.show_frame("pendentes")),
            ("🚪 Sair", self.root.quit)
        ]
        
        for text, command in menu_options:
            tk.Button(frame, text=text, command=command, bg=self.colors["button_primary"], fg=self.colors["text"],
                      font=self.fonts["default"], width=30, height=2, bd=0, activebackground=self.colors["button_active"]
                      ).pack(pady=5)

        frame.place(x=0, y=0, relwidth=1, relheight=1)
        return frame

    def _create_list_frame(self, title: str, task_source: List[Task]) -> tk.Frame:
        """Cria um painel genérico para listar tarefas."""
        frame = tk.Frame(self.root, bg=self.colors["bg_list"])
        tk.Label(frame, text=f"📋 {title}", font=self.fonts["title"], bg=self.colors["bg_list"]).pack(pady=15)

        listbox = tk.Listbox(frame, width=40, height=15, font=self.fonts["default"],
                             bg=self.colors["bg_list"], bd=0, highlightthickness=0, selectbackground=self.colors["button_primary"])
        listbox.pack(pady=10, padx=10)

        def update_list():
            listbox.delete(0, tk.END)
            self.todo_list.tasks = self.todo_list._load_tasks() 
            if title == "Todas as Tarefas":
                tasks_to_show = self.todo_list.tasks
            elif title == "Tarefas Concluídas":
                tasks_to_show = [t for t in self.todo_list.tasks if t.completed]
            else: 
                tasks_to_show = [t for t in self.todo_list.tasks if not t.completed]

            if not tasks_to_show:
                listbox.insert(tk.END, "Nenhuma tarefa encontrada.")
            else:
                for task in tasks_to_show:
                    listbox.insert(tk.END, str(task))
        
        tk.Button(frame, text="🔙 Voltar", font=self.fonts["default"], bg=self.colors["button_primary"],
                  width=15, command=lambda: self.show_frame("menu")).pack(pady=10)

        frame.bind("<<ShowFrame>>", lambda e: update_list())
        frame.place(x=0, y=0, relwidth=1, relheight=1)
        return frame
        
    def _create_add_frame(self) -> tk.Frame:
        frame = tk.Frame(self.root, bg=self.colors["bg_list"])
        tk.Label(frame, text="➕ Nova Tarefa", font=self.fonts["title"], bg=self.colors["bg_list"]).pack(pady=20)

        entry = tk.Entry(frame, font=("Arial", 12), width=30, bd=1, relief="solid")
        entry.pack(pady=10, ipady=5)
        entry.focus()

        def save_task():
            description = entry.get().strip()
            if description:
                self.todo_list.add_task(description)
                entry.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Tarefa adicionada!")
                self.show_frame("menu")
            else:
                messagebox.showwarning("Atenção", "A descrição não pode ser vazia.")

        tk.Button(frame, text="Salvar", command=save_task, font=self.fonts["default"],
                  bg=self.colors["button_success"], width=15).pack(pady=5)
        tk.Button(frame, text="🔙 Voltar", command=lambda: self.show_frame("menu"), font=self.fonts["default"],
                  bg=self.colors["button_primary"], width=15).pack(pady=5)

        frame.place(x=0, y=0, relwidth=1, relheight=1)
        return frame

    def _create_edit_frame(self, title: str, action_callback: Callable) -> tk.Frame:
        frame = tk.Frame(self.root, bg=self.colors["bg_list"])
        tk.Label(frame, text=f"📌 {title}", font=self.fonts["title"], bg=self.colors["bg_list"]).pack(pady=15)
        
        listbox = tk.Listbox(frame, width=40, height=15, font=self.fonts["default"],
                             bg=self.colors["bg_list"], bd=0, highlightthickness=0, selectbackground=self.colors["button_primary"])
        listbox.pack(pady=10, padx=10)

        def update_list():
            listbox.delete(0, tk.END)
            self.todo_list.tasks = self.todo_list._load_tasks()
            for i, task in enumerate(self.todo_list.tasks):
                listbox.insert(tk.END, str(task))
        
        tk.Button(frame, text=title.split(" ")[0], command=lambda: action_callback(listbox), font=self.fonts["default"], 
                  bg=self.colors["button_danger"] if "Remover" in title else self.colors["button_success"], width=15).pack(pady=5)
        tk.Button(frame, text="🔙 Voltar", command=lambda: self.show_frame("menu"), font=self.fonts["default"],
                  bg=self.colors["button_primary"], width=15).pack(pady=5)
        
        frame.bind("<<ShowFrame>>", lambda e: update_list())
        frame.place(x=0, y=0, relwidth=1, relheight=1)
        return frame

    def _complete_selected_task(self, listbox: tk.Listbox):
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atenção", "Por favor, selecione uma tarefa.")
            return
        
        index = selected_indices[0]
        self.todo_list.complete_task(index)
        messagebox.showinfo("Sucesso", "Tarefa concluída!")
        listbox.event_generate("<<ShowFrame>>") 

    def _remove_selected_task(self, listbox: tk.Listbox):
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atenção", "Por favor, selecione uma tarefa.")
            return

        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover esta tarefa?"):
            index = selected_indices[0]
            self.todo_list.remove_task(index)
            messagebox.showinfo("Sucesso", "Tarefa removida!")
            listbox.event_generate("<<ShowFrame>>") 



if __name__ == "__main__":
    root = tk.Tk()
    app = TodoAppGUI(root)
    root.mainloop()
