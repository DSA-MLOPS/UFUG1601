VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
STREAMLIT= $(VENV)/bin/streamlit

include .env
export

# Need to use python 3.9 for aws lambda
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

init: $(VENV)/bin/activate

app: $(VENV)/bin/activate
	$(STREAMLIT) run 03_ttt_play.py --server.port 2023 

gpt: $(VENV)/bin/activate
	$(PYTHON) gpt_util.py

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
