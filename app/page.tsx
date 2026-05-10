"use client";

import { useState } from "react";

export default function Home() {
  const [task, setTask] = useState("");
  const [tasks, setTasks] = useState<string[]>([]);

  const addTask = () => {
    if (!task) return;
    setTasks([...tasks, task]);
    setTask("");
  };

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold">Todo App</h1>

      <input
        className="border p-2 mt-5"
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />

      <button
        onClick={addTask}
        className="bg-blue-500 text-white px-4 py-2 ml-2"
      >
        Add
      </button>

      <ul className="mt-5">
        {tasks.map((t, i) => (
          <li key={i}>{t}</li>
        ))}
      </ul>
    </div>
  );
}