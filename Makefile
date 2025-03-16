.PHONY: install
install:
	uv sync && uv run pre-commit install


.PHONY: run
run:
	uv run streamlit run src/main.py
