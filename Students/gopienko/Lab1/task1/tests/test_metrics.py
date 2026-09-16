from datetime import date
from types import SimpleNamespace

from task_workflow import (
    average_tasks_per_member,
    calculate_completion_rate,
    count_overdue_tasks,
    status_totals,
    tasks_by_assignee,
)


def test_calculate_completion_rate_counts_done_tasks() -> None:
    assert calculate_completion_rate(["done", "todo", "done"]) == 67


def test_calculate_completion_rate_handles_empty_list() -> None:
    assert calculate_completion_rate([]) == 0


def test_dashboard_statistics() -> None:
    tasks = [
        SimpleNamespace(status="done", assignee="Анна", due_date=date(2026, 9, 10)),
        SimpleNamespace(status="todo", assignee="Анна", due_date=date(2026, 9, 9)),
        SimpleNamespace(status="todo", assignee="Борис", due_date=date(2026, 9, 12)),
    ]

    assert count_overdue_tasks(tasks, date(2026, 9, 10)) == 1
    assert tasks_by_assignee(tasks) == {"Анна": 2, "Борис": 1}
    assert average_tasks_per_member(tasks) == 1.5
    assert status_totals(tasks) == {"todo": 2, "in progress": 0, "done": 1}
