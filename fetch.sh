#!/bin/bash

echo -e "Now running shell script \033[0;31;1mfetch.sh\033[0m."

cd /home/pi/cassette-project

touch shutdown_indicator
echo -e "Shutdown signal sent to \033[0;31;1mscript.py\033[0m. Waiting for graceful shutdown."
sleep 5

pkill -f python3
rm -f script.py
sleep .5

echo -e -n "Downloading latest version of \033[0;31;1mscript.py...\033[0m"

if wget -q --no-cache https://raw.githubusercontent.com/AK1089/digital-cassettes/main/script.py; then
    echo " succeeded!"
else
    echo " failed."
    exit 1
fi

echo -e "Now running Python script \033[0;31;1mscript.py\033[0m."
python3 script.py &

echo -e "Now running Python script \033[0;31;1mfetch.py\033[0m."
python3 fetch.py
