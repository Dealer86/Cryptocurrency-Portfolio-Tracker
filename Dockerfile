FROM python:3.11.4

WORKDIR /code

ENV PORT 8000

# Copy only the necessary files and directories
COPY finance-project /code/finance-project
COPY requirements.txt /code/requirements.txt
COPY tests /code/tests
COPY README.md /code/README.md

RUN pip install -r requirements.txt

WORKDIR /code/finance-project

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
