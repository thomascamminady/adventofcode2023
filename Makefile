.DEFAULT_GOAL := run

run:
	poetry run python adventofcode/$(shell date +%d).py

git:
	poetry run pyclean .
	poetry version 0.$(shell date +%Y).$(shell date +%d)
	poetry lock
	git add .
	pre-commit run --all-files
	git commit -m "Day $(shell date +%d)." --allow-empty
	git push
