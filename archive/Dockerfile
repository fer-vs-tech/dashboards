# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster as python_slim_gcc

ENV ACCEPT_EULA=Y

ADD requirements.txt .

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get --no-install-recommends install -y gnupg curl g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
    unixodbc-dev \
    msodbcsql17 \
    && python -m pip install --no-cache-dir -r ./requirements.txt \
    && apt-get remove -y g++ \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM python_slim_gcc as modeldash

EXPOSE 5050

WORKDIR /app
COPY . .

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser \
    && mkdir /home/modelrunner \
    && chown -R appuser /home/modelrunner \
    && chown -R appuser /app
USER appuser

CMD ["python", "modeldash.py"]