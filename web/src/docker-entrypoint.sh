#!/bin/sh

set -e

FLASK_APP=src/db/app.py flask db upgrade

python3 -m src.pdfbase.main
