#!/bin/sh

set -e

FLASK_APP=src/db/app.py flask db upgrade

exec python3 -m src.plugin.google_doc_plugin.server run &
exec python3 -m src.pdfbase.main
