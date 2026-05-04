FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

EXPOSE 8006

COPY entrypoint.sh /entrypoint.sh

CMD ["/entrypoint.sh"]