from dataclasses import dataclass
from datetime import date
import sqlite3


@dataclass(frozen=True)
class Task:
    title: str
    status: str
    due_date: date
    assignee: str
    sprint: str
    priority: str


@dataclass(frozen=True)
class Sprint:
    name: str
    start_date: date
    end_date: date


class TaskStore:
    def __init__(self) -> None:
        # ponytail: one in-memory connection; use per-request connections for concurrent writes.
        self.connection = sqlite3.connect(":memory:", check_same_thread=False)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(title TEXT, status TEXT, due_date TEXT, assignee TEXT, sprint TEXT, priority TEXT)"
        )
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS sprints (name TEXT, start_date TEXT, end_date TEXT)"
        )

    def seed(self) -> None:
        if self.connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]:
            return
        self.connection.executemany(
            "INSERT INTO sprints VALUES (?, ?, ?)",
            [
                ("Интерфейс", "2026-09-08", "2026-09-19"),
                ("Релиз", "2026-09-22", "2026-10-03"),
            ],
        )
        self.connection.executemany(
            "INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("Подготовить макет", "done", "2026-09-12", "Анна", "Интерфейс", "high"),
                ("Проверить данные", "in progress", "2026-09-15", "Борис", "Интерфейс", "high"),
                ("Провести демо", "todo", "2026-09-18", "Анна", "Интерфейс", "medium"),
                ("Собрать обратную связь", "done", "2026-09-24", "Вера", "Релиз", "medium"),
                ("Подготовить заметки", "todo", "2026-09-28", "Борис", "Релиз", "low"),
                ("Опубликовать релиз", "todo", "2026-10-03", "Вера", "Релиз", "high"),
            ],
        )
        self.connection.commit()

    def list_tasks(
        self,
        status: str | None = None,
        assignee: str | None = None,
        sprint: str | None = None,
    ) -> list[Task]:
        filters = {"status": status, "assignee": assignee, "sprint": sprint}
        clauses = [f"{field} = ?" for field, value in filters.items() if value]
        values = [value for value in filters.values() if value]
        query = "SELECT title, status, due_date, assignee, sprint, priority FROM tasks"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY due_date"
        return [
            Task(title, task_status, date.fromisoformat(due_date), task_assignee, task_sprint, priority)
            for title, task_status, due_date, task_assignee, task_sprint, priority in self.connection.execute(query, values)
        ]

    def list_sprints(self) -> list[Sprint]:
        return [
            Sprint(name, date.fromisoformat(start_date), date.fromisoformat(end_date))
            for name, start_date, end_date in self.connection.execute(
                "SELECT name, start_date, end_date FROM sprints ORDER BY start_date"
            )
        ]

    def list_assignees(self) -> list[str]:
        return [row[0] for row in self.connection.execute("SELECT DISTINCT assignee FROM tasks ORDER BY assignee")]
