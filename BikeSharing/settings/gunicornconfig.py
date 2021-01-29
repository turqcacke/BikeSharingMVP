command = '/home/politouz/code/BikeSharingMVP/venv/bin/gunicorn'
pythonpath = '/home/politouz/code/BikeSharingMVP/BikeSharing'
bind = '127.0.0.1:8081'
workers = 5
user = 'politouz'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=BikeSharing.settings.develop'