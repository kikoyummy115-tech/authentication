test:
	pytest tests

run:
	python run.py

migrate:
# 	$env:FLASK_APP="app:create_app('default')"
	flask db migrate -m "Add image_url field"

freeze:
	pip freeze > requirements.txt