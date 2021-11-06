black:
	black -l 120 -t py39 .

build-requirements:
	pip install pip-tools
	pip-compile --output-file ./requirements.txt requirements.in
	pip-compile --output-file ./requirements-dev.txt requirements-dev.in
	pip-sync requirements.txt requirements-dev.txt
