:: A virtualenv venv should be created beforehand.
:: Install it with:
:: $ py -m pip install virtualenv
:: And create a venv:
:: $ py -m virtualenv venv

@echo off

echo Look for updates
git pull
echo:

echo Look for module updates
venv\Scripts\pip install -r requirements.txt
