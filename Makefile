run:
	python run.py


migrate:
	flask db migrate -m "Initial migration"