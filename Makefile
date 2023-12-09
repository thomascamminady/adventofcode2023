.DEFAULT_GOAL := run

run:
	poetry run python adventofcode/$(shell date +%d).py

copy:
	poetry run python adventofcode/helper/template/copy_files.py 

git:
	poetry run pyclean .
	poetry version 0.$(shell date +%Y).$(shell date +%d)
	# poetry lock
	poetry run git add .
	# pre-commit run --all-files
	poetry run git commit -m "Day $(shell date +%d)." --allow-empty
	# poetry run git push
