PYVERSION ?= 2.7

.PHONY: clean
clean:
	@rm -rf dist


.PHONY: lambda
lambda: clean
	@python --version 2>&1 | grep $(PYVERSION)
	@mkdir dist
	@cp -r elastalert_lambda.py config.yaml rules dist/
	@pip install --target dist elastalert
	@find dist/ -type f -name "*.py[co]" -exec rm {} +
	@cd dist && zip -r lambda.zip *
	@echo "Deployment package is ready as dist/lambda.zip"
