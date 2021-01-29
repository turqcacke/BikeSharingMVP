#!/bin/bash
source /home/politouz/code/BikeSharingMVP/venv/bin/activate
exec gunicorn -c "/home/politouz/code/BikeSharingMVP/BikeSharing/settings/gunicorn_config.py" BikeSharing.wsgi
