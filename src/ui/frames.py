import tkinter as tk
from tkinter import messagebox
from typing import Callable
from src.ui.style import Style
from src.ui.widgets import BaseFrame, TaskListBox

class MenuFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.config(bg=Style.COLORS["bg_main"])

        tk.Label(self, text="O que você quer fazer hoje?", font=Style.FONTS["title"], bg=Style.COLORS["bg_main"]).pack(pady=20)

        menu_options = [
            ("📋 Ver todas as tarefas", lambda: controller.show_frame("ListTasksFrame", "Todas", controller.todo_list.get_all_tasks)),
            ("➕ Adicionar tarefa", lambda: controller.show_frame("AddTaksFrame")),
            ("✔️ Marcar como concluída", lambda: controller.show_frame("CompleteTaskFrame")),
            ("🗑️ Remover tarefa", lambda: controller.show_frame("RemoveTaskFrame")),
            ("✅ Ver concluídas", lambda: controller.show_frame("ListTasksFrame", "Concluídas", controller.todo_list.get_completed_tasks)),
            ("⏳ Ver pendentes", lambda: controller.show_frame("ListTasksFrame", "Pendentes", controller.todo_list.get_pending_tasks)),
            ("🚪 Sair", controller.quit)
        ]

        for text, command in menu_options:
            tk.Button(self, text=text, command=command, bg=Style.COLORS["button_primary"], fg=Style.COLORS["text"],
                      font=Style.FONTS["default"], width=30, height=2, bd=0,
                      activebackground=Style.COLORS["button_active"]).pack(pady=5)

class ListTasksFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.title_label = tk.Label(self, text="", font=Style.FONTS["title"], bg=Style.COLORS["bg_list"])
        self.title_label.pack(pady=15)
        
        self.listbox = TaskListBox(self, [])
        
        tk.Button(self, text="🔙 Voltar", font=Style.FONTS["default"], bg=Style.COLORS["button_primary"],
                  width=15, command=lambda: controller.show_frame("MenuFrame")).pack(pady=10)

    def on_show(self, title: str, task_fetcher: Callable):
        self.title_label.config(text=f"📋 {title}")
        self.listbox.update_tasks(task_fetcher())

class AddTaksFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="➕ Nova Tarefa", font=Style.FONTS["title"], bg=Style.COLORS["bg_list"]).pack(pady=20)
        
        self.entry = tk.Entry(self, font=Style.FONTS["entry"], width=30, bd=1, relief="solid")
        self.entry.pack(pady=10, ipady=5)
        
        tk.Button(self, text="Salvar", command=self.save_task, font=Style.FONTS["default"],
                  bg=Style.COLORS["button_success"], width=15).pack(pady=5)
        tk.Button(self, text="🔙 Voltar", command=lambda: controller.show_frame("MenuFrame"), font=Style.FONTS["default"],
                  bg=Style.COLORS["button_primary"], width=15).pack(pady=5)

    def on_show(self):
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def save_task(self):
        description = self.entry.get().strip()
        if description:
            self.controller.todo_list.add_task(description)
            messagebox.showinfo("Sucesso", "Tarefa adicionada!")
            self.controller.show_frame("MenuFrame")
        else:
            messagebox.showwarning("Atenção", "A descrição não pode ser vazia.")

class EditTaskFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.title_label = tk.Label(self, text="", font=Style.FONTS["title"], bg=Style.COLORS["bg_list"])
        self.title_label.pack(pady=15)
        
        self.listbox = TaskListBox(self, [])
        
        self.action_button = tk.Button(self, text="", font=Style.FONTS["default"], width=15)
        self.action_button.pack(pady=5)
        
        tk.Button(self, text="🔙 Voltar", command=lambda: controller.show_frame("MenuFrame"), font=Style.FONTS["default"],
                  bg=Style.COLORS["button_primary"], width=15).pack(pady=5)

    def on_show(self):
        self.listbox.update_tasks(self.controller.todo_list.get_all_tasks())

class CompleteTaskFrame(EditTaskFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.title_label.config(text="✔️ Marcar como Concluída")
        self.action_button.config(text="Concluir", bg=Style.COLORS["button_success"], command=self.complete_task)

    def complete_task(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atenção", "Por favor, selecione uma tarefa.")
            return
        
        index = selected_indices[0]
        self.controller.todo_list.complete_task(index)
        messagebox.showinfo("Sucesso", "Tarefa concluída!")
        self.on_show()

class RemoveTaskFrame(EditTaskFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.title_label.config(text="🗑️ Remover Tarefa")
        self.action_button.config(text="Remover", bg=Style.COLORS["button_danger"], command=self.remove_task)

    def remove_task(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atenção", "Por favor, selecione uma tarefa.")
            return

        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover esta tarefa?"):
            index = selected_indices[0]
            self.controller.todo_list.remove_task(index)
            messagebox.showinfo("Sucesso", "Tarefa removida!")
            self.on_show()