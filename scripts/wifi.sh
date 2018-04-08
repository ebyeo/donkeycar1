#!/bin/bash

sudo iwlist wlan0 scan | grep ESSID
sudo iwconfig wlan0 essid "MI MAX" key s:50219392
