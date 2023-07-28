from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
import logging

from api.users import users_router
from domain_logic.user_repo import NonExistingUserId

app = FastAPI(debug=True,
              description="A place to track/see and see cryptocurrency prices",
              title="Crypto Fintech API",
              version="0.0.1"
              )

logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)

app.include_router(users_router)


@app.exception_handler(NonExistingUserId)
def return_400(_: Request, e: NonExistingUserId):
    return JSONResponse(status_code=400, content=str(e))


if __name__ == "__main__":
    import subprocess
    logging.info("Starting webserver...")
    try:
        subprocess.run(["uvicorn", "main:app", "--reload"])
    except KeyboardInterrupt as e:
        logging.warning("Keyboard interrupt.")
    except Exception as e:
        logging.warning("Webserver has stopped. Reason: " + str(e))


