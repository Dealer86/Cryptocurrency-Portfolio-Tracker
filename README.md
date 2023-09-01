# Cryptocurrency Portfolio Tracker

Cryptocurrency Portfolio Tracker, designed for managing and analyzing cryptocurrency investments, is a web server with REST API that allows you to keep track of your cryptocurrency and compare their evolution over time.

## Deployment Instructions

### Windows
1. Clone the git repository using `<git_repo_url>`.
2. Navigate to the `cd <your-created-directory>` directory.
3. Create a new virtual environment by running `python -m venv env/`.
4. Activate the virtual environment by running `.\env\Scripts\activate`.
5. Upgrade pip by running `python.exe -m pip install --upgrade pip`.
6. Install the required dependencies by running `pip install -r requirements.txt`.
7. Configure database settings(pick sqlite3 or json) in the config.json file found in configuration file.
8. Run main.py location -> finance-project folder.
9. Check [swagger](http://127.0.0.1:8000/docs). 

## Technology Stack
Leveraging modern tools such as FastAPI, Uvicorn, Json and sqlite3 as databases along with integration of financial API(CoinGecko), this project showcases my skills in both backend development and fintech API integration.
Following SOLID principles, employing design patterns, and adhering to Domain-Driven Design (DDD) concepts, I've created a robust and extensible application.

This project uses the following technologies:
* FastAPI - a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
* Uvicorn - a lightning-fast ASGI server, built on top of the asyncio event loop.
* Matplotlib - a Python library for creating static, animated, and interactive visualizations in Python.
* Sqlite3 - SQLite is library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
* CoinGecko API - cryptocurrency data API for traders and developers.

## Resources

For more information about FastAPI, visit their [official documentation](https://fastapi.tiangolo.com/).

For more information about Uvicorn, visit their [official documentation](https://www.uvicorn.org/).

For more information about Matplotlib, visit their [official documentation](https://matplotlib.org/stable/index.html).

For more information about Sqlite3, visit their [official documentation](https://www.sqlite.org/index.html).

For more information about CoinGecko Api, visit their [official documentation](https://www.coingecko.com/en/api).
