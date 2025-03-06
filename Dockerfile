FROM ghcr.io/astral-sh/uv:0.6.4 as uv

FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache \
    gcc g++ gfortran musl-dev linux-headers \
    python3-dev lapack-dev

RUN --mount=from=uv,source=/uv,target=./uv \
    ./uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=from=uv,source=/uv,target=./uv \
    ./uv pip install  -r requirements.txt gunicorn

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
