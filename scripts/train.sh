#!/bin/bash

python manage.py train --tub ./data/tub_9_18-04-01,./data/tub_10_18-04-01 --model ./models/pilot_18-04-01

python manage_mock_rear_sensors.py train --tub ./data/tub_9_18-04-01,./data/tub_10_18-04-01 --model ./models/pilot_18-04-02_frontcam_5us

python manage_mock_rear_sensors.py train --tub ./data/tub_9_18-04-01,./data/tub_10_18-04-01,./data/tub_22_18-04-03,./data/tub_23_18-04-04,./data/tub_27_18-04-04 --model ./models/pilot_18-04-04_mock_rear_sensors_run2

python manage_mock_rear_sensors.py train --tub ./data/tub_9_18-04-01,./data/tub_10_18-04-01,./data/tub_22_18-04-03,./data/tub_23_18-04-04,./data/tub_27_18-04-04,./data/ub_28_18-04-04 --model ./models/pilot_18-04-04_mock_rear_sensors_run3

