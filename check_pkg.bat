black src unittests
isort src unittests
python -m pip install pip -U
pip install .
flake8 src unittests
pylint src unittests
