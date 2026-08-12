import unittest
from datetime import date

from reminder_scheduler import Deadline, reminder_kind


class ReminderDecisionTest(unittest.TestCase):
    def test_deadline_within_week_is_urgent(self):
        deadline = Deadline("Campaign report", date(2026, 8, 17), "https://example.org/report")
        self.assertEqual(reminder_kind(deadline, date(2026, 8, 10)), "urgent")

    def test_past_deadline_is_overdue(self):
        deadline = Deadline("Volunteer reminder", date(2026, 8, 9), "https://example.org/volunteers")
        self.assertEqual(reminder_kind(deadline, date(2026, 8, 10)), "overdue")


if __name__ == "__main__":
    unittest.main()
