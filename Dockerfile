# बेस इमेज (स्लिम और सिक्योर)
FROM python:3.10-slim

# Env variables (python cache disable + path)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# वर्किंग डायरेक्टरी बनाओ
WORKDIR /app

# non-root user बनाओ (सिक्योरिटी के लिये)
RUN adduser --disabled-password --gecos '' botuser
USER botuser

# पहले requirements.txt कॉपी करो और install करो
COPY --chown=botuser:botuser requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# बाकी सारे कोड कॉपी करो
COPY --chown=botuser:botuser . /app/

# Container start होने पर main.py run होगा
CMD ["python3", "main.py"]
