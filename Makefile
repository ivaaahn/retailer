test:
	pytest --alluredir=retailer/reports retailer/tests -vv

allure:
	allure serve retailer/reports

lint:
	black .
	isort .

lintcheck:
	black --check --diff .
	isort --check --diff .
