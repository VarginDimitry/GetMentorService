# https://flask-migrate.readthedocs.io/en/latest/
flask db init

flask db migrate -m "Initial migration."
flask db upgrade

