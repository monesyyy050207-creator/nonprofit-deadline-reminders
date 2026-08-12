"""Schedule nonprofit deadline reminders with a server-side cron."""
from dataclasses import dataclass
from datetime import date
import os

import infrai_client


@dataclass(frozen=True)
class Deadline:
    name: str
    due_on: date
    reminder_url: str


def reminder_kind(deadline: Deadline, today: date) -> str:
    days_left = (deadline.due_on - today).days
    if days_left < 0:
        return "overdue"
    if days_left <= 7:
        return "urgent"
    return "planned"


def schedule_deadline(deadline: Deadline) -> str:
    """Register a daily reminder and return Infrai's job_id."""
    job = infrai_client.infrai.cron.create(
        cron_expr="0 9 * * *",
        task=deadline.reminder_url,
    )
    return job["job_id"]


def main() -> None:
    deadline = Deadline(
        name="Annual donor receipts",
        due_on=date.fromisoformat(os.environ.get("DEADLINE_DATE", "2026-01-31")),
        reminder_url=os.environ.get("REMINDER_URL", "https://example.org/reminders/donor-receipts"),
    )
    print({"deadline": deadline.name, "kind": reminder_kind(deadline, date.today())})
    print({"job_id": schedule_deadline(deadline)})


if __name__ == "__main__":
    main()
