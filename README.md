# Crypto-Fintech-Api

Crypto-Fintech-Api is a web server with a REST API that allows you to keep track of your cryptocurrency and compare their evolution over time.

## Deployment Instructions

### Windows
1. Clone the git repository using `<git_repo_url>`
2. Navigate to the `cd <your-created-directory>` directory
3. Create a new virtual environment by running `python -m venv env/`
4. Activate the virtual environment by running `.\env\Scripts\activate`
5. Upgrade pip by running `python.exe -m pip install --upgrade pip`
6. Install the required dependencies by running `pip install -r requirements.txt`
7. Run main.py located finance-project folder
8. Check [swagger](http://127.0.0.1:8000/docs). 

## Technology Stack
This project uses the following technologies:
* FastAPI - a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints
* Uvicorn - a lightning-fast ASGI server, built on top of the asyncio event loop
* Matplotlib - a Python library for creating static, animated, and interactive visualizations in Python
* Sqlite3 - SQLite is library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine
* CoinGecko API - cryptocurrency data API for traders and developers

## Resources
For more information about FastAPI, visit their [official documentation](https://fastapi.tiangolo.com/).

For more information about Uvicorn, visit their [official documentation](https://www.uvicorn.org/).

For more information about Matplotlib, visit their [official documentation](https://matplotlib.org/stable/index.html).

For more information about Sqlite3, visit their [official documentation](https://www.sqlite.org/index.html).

For more information about CoinGecko Api, visit their [official documentation](https://www.coingecko.com/en/api).
