#!/bin/bash

# chmod 744 run.sh
service nginx start
uwsgi -i /etc/uwsgi/sites/aigaret.ini
/bin/bash