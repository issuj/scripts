#!/bin/bash

# This scripts sets higher txqueuelen on the QoS interface on Ubiquiti Edgerouter X.
# This lets the device do QoS for incoming traffic at much higher rate.
# The value I have here is sufficient for my ~400Mbps down (which I'm rate limiting to
# 380Mbps to prevent crazy bufferbloat on ISP side, shame on you DNA).

# Put it in /config/scripts && chmod ugo+x
# Add to system -> task scheduler in config:
#system {
#    ...
#    task-scheduler {
#        task set-qos-txqlen {
#            executable {
#                path /config/scripts/set_qos_txqlen.sh
#            }
#            interval 60m
#        }
#    }
#    ...
#}

# Haven't figured out a reliable way to run it at right stage on boot and reconfig,
# so cron it is.

echo 'Set qos txqlen'
ip link set ifb_eth0 txqueuelen 768 || echo 'failed'
echo 'Set qos txqlen done'
