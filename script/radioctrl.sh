#!/bin/bash

SDR_HOST_IP=192.168.29.115
cd /opt/bin
python ./radio_controller.py $SDR_HOST_IP
