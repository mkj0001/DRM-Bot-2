FROM python:3.9.7-slim-bullseye

# Workdir
WORKDIR /app

# Copy all project files into the image
COPY . .

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential curl git cmake aria2 wget pv jq python3-dev ffmpeg mediainfo \
 && rm -rf /var/lib/apt/lists/*

# Build Bento4
RUN git clone https://github.com/axiomatic-systems/Bento4.git /tmp/Bento4 && \
    mkdir /tmp/Bento4/cmakebuild && \
    cd /tmp/Bento4/cmakebuild && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make && make install && \
    rm -rf /tmp/Bento4

# Python dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Entrypoint – run your handlers/tg.py file
CMD ["python3","-u","handlers/tg.py"]
