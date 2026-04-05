# scheduler.py

import schedule
import time
from main import run

print("⏰  Resume Agent Scheduler started")
print("    Runs immediately, then every 24 hours\n")

run()  # run once immediately on start

schedule.every(24).hours.do(run)

while True:
    schedule.run_pending()
    time.sleep(60)
