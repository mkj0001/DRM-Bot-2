# Base image
FROM python:3.9.7-slim-bullseye

# Workdir container के अंदर /app
WORKDIR /app

# Project files container में copy
COPY . .

# Dependencies install + Bento4 build
RUN apt-get update -y && \
    apt-get install -y build-essential curl git cmake aria2 wget pv jq python3-dev ffmpeg mediainfo && \
    git clone https://github.com/axiomatic-systems/Bento4.git && \
    cd Bento4 && \
    mkdir cmakebuild && \
    cd cmakebuild && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make && \
    make install

# Python requirements install
RUN pip3 install --no-cache-dir -r requirements.txt

# Container start होने पर ये script चलेगा
CMD ["sh", "start.sh"]
