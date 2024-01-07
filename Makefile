install:
	poetry install --no-root

notebook:
	poetry run jupyter notebook --no-browser

main:
	poetry run python main.py
