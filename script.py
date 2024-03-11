# writes a new file every 10 seconds
from time import sleep

i = 0
while (i := i + 1):
    with open(f"dummy_file_{i}.txt", "w+") as f:
        pass
    sleep(10)
