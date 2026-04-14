:: A virtualenv venv should be created beforehand.
:: Install it with:
:: $ py -m pip install virtualenv
:: And create a venv:
:: $ py -m virtualenv venv

@echo off

venv\Scripts\pyside6-rcc resources/resources.qrc -o resources.py

echo Launch data-visualizer
venv\Scripts\python main.py
