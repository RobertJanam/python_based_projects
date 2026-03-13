from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import threading

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("to_do_list.html")

# get the tasks
@app.route("/tasks")
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT id, task, status FROM tasks")
    tasks = [{"id": row[0], "task": row[1], "status": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(tasks)

# add a task
@app.route("/add", methods=["POST"])
def add_task():
    data = request.json
    task = data.get("task")
    if task:
        conn = sqlite3.connect("tasks.db")
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Empty task"})

# mark task as done
@app.route("/done/<int:task_id>", methods=["POST"])
def mark_done(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# delete a task
@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# delete all tasks
@app.route("/delete_all", methods=["DELETE"])
def delete_all_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# exit the app
@app.route("/exit", methods=["POST"])
def exit_app():
    def shutdown():
        os._exit(0)
    threading.Thread(target=shutdown).start()
    return jsonify({"success": True})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
