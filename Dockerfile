FROM python:3.7-alpine as builder

WORKDIR /app

RUN apk add --no-cache build-base libffi-dev openssl-dev \
    && pip install poetry

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install -n --no-dev

COPY exchange_price_exporter exchange_price_exporter

RUN poetry build -n -f wheel

FROM python:3.7-alpine

WORKDIR /app

COPY --from=builder /app/dist /app
COPY config.toml /app/config.toml

RUN pip install exchange_price_exporter-*.whl

ENTRYPOINT [ "exchange-price-exporter" ]
