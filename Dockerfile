# Python + Debian 11 (Bullseye) base image
FROM python:3.9-slim-bullseye

# Workdir
WORKDIR /app
COPY . .

# Noninteractive environment
ENV DEBIAN_FRONTEND=noninteractive

# Update & install dependencies
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
        build-essential \
        curl \
        git \
        cmake \
        aria2 \
        wget \
        pv \
        jq \
        python3-dev \
        ffmpeg \
        mediainfo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone and build Bento4
RUN git clone https://github.com/axiomatic-systems/Bento4.git /tmp/Bento4 && \
    mkdir /tmp/Bento4/cmakebuild && \
    cd /tmp/Bento4/cmakebuild && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make && \
    make install && \
    rm -rf /tmp/Bento4

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Default command
CMD ["sh", "start.sh"]
