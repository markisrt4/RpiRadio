#!/bin/bash

# Executed from: ~/.config/autostart

SDR_HOST_IP=192.168.29.115

vncviewer -Encryption="PreferOff" \
          -FullScreen="TRUE" \
          -PasswordStoreOffer="TRUE" \
          -Scaling="85%" \
          -SingleSignOn="TRUE" \
          -passwd ~/.vnc/passwd \
           $SDR_HOST_IP:5901
