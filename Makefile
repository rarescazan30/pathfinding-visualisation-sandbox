run:
	python3 main.py

install:
	pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf venv