FROM python:3.10

ENV PYTHONUNBUFFERED 1


# Google Chrome installation
# Google Chrome dependencies Installation
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/`curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE`/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# Install Poetry
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

WORKDIR /app
COPY . /app/

RUN poetry install --no-root