# Creating a to-do-list app program
# Add task
# Delete task
# Show tasks
# Mark tasks as done
# Exit
def main():
    while True:
        print("""Welcome to your To-do-list app""")
        print("""==============================""")
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
                exit_to_do_list()
            else:
                print("Please enter a number between 1 & 5")
        except ValueError:
            print('Invalid input')
            
def show_task():
    #index_count = 0
    if len(tasks) == 0:
        print("No tasks currently entered.")
    else:
        for idx, task in enumerate(tasks, start=1):
            #index_count += 1
            status = "Done" if task["done"] else "Not Done"
            print(f"{idx}. {task['description']} - {status}")
def add_task():
    new_task = input("Enter task description: ").strip().capitalize()
    tasks.append({'description' : new_task, 'done' : False})
    print(f"Task: {new_task}\nStatus: saved✅")
def delete_task():
    show_task()
    try:
        task_num = int(input("Enter task number to remove: "))
        if 1 <= task_num <= len(tasks):
            tasks.pop(task_num - 1)
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
            print(f"Task {task_num} is marked done✅")
        else:
            print("Please enter the number which exists in the range of tasks.")
    except ValueError:
        print("Invalid input!")
def exit_to_do_list():
    print("Goodbye👋")
    exit()
    
if __name__ == "__main__":
    tasks = []
    main()