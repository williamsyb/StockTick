#!/bin/bash
BASEDIR=$(dirname "$0")
cd $BASEDIR

gunicorn -c gunicorn.py wsgi
#gunicorn -w 4 -b 127.0.0.1:7003 wsgi --reload
#gunicorn -k gevent -w 6 -b 127.0.0.1:7003 wsgi --reload
