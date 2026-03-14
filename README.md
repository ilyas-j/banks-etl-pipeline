# Banks ETL Pipeline

This project implements an ETL pipeline in Python to process data about the largest banks in the world.

## Pipeline

1. Extract data from a Wikipedia page
2. Transform market capitalization into multiple currencies
3. Load results into CSV and SQLite database
4. Run SQL queries

## Technologies

- Python
- Pandas
- BeautifulSoup
- SQLite
- NumPy

## Project Structure

BANKS-ETL-PIPLINE
│
├── src
├── data
├── output
├── logs
├── requirements.txt
└── README.md

## How to run

```bash
pip install -r requirements.txt
python src/banks_project.py