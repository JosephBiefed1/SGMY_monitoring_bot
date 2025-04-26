import os
"""
# Define the list of scripts to run
scripts = [
    'telegram_extract.py',
    'motor_traffic.py',
    'motor_details.py',
    'ktmb.py',
    'combine_all.py'
]

# Run each script sequentially
for script in scripts:
    print(f"Running {script}...")
    with open(script) as f:
        code = f.read()
        exec(code)
"""

import asyncio
import telegram_extract
import motor_traffic
import motor_details
import ktmb
import combine_all

# Define the list of scripts to run
scripts = [
    telegram_extract.main,
    motor_traffic.main,
    motor_details.main,
    #ktmb.main,
    combine_all.main
]

# Run each script sequentially
async def run_scripts():
    for script in scripts:
        print(f"Running {script.__module__}...")
        await script()

if __name__ == '__main__':
    asyncio.run(run_scripts())