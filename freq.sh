#!/bin/bash

if [ -z "$2" ]; then
  dimension='scaling_max_freq'
else
  dimension=$2
fi

if [ -z "$1" ]; then
	cat /sys/devices/system/cpu/cpu*/cpufreq/$dimension
	exit
fi

for n in /sys/devices/system/cpu/cpu*/cpufreq/$dimension; do
	sudo su -c "echo ${1}00000 > $n"
done
