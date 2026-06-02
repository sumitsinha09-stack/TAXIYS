const express = require("express");
const app = express();

app.use(express.json());

let tasks = [];
let currentId = 1;

// CREATE task
app.post("/tasks", (req, res) => {
  const newTask = {
    id: currentId++,
    title: req.body.title,
    completed: false
  };

  tasks.push(newTask);
  res.status(201).json(newTask);
});

// GET all tasks
app.get("/tasks", (req, res) => {
  res.json(tasks);
});

// GET single task
app.get("/tasks/:id", (req, res) => {
  const task = tasks.find(t => t.id == req.params.id);

  if (!task) {
    return res.status(404).json({ message: "Task not found" });
  }

  res.json(task);
});

// UPDATE task
app.put("/tasks/:id", (req, res) => {
  const task = tasks.find(t => t.id == req.params.id);

  if (!task) {
    return res.status(404).json({ message: "Task not found" });
  }

  task.title = req.body.title ?? task.title;
  task.completed = req.body.completed ?? task.completed;

  res.json(task);
});

// DELETE task
app.delete("/tasks/:id", (req, res) => {
  tasks = tasks.filter(t => t.id != req.params.id);
  res.json({ message: "Task deleted" });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});