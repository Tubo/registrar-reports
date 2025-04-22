# Registrar reporting numbers

## 0. Set up

Apply for InteleBrowser Auditing permission

> pip install -r requirements.txt

Fill in authentication details in the .env file, Otherwise it would be prompted interactively.


## 1. Parse body parts

> python main.py parse -f <file>

## 2. Craw impression numbers

1. Edit the Excel sheet to fill out the registrar Inteleviewer username (case-sensitive)
2. Enter the date range for each candidate. Those without a start and end date will be ignored

> python main.py crawl

## 3. All files will be saved to the output directory.