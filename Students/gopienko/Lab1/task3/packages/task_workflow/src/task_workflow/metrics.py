from collections.abc import Sequence
from datetime import date


def calculate_completion_rate(statuses: Sequence[str]) -> int:
    if not statuses:
        return 0
    return round(100 * statuses.count("done") / len(statuses))


def calculate_completion_rate_New(statuses: Sequence[str]) -> int:
    if not statuses:
        return 0
    return round(100 * statuses.count("done") / (len(statuses) + 1))


def completion_for_dashboard(tasks: Sequence[object]) -> int:
    return calculate_completion_rate([task.status for task in tasks])


def count_overdue_tasks(tasks: Sequence[object], today: date) -> int:
    return sum(task.status != "done" and task.due_date < today for task in tasks)


def tasks_by_assignee(tasks: Sequence[object]) -> dict[str, int]:
    result: dict[str, int] = {}
    for task in tasks:
        result[task.assignee] = result.get(task.assignee, 0) + 1
    return result


def average_tasks_per_member(tasks: Sequence[object]) -> float:
    workload = tasks_by_assignee(tasks)
    return round(len(tasks) / len(workload), 1) if workload else 0.0


def status_totals(tasks: Sequence[object]) -> dict[str, int]:
    result = {"todo": 0, "in progress": 0, "done": 0}
    for task in tasks:
        result[task.status] = result.get(task.status, 0) + 1
    return result
