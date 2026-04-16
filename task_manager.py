# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:47:52 2026

@author: 14533
"""




import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Task:
    def __init__(self, task_id, description, completed=False, created_at=None):
        self.id = task_id
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {"id": self.id, "description": self.description, 
                "completed": self.completed, "created_at": self.created_at}

    @staticmethod
    def from_dict(data):
        return Task(data["id"], data["description"], data["completed"], data["created_at"])

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
        self.next_id = max([t.id for t in self.tasks], default=0) + 1

    def add_task(self, description):
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()

    def get_all_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            self.tasks = []

class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("500x400")

        # UI components
        self.listbox = tk.Listbox(root, height=15, width=60)
        self.listbox.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Add Task", command=self.add_task_ui).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Complete Task", command=self.complete_task_ui).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task_ui).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_list).grid(row=0, column=3, padx=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.manager.get_all_tasks():
            status = "✓" if task.completed else "◻"
            self.listbox.insert(tk.END, f"[{status}] {task.id}: {task.description}")

    def add_task_ui(self):
        desc = simpledialog.askstring("New Task", "Task description:")
        if desc:
            self.manager.add_task(desc)
            self.refresh_list()

    def complete_task_ui(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a task to complete.")
            return
        line = self.listbox.get(selection[0])
        task_id = int(line.split(":")[0].split()[-1])   # 提取ID
        self.manager.complete_task(task_id)
        self.refresh_list()

    def delete_task_ui(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a task to delete.")
            return
        line = self.listbox.get(selection[0])
        task_id = int(line.split(":")[0].split()[-1])
        self.manager.delete_task(task_id)
        self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()