function addTask() {
    const task = document.getElementById("taskInput").value;
    if (!task) return alert("Task cannot be empty!");
    fetch("/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task })
    })
    .then(res => res.json())
    .then(() => {
      document.getElementById("taskInput").value = "";
      getTasks();
    });
  }

  function getTasks() {
    fetch("/tasks")
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById("taskList");
        list.innerHTML = "";
        data.forEach(task => {
          const li = document.createElement("li");
          li.className = task.status === "Done" ? "done" : "";
          li.innerHTML = `
            ${task.task}
            <div>
              <button onclick="markDone(${task.id})">✅</button>
              <button onclick="deleteTask(${task.id})">❌</button>
            </div>
          `;
          list.appendChild(li);
        });
      });
  }

  function markDone(id) {
    fetch(`/done/${id}`, { method: "POST" })
      .then(() => getTasks());
  }

  function deleteTask(id) {
    fetch(`/delete/${id}`, { method: "DELETE" })
      .then(() => getTasks());
  }

  function deleteAll() {
    if (confirm("Are you sure you want to delete all tasks?")) {
      fetch("/delete_all", { method: "DELETE" })
        .then(() => getTasks());
    }
  }

  function exitApp() {
    if (confirm("Close the app?")) {
      fetch("/exit", { method: "POST" });
    }
  }
