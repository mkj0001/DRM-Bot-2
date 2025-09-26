FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN adduser --disabled-password --gecos '' botuser
USER botuser

COPY --chown=botuser:botuser requirements.txt /app/
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

COPY --chown=botuser:botuser . /app/

CMD ["python3", "main.py"]
