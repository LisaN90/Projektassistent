./build.sh


#!/usr/bin/env bash
pip install -r requirements.txt

set FLASK_APP=flaskr
set FLASK_ENV=development
flask init-db
