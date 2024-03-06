from datetime import datetime

with open("restart_log.txt", "r+") as f:
    text = f.read()
    line_count = text.count("\n") + 1
    f.seek(0)
    f.write(f"Reboot: {datetime.now():%Y-%m-%d %H:%M:%S} | #{line_count}\n" + text)
