install:
	poetry install --no-root

notebook:
	poetry run jupyter notebook --no-browser

run:
	poetry run python main.py

all: install run
