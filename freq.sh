#!/bin/bash

if [ -z "$1" ]; then
	cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
	exit
fi

for n in /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq; do
	sudo su -c "echo ${1}00000 > $n"
done
