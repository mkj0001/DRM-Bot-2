# 1. Lightweight Python base image
FROM python:3.10-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy all project files into container
COPY . /app

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Add /app to PYTHONPATH so imports like 'from main import ...' always work
ENV PYTHONPATH="/app"

# 6. Expose a port (optional, for health checks)
EXPOSE 8080

# 7. Run your main file when container starts
CMD ["pyt]()
