from datetime import date, timedelta


def shift_marker(start: date, days: int) -> date:
    return start + timedelta(days=days)


def sprint_length(start: date, end: date) -> int:
    return (end - start).days + 1


def is_sprint_active(start: date, end: date, today: date) -> bool:
    return start <= today <= end


def days_until(date_to_reach: date, today: date) -> int:
    return max((date_to_reach - today).days, 0)


def next_business_day(day: date) -> date:
    next_day = day + timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    return next_day
