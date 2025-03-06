poetry export --without-hashes --format=requirements.txt > requirements.txt
poetry run python -m flask --app main run