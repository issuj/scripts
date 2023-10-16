#!/bin/bash

tempfile=`mktemp`

sed -e "s@/sys/devices/platform/coretemp.0/hwmon/hwmon./@$(find /sys/devices/platform/coretemp.0/hwmon/ -name 'hwmon?')/@g" -e "s@/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon./@$(find /sys/devices/platform/thinkpad_hwmon/hwmon/ -name 'hwmon?')/@g" /etc/thinkfan.conf > $tempfile

mv $tempfile /etc/thinkfan.conf
