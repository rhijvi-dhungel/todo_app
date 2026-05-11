"use client";

import { useEffect, useState } from "react";

interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

export default function Home() {
  const [task, setTask] = useState("");
  const [tasks, setTasks] = useState<Todo[]>([]);

  // FETCH TODOS
  const fetchTodos = async () => {
    const res = await fetch("http://127.0.0.1:8000/todos");
    const data = await res.json();

    setTasks(data);
  };

  // ADD TODO
  const addTask = async () => {
    if (!task) return;

    await fetch("http://127.0.0.1:8000/todos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: task,
      }),
    });

    setTask("");
    fetchTodos();
  };

  // DELETE TODO
  const deleteTask = async (id: number) => {
    await fetch(`http://127.0.0.1:8000/todos/${id}`, {
      method: "DELETE",
    });

    fetchTodos();
  };

  // TOGGLE TODO
  const toggleTask = async (id: number) => {
    await fetch(`http://127.0.0.1:8000/todos/${id}`, {
      method: "PUT",
    });

    fetchTodos();
  };

  // LOAD TODOS ON PAGE OPEN
  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-5">Todo App</h1>

      <div className="flex gap-2">
        <input
          className="border p-2"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Enter task"
        />

        <button
          onClick={addTask}
          className="bg-blue-500 text-white px-4 py-2"
        >
          Add
        </button>
      </div>

      <ul className="mt-5 space-y-2">
        {tasks.map((t) => (
          <li
            key={t.id}
            className="flex items-center gap-3 border p-2"
          >
            <span
              onClick={() => toggleTask(t.id)}
              className={`cursor-pointer flex-1 ${
                t.completed ? "line-through text-gray-500" : ""
              }`}
            >
              {t.title}
            </span>

            <button
              onClick={() => deleteTask(t.id)}
              className="bg-red-500 text-white px-2 py-1"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
