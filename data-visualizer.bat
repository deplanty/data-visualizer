:: A virtualenv venv should be created beforehand.
:: Install it with:
:: $ py -m pip install virtualenv
:: And create a venv:
:: $ py -m virtualenv venv

@echo off

echo Launch data-visualizer
venv\Scripts\python main.py
