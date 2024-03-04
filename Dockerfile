FROM python:3.10-slim

# Create and change directory to /app
WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Install add required packages
ADD requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --system --no-create-home python
USER python

ADD --chown=python:nogroup ["src", "/app/src"]

EXPOSE 8000

D CFIO;
=_";¸ENTRYPOINT [ "python3" ]
CMD ["src/index.py", "api-start"]