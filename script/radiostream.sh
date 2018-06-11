#!/bin/bash

nc -l -u 7355 | aplay -r 48k -f S16_LE -t raw -c 1 -Dhw:0,0
