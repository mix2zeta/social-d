FROM python:3.7-slim

WORKDIR /usr/src
COPY /requirements.txt /app/requirements.txt
RUN set -xe \
    # && apt-get update -q \
    # && apt-get install -y curl \
    && python3 -m pip install -r /app/requirements.txt \
    # && apt-get remove -y python3-pip python3-wheel \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -f *.whl \
    && rm -rf /var/lib/apt/lists/*

COPY /src /usr/src