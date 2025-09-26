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

# पहले requirements.txt कॉपी करके root user से install करो
COPY requirements.txt /app/
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

# फिर बाकी कोड कॉपी करो और ownership botuser को दो
COPY --chown=botuser:botuser . /app/

# अब non-root user पर switch करो
USER botuser

CMD ["python3", "main.py"]
