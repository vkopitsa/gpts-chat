FROM python:3.10-slim

RUN apt-get update && apt-get install libpq-dev -y && apt-get install git tree gcc build-essential --no-install-recommends -y

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create a non-root user and switch to it
RUN apt-get update && apt-get install ssh --no-install-recommends -y
RUN useradd -m -u 1000 python
USER python

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app/

CMD ["uvicorn", "--workers", "2", "--backlog", "100", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
