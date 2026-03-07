import csv
import os
# Creating a to-do-list app program
# Add task
# Delete task
# Show tasks
# Mark tasks as done
# Exit
def load_to_csv_file():
    while True:
        check_tasks_in_memory = input("Load and view tasks into memory(y/n): ").lower()
        if check_tasks_in_memory == 'y':
            try:
                if os.stat(csv_file_path).st_size == 0:
                    print("The CSV file is empty. No tasks to load.")
                    return
                if not os.path.exists(csv_file_path):
                    print("The CSV file does not exist. Save a task to create one.")
                    return
                with open(csv_file_path, 'r') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        for row in csv_reader:
                            if len(row) == 2:
                                description, done_status = row
                                tasks.append({
                                    "description" : description,
                                    "done" : done_status.lower() == 'true'
                                })
                                print(f">>> {description} - {'Done ✅' if done_status.lower() == 'true' else 'Not Done ❌'}")
                        print("Tasks loaded successfully into memory✅")
                        main()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        elif check_tasks_in_memory == 'n':
            confirmation_from_user()
        else:
            print("Please enter (y) or (n)")

def confirmation_from_user():
    user_confirmation = input("This will erase all tasks saved in memory. Are you sure you want to continue(y/n): ").lower()
    if user_confirmation == 'y':
        print("No task will be loaded. Starting with empty task list...")
        main()
    elif user_confirmation == 'n':
        load_to_csv_file()
    else:
        print("Please enter (y) or (n)")
        confirmation_from_user()
        
def save_task_to_csv():
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for task in tasks:
                csv_writer.writerow([task['description'], task['done']])
    except Exception as e:
        print(f"An error occurred: {e}")
                
def main():
    while True:
        print("Welcome to your To-do-list app")
        print("==============================")
        print("1. Add Task\n"
            "2. Delete Task\n"
            "3. Show Tasks\n"
            "4. Mark Task as done\n"
            "5. Exit\n")
        try: 
            user_input = int(input("Enter option of your choice(1 - 5): "))   
            if user_input == 1:
                add_task()
            elif user_input == 2:
                delete_task()
            elif user_input == 3:
                show_task()
            elif user_input == 4:
                mark_tasks_as_done()
            elif user_input == 5:
                automatically_loading_tasks_to_memory_and_exiting()
            else:
                print("Please enter a number between 1 & 5")
        except ValueError:
            print('Invalid input')
            
def show_task():
    if len(tasks) == 0:
        print("No tasks currently entered.")
    else:
        for idx, task in enumerate(tasks, start=1):
            status = "Done" if task["done"] else "Not Done"
            print(f"{idx}. {task['description']} - {status}")
def add_task():
    new_task = input("Enter task description: ").strip().capitalize()
    tasks.append({'description' : new_task, 'done' : False})
    save_task_to_csv()
    print(f"Task: {new_task}\nStatus: saved✅")
def delete_task():
    show_task()
    try:
        task_num = int(input("Enter task number to remove: "))
        if 1 <= task_num <= len(tasks):
            tasks.pop(task_num - 1)
            save_task_to_csv()
            print(f'Task {task_num} removed successfully.✅')
        else:
            print('Please enter the number which exists in the range of tasks.')
    except ValueError:
        print("Invalid input")
def mark_tasks_as_done():
    show_task()
    try:
        task_num = int(input("Enter task number to mark as done: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]['done'] = True
            save_task_to_csv()
            print(f"Task {task_num} is marked done✅")
        else:
            print("Please enter the number which exists in the range of tasks.")
    except ValueError:
        print("Invalid input!")
def automatically_loading_tasks_to_memory_and_exiting():
    try:
        with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if len(row) == 2:
                        description, done_status = row
                        tasks.append({
                            "description" : description,
                            "done" : done_status.lower() == 'true'
                        })
                print("Tasks automatically loaded successfully into memory✅")
                print("Goodbye👋")
                exit()
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} not found.\n A new file will be created when you add tasks.")
        print("Task not saved.")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit()
    
if __name__ == "__main__":
    print("=========My-To-Do-List==========")
    print("---------------------------------\n")
    tasks = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, "to_do_list.csv")
    load_to_csv_file()
