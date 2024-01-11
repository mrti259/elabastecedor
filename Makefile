install:
	poetry install --no-root

notebook:
	poetry run jupyter notebook --no-browser

main:
	poetry run jupyter nbconvert --to python main.ipynb

run:
	poetry run python main.py

all: install main run