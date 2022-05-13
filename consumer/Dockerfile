FROM python:3.10

RUN pip install poetry==1.1.13

WORKDIR /producer
COPY ./pyproject.toml /producer/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

COPY . .

CMD ["python", "main.py"]
