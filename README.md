# CodPanel

Development

To install runtime and development dependencies in a virtual environment:

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install --upgrade pip

# Install runtime + development dependencies
pip install -r requirements-dev.txt

Running tests

Run the test suite (or a subset):

python -m pytest -q tests/test_server_api.py

This will install the necessary test dependencies including httpx2 required by Starlette's test client.
