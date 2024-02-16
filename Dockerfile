FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
 && apt-get -y install \
            curl \
            gcc \
            git \
            libpq-dev \
            ssh \
 && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip


WORKDIR /app

RUN mkdir -p ./logs/app/

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

RUN python -m compileall src/

ENV PORT 8000

RUN echo "#!/bin/bash" > /entrypoint.sh && \
    # echo "uvicorn src.main:app --host 0.0.0.0 --port $PORT --no-access-log --workers 2 --loop uvloop" >> /entrypoint.sh && \
    echo "uvicorn src.main:app --host 0.0.0.0 --port $PORT --no-access-log" >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
