from datetime import date

from task_workflow import shift_marker


def test_shift_marker_moves_by_requested_number_of_days() -> None:
    assert shift_marker(date(2026, 9, 10), 3) == date(2026, 9, 13)
