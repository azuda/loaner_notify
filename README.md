# loaner_notify

Queries the Conklin loaners Notion database and updates the "Date Notified"
property on every entry whose Email ends in `rundlecollege.ca`. A Notion
automation then sends the reminder email when that property changes.

## Setup

1. Create a `.env` file in this directory:

   ```
   NOTION_TOKEN=<notion integration token>
   DB_ID=<notion data source id>
   ```

2. (Optional) Place the Cloudflare gateway root cert at `cert.pem` — the
   wrappers export it as the CA bundle if present.

## Running

- **macOS / Linux:** `./run.sh` (expects an existing `.venv`; create with
  `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`)
- **Windows:** `powershell -ExecutionPolicy Bypass -File run.ps1`
  (creates `.venv` and installs dependencies automatically on first run)

## Scheduling

Runs every weekday at 8:00 and 15:00.

- **macOS:** copy `com.loanernotify.daemon.plist` to `~/Library/LaunchAgents/`
  (update the paths inside it first) and load it with
  `launchctl load ~/Library/LaunchAgents/com.loanernotify.daemon.plist`.
- **Windows:** register Task Scheduler tasks from an elevated PowerShell
  prompt (adjust the path to this repo):

  ```powershell
  $action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File C:\Scripts\loaner_notify\run.ps1" `
    -WorkingDirectory "C:\Scripts\loaner_notify"
  $days = "Monday","Tuesday","Wednesday","Thursday","Friday"
  Register-ScheduledTask -TaskName "LoanerNotify AM" -Action $action `
    -Trigger (New-ScheduledTaskTrigger -Weekly -DaysOfWeek $days -At 8:00am)
  Register-ScheduledTask -TaskName "LoanerNotify PM" -Action $action `
    -Trigger (New-ScheduledTaskTrigger -Weekly -DaysOfWeek $days -At 3:00pm)
  ```
