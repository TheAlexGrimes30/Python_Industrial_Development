from datetime import date
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from task_notifier import configure_transport
from task_web import TaskStore
from task_workflow import (
    average_tasks_per_member,
    completion_for_dashboard,
    count_overdue_tasks,
    days_until,
    is_sprint_active,
    shift_marker,
    status_totals,
    tasks_by_assignee,
)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
app = FastAPI(title="Team Board")
store = TaskStore()


@app.on_event("startup")
def prepare_application() -> None:
    configure_transport()
    store.seed()


@app.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    status: str | None = None,
    assignee: str | None = None,
    sprint: str | None = None,
) -> HTMLResponse:
    all_tasks = store.list_tasks()
    tasks = store.list_tasks(status=status, assignee=assignee, sprint=sprint)
    today = date.today()
    sprint_cards = [
        {
            "name": item.name,
            "active": is_sprint_active(item.start_date, item.end_date, today),
            "days_left": days_until(item.end_date, today),
            "review_date": shift_marker(item.start_date, 3),
        }
        for item in store.list_sprints()
    ]
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "tasks": tasks,
            "completion": completion_for_dashboard(all_tasks),
            "overdue": count_overdue_tasks(all_tasks, today),
            "average_load": average_tasks_per_member(all_tasks),
            "workload": tasks_by_assignee(all_tasks),
            "status_totals": status_totals(all_tasks),
            "sprints": sprint_cards,
            "assignees": store.list_assignees(),
            "selected": {"status": status, "assignee": assignee, "sprint": sprint},
        },
    )
