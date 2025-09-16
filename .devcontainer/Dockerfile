FROM python:3.12.11-slim-bookworm

USER root

# Python向けの基本的なツールをインストール
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential python3-dev curl net-tools lsof && \
    python -m pip install --upgrade pip setuptools wheel debugpy black isort && \
    rm -rf /var/lib/apt/lists/*

# ngrokのインストール
RUN curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o ngrok.tgz && \
    tar -xvzf ngrok.tgz -C /usr/local/bin && \
    rm ngrok.tgz

WORKDIR /workspaces/AnimeListDistributionBot
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 5678
