#!/bin/sh
set -e

python -c "from database import init_db; init_db()"

exec gunicorn -b 0.0.0.0:5000 app:app --workers 1
