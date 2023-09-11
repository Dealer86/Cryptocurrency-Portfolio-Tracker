import logging
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from api.crypto import crypto_router
from api.users import users_router
from configuration.config import InvalidDataBase

app = FastAPI(
    debug=True,
    description="A place to track/see and see cryptocurrency prices",
    title="Crypto Fintech API",
    version="1.0.2",
)

logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)

app.include_router(users_router)
app.include_router(crypto_router)


@app.exception_handler(InvalidDataBase)
def return_invalid_database(_: Request, e: InvalidDataBase):
    logging.warning(f"Invalid database selected. Reason: {str(e)}")
    return JSONResponse(status_code=404, content=str(e))


if __name__ == "__main__":
    import subprocess

    logging.info("Starting webserver...")
    try:
        subprocess.run(["uvicorn", "main:app", "--reload"])
    except KeyboardInterrupt as e:
        logging.warning("Keyboard interrupt.")
    except Exception as e:
        logging.warning("Webserver has stopped. Reason: " + str(e))
