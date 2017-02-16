FROM python:3.5.1
MAINTAINER Richard Chien <richardchienthebest@gmail.com>

COPY *.py ./
COPY msg_src_adapters msg_src_adapters
COPY filters filters
COPY commands commands
COPY nl_processors nl_processors
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y libav-tools \
    && rm -rf /var/lib/apt/lists/*

CMD python app.py