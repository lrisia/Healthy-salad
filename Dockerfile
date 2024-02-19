FROM python:3.10-slim

# Create and change directory to /app
WORKDIR /app

# Install add required packages
ADD requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --system --no-create-home python
USER python

ADD --chown=user:python ["src", "/app/src"]

EXPOSE $SERVER_PORT

# CMD gunicorn --bind :$SERVER_PORT --workers 1 --threads 8 --timeout 0 main:app
CMD [ "python3", "src/main.py"]