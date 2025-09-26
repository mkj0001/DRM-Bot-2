FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    DOWNLOAD_LOCATION=/app/DOWNLOADS

WORKDIR /app

# नया user बनाएँ
RUN adduser --disabled-password --gecos '' botuser

# पहले से DOWNLOADS folder बना दो और permission दे दो
RUN mkdir -p /app/DOWNLOADS && chown -R botuser:botuser /app

USER botuser

COPY --chown=botuser:botuser requirements.txt /app/
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

COPY --chown=botuser:botuser . /app/

CMD ["python3", "main.py"]
