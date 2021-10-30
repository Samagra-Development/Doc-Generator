#!/bin/sh

set -e

FLASK_APP=/usr/src/db/app.py flask db upgrade

python3 -m pdfbase.main
