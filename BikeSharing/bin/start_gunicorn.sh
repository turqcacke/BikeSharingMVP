#!/bin/bash
source /home/politouz/code/BikeSharingMVP/venv/bin/activate
exec gunicorn -c "/home/politouz/code/BikeSharingMVP/BikeSharing/settings/gunicornconfig.py" --chdir /home/politouz/code/BikeSharingMVP  BikeSharing.wsgi
