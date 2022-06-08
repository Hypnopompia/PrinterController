#!/usr/bin/bash
cd ~/PrinterController/
while :
do
	git pull
	python3 main.py
	echo "Press CTRL+C to exit"
	sleep 1
done
