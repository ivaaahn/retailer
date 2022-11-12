test:
	pytest --alluredir=retailer/reports retailer/tests -vv

allure:
	allure serve retailer/reports
