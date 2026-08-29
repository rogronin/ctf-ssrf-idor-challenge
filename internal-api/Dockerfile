FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py init_db.py ./

# Build the database INSIDE the image at build time.
# This means documents.db never needs to exist on your host machine or in Git.
RUN python init_db.py

EXPOSE 8000

CMD ["python", "app.py"]