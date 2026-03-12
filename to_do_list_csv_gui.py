import tkinter as tk
from tkinter import messagebox
import csv
import os
import sys

tasks = []

if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, "To_do_list_GUI.csv")
def check_csv_integrity():
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv.reader(csv_file)
    except Exception as e:
        messagebox.showerror("File Error", f"CSV file is corrupted: {e}")

def clear_task_display():
    task_listBox.delete(0, tk.END)

def save_task_to_csv():
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for i in range(task_listBox.size()):
            task = task_listBox.get(i)
            csv_writer.writerow([task])

def backup_csv_file():
    backup_path = csv_file_path.replace(".csv", "_backup.csv")
    is_original_empty = False
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as original_file:
            if not original_file.read().strip():
                is_original_empty = True
    except FileNotFoundError:
        is_original_empty = True

    if is_original_empty:
        messagebox.showerror("Backup Error", "No tasks to back up. The original file is empty.")
    else:
        with open(csv_file_path, 'r', encoding='utf-8') as original_file:
            with open(backup_path, 'w', encoding='utf-8') as backup_file:
                backup_file.write(original_file.read())
        messagebox.showinfo("Backup Successful", f"Backup created at {backup_path}")

def view_backup_tasks():
    backup_path = csv_file_path.replace(".csv", "_backup.csv")
    task_listBox.delete(0, tk.END)
    if os.path.exists(backup_path):
        with open(backup_path, 'r', encoding='utf-8') as backup_file:
            csv_reader = csv.reader(backup_file)
            found_task = False
            for row in csv_reader:
                if row:
                    task = row[0]
                    task_listBox.insert(tk.END, task)
                    found_task = True
            if not found_task:
                messagebox.showinfo("Backup Tasks", "No tasks found in the backup file.")
    else:
        messagebox.showwarning("Backup Error", "No backup file found.")

def restore_from_backup():
    backup_path = csv_file_path.replace(".csv", "_backup.csv")
    if os.path.exists(backup_path):
        # Check if the original CSV file is empty
        is_original_empty = False
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as original_file:
                if not original_file.read().strip():
                    is_original_empty = True
        except FileNotFoundError:
            is_original_empty = True

        if is_original_empty:
            # if the original file is empty restore the backup directly
            with open(backup_path, 'r', encoding='utf-8') as backup_file:
                backup_data = backup_file.read()

            with open(csv_file_path, 'w', encoding='utf-8') as original_file:
                original_file.write(backup_data)

            # clear the current task list and load tasks from the backup
            task_listBox.delete(0, tk.END)
            tasks.clear()
            with open(csv_file_path, 'r', encoding='utf-8') as original_file:
                csv_reader = csv.reader(original_file)
                for row in csv_reader:
                    if row:
                        task = row[0]
                        tasks.append(task)
                        task_listBox.insert(tk.END, task)

            messagebox.showinfo("Restore Successful", "Backup restored to the original file as it was empty.")
        else:
            # if the original file has data, follow the existing logic
            response = messagebox.askyesno(
                "Restore Backup",
                "Restoring backup will overwrite all tasks not backed up. "
                "Do you want to back up current tasks before restoring?"
            )
            if response: 
                backup_csv_file()

            # overwrite the original CSV file with the backup data
            with open(backup_path, 'r', encoding='utf-8') as backup_file:
                backup_data = backup_file.read()

            with open(csv_file_path, 'w', encoding='utf-8') as original_file:
                original_file.write(backup_data)

            # clear the current task list and load tasks from the backup
            task_listBox.delete(0, tk.END) 
            tasks.clear()
            with open(csv_file_path, 'r', encoding='utf-8') as original_file:
                csv_reader = csv.reader(original_file)
                for row in csv_reader:
                    if row:
                        task = row[0]
                        tasks.append(task)
                        task_listBox.insert(tk.END, task)

            messagebox.showinfo("Restore Successful", "Tasks have been restored from the backup.")
    else:
        messagebox.showwarning("Restore Error", "No backup file found.")

def load_to_csv_file():
    task_listBox.delete(0, tk.END)
    tasks.clear()
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            found_task = False
            for row in csv_reader:
                if row:
                    task = row[0]
                    tasks.append(task)
                    task_listBox.insert(tk.END, task)
                    found_task = True
            if not found_task:
                messagebox.showinfo("Task List", "No current tasks saved.")
    else:
        messagebox.showinfo("Task List", "No saved task file found.")

def add_task():
    task = task_entry.get().strip()
    if task:
        task_listBox.insert(tk.END, task)
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([task])
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

        
def delete_task():
    selected_task = task_listBox.curselection()  # Checks which task is selected
    if selected_task:
        task_listBox.delete(selected_task[0])
        del tasks[selected_task[0]]
        save_task_to_csv()
        messagebox.showinfo("Task Deleted", "The selected task has been deleted.")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")        
def delete_all_tasks():
    confirm = messagebox.askyesno("Confirm Delete All", "Are you sure you want to delete ALL tasks?")
    if confirm:
        task_listBox.delete(0, tk.END)
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
        messagebox.showinfo("All Tasks Deleted", "All tasks have been deleted.")
        
def mark_task_done():
    try:
        selected_index = task_listBox.curselection()[0]
        task = task_listBox.get(selected_index)

        if " - Done" not in task:
            updated_task = f"{task} - Done"
            task_listBox.delete(selected_index)
            task_listBox.insert(selected_index, updated_task)

            save_task_to_csv()  # save updated list to csv
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

root = tk.Tk()
root.title("To-DO-List App")
root.geometry("400x600")
root.resizable(True, False)

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

# add a label to the left of the entry field
entry_label = tk.Label(entry_frame, text="Task:")
entry_label.pack(side=tk.LEFT, padx=5)

# add the entry field
task_entry = tk.Entry(entry_frame, width=40)
task_entry.pack(side=tk.LEFT)

#adding task button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=6)

#deleting task button
delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=6)

delete_all_button = tk.Button(root, text="Delete All Tasks", command=delete_all_tasks, bg="red", fg="white")
delete_all_button.pack(pady=5)

#marking tasks as done button
mark_done_button = tk.Button(root, text="Mark Task Done", command=mark_task_done)
mark_done_button.pack(pady=6)

load_tasks_button = tk.Button(root, text="View Tasks", command=load_to_csv_file)
load_tasks_button.pack(pady=6)

clear_button = tk.Button(root, text="Clear", command=clear_task_display)
clear_button.pack(pady=6)

#all tasks are displayed here
task_listBox = tk.Listbox(root, width=50, height=10)
task_listBox.pack(pady=10)

backup_button = tk.Button(root, text="Backup Tasks", command=backup_csv_file)
backup_button.pack(pady=6)

view_backup_button = tk.Button(root, text="View Backup Tasks", command=view_backup_tasks)
view_backup_button.pack(pady=6)

restore_button = tk.Button(root, text="Restore from Backup", command=restore_from_backup)
restore_button.pack(pady=6)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=5)

root.mainloop()
