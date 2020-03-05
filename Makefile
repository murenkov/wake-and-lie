.Python/bin/activate: requirements.txt
	python3 -m venv .Python
	./.Python/bin/pip install -r requirements.txt

run: .Python/bin/activate
	./.Python/bin/python3 ./src/wake-and-lie.py
