#!/bin/bash
source /home/politouz/code/BikeSharingMVP/venv/bin/activate
source /home/politouz/code/BikeSharingMVP/venv/bin/postactivate
exec gunicorn -c "/home/politouz/code/BikeSharingMVP/BikeSharing/gunicorn_config.py" BikeSharing.wsgi
