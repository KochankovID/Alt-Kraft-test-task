FROM python:3.10

RUN pip install poetry==1.1.13

WORKDIR /service
COPY ./pyproject.toml /service/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

COPY . .

CMD ["bash", "./scripts/fastApi-entrypoint.sh"]
