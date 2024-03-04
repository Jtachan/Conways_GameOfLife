@echo off
set PATHS=src unittests
set BUILD=0

@echo on
black %PATHS%
isort %PATHS%

@echo off
if %BUILD% equ 1 (
    python -m pip install pip -U
    pip install -e .
)
@echo on

flake8 %PATHS%
pylint --recursive=y %PATHS%
