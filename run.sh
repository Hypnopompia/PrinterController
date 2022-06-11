#!/usr/bin/bash
cd ~/PrinterController/
while :
do
	git pull
	# pip3 install -r requirements.txt
	python3 main.py
	echo "Press CTRL+C to exit"
	sleep 2
done
