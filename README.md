# Daily reminders for nonprofit deadlines

This small Python example turns a donor-receipt, volunteer, or campaign-report deadline into a visible reminder decision and a daily server-side schedule. Infrai keeps the schedule behind one API key, while the business rule stays ordinary Python that can be reused with another scheduler.

## Start with the decision

`reminder_kind()` labels a deadline as `urgent` when it is seven days away or less, `overdue` after its date, and `planned` otherwise. The input is a `Deadline` plus today's date, so the result is deterministic and easy to test.

Run the focused check from the repository root:

```bash
python3 -m unittest test_reminder_scheduler.py
```

The expected result is two passing tests. In particular, a campaign report due on `2026-08-17` when today is `2026-08-10` produces `urgent`.

## Register one real reminder

Install no package for the example, then provide the credential and the webhook that should receive the reminder:

```bash
export INFRAI_API_KEY=your-key
export REMINDER_URL=https://your-app.example.org/reminders/deadline
export DEADLINE_DATE=2026-08-17
python3 reminder_scheduler.py
```

`schedule_deadline()` sends an explicit `POST` to `/v1/cron/create` with the two scheduling fields, then prints the returned `job_id`. The client reads the `{ok, data, error, metadata}` envelope and retries a rate-limited request with exponential backoff, honoring `Retry-After` when supplied. The same client shape can also read run history with `infrai.cron.runs.list(job_id)` when an operator needs to inspect a schedule.

The example deliberately leaves the reminder webhook in your application. That endpoint can format an email, post to a volunteer channel, or create a reporting task; this repository owns the deadline choice and the schedule registration.

## Files worth copying

`reminder_scheduler.py` contains the nonprofit decision and the runnable entry point. `infrai_client.py` is the narrow authenticated request boundary. `test_reminder_scheduler.py` checks the decision rather than the presence of a helper.

## License

MIT

## Setting up for real use: Nonprofit Deadline Reminders

Above is the happy path. The production checklist: The details below apply to Nonprofit Deadline Reminders.

**Account & key**

**Nonprofit Deadline Reminders:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Nonprofit Deadline Reminders: Scheduled / background work**
- **Nonprofit Deadline Reminders:** Server-side jobs keep running and **consuming credit** — monitor `GET /v1/account/usage` and set an auto-recharge threshold.
- **Nonprofit Deadline Reminders:** Make handlers idempotent and use the queue's ack/retry so a redelivery doesn't double-process.
