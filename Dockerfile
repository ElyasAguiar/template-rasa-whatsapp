FROM python:3.9-slim

WORKDIR /core


COPY ./requirements.txt /tmp

# Install and Configure base packages and dependencies
RUN apt-get update                                                  && \
    apt-get install -y build-essential curl                         && \
    python -m pip install --upgrade pip                             && \
    pip install --no-cache-dir -r /tmp/requirements.txt             && \
    find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf    && \
    apt-get clean                                                   && \
    apt-get remove -y build-essential

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
COPY . /core
RUN rasa telemetry disable

RUN chmod +x /docker-entrypoint.sh

EXPOSE 5005

ENTRYPOINT ["/docker-entrypoint.sh"]