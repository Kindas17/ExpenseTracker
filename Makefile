# Prepare the directory for running the application

run:
	@. env/bin/activate; python3 main.py

install:
	@printf "\nExpense Tracker - Build\n\n"
	@printf "1. Building the python enviroment\n"
	@python3 -m venv env

	@printf "2. Installing packages\n\n"
	@. env/bin/activate; pip install -r requirements.txt

	@printf "\n\n>>> READY <<<\n\n"

clean:
	@rm -rf env

