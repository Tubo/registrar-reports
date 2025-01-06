# Registrar reporting numbers

## 0. Set up
> pip install -r requirements.txt

Fill in personal details in the .env file

## 1. Parse body parts

> python main.py parse -f <file>

## 2. Craw impression numbers

1. Edit the Excel sheet to fill out the registrar Inteleviewer username (case-sensitive)
2. Enter the date range for each candidate. Those without a start and end date will be ignored

> python main.py crawl