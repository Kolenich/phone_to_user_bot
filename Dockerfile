FROM python:alpine
WORKDIR /app
RUN pip install -U pip -U setuptools
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x ./dockerentrypoint.sh
ENTRYPOINT ["./dockerentrypoint.sh"]
