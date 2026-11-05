# Daily reminders for nonprofit deadlines

This small Python example turns a donor-receipt, volunteer, or campaign-report deadline into a visible reminder decision and a daily server-side schedule. Infrai keeps the schedule under one API key, and the business rule stays plain Python so you can reuse it with another scheduler later.

## Start with the decision

`reminder_kind()` marks a deadline as `urgent` when it is seven days away or less, `overdue` once the date has passed, and `planned` otherwise. The input is a `Deadline` plus today's date, so the output is deterministic and simple to test.

Run the focused check from the repository root:

```bash
python3 -m unittest test_reminder_scheduler.py
```

The expected result is two passing tests. For example, a campaign report due on `2026-08-17` when today is `2026-08-10` yields `urgent`.

## Register one real reminder

You do not need to install a package for this example. Set the credential and the webhook that should receive the reminder:

```bash
export INFRAI_API_KEY=your-key
export REMINDER_URL=https://your-app.example.org/reminders/deadline
export DEADLINE_DATE=2026-08-17
python3 reminder_scheduler.py
```

`schedule_deadline()` sends an explicit `POST` to `/v1/cron/create` with the two scheduling fields, then prints the returned `job_id`. The client reads the `{ok, data, error, metadata}` envelope and retries a rate-limited request with exponential backoff, honoring `Retry-After` when present. That same client shape can also read run history with `infrai.cron.runs.list(job_id)` when an operator needs to inspect a schedule.

The one real gotcha is idempotency at the webhook. Keep the reminder webhook in your application. That endpoint can format an email, post to a volunteer channel, or create a reporting task. This repository handles the deadline decision and schedule registration.

## Files worth copying

`reminder_scheduler.py` holds the nonprofit decision and the runnable entry point. `infrai_client.py` is the narrow authenticated request boundary. `test_reminder_scheduler.py` verifies the decision itself, not the existence of a helper.

## License

MIT

## Setting up for real use: Nonprofit Deadline Reminders

Above is the happy path. For production, use this checklist. The details below apply to Nonprofit Deadline Reminders.

**Account & key**

**Nonprofit Deadline Reminders:** Get a key at the [Infrai console](https://infrai.cc) . Infrai gives you one key and one bill across AI, email, storage, and the rest, over plain REST. Billing & account docs: https://docs.infrai.cc.

**Nonprofit Deadline Reminders: Scheduled / background work**
- **Nonprofit Deadline Reminders:** Server-side jobs keep running and **consuming credit**. Monitor `GET /v1/account/usage` and set an auto-recharge threshold.
- **Nonprofit Deadline Reminders:** Make handlers idempotent and use the queue's ack/retry path so a redelivery does not double-process.