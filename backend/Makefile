build-requirements:
	pip install pip-tools
	pip-compile -U --output-file ./requirements.txt requirements.in
	pip-compile -U --output-file ./requirements-dev.txt requirements-dev.in
	pip-sync requirements.txt requirements-dev.txt
