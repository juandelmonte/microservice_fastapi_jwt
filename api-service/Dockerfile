FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies from requirements.txt for better caching and local dev parity
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]