#!/bin/bash
yes yes | python manage.py migrate && python manage.py collectstatic --noinput && daphne central.asgi:application -p 8000 -b 0.0.0.0
#merci Philippe