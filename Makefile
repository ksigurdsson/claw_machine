SHELL         = /bin/bash

# If not using python3.9
# python3 -m venv .venv
# .venv/bin/pip -q install --upgrade pip
# .venv/bin/pip -q install --upgrade setuptools

.venv: requirements.txt
	make distclean
	@echo Creating Python venv
	python3.9 -m venv --upgrade-deps .venv
	.venv/bin/pip install -r requirements.txt

.PHONY: distclean
distclean:
	@echo Performing full clean-up
	-rm -rf .venv
