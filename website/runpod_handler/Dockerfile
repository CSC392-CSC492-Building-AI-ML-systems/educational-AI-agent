FROM python:3.10-slim

WORKDIR /

# Copy requirements and install
COPY requirements.txt .
RUN pip install -U bitsandbytes
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler
COPY handler.py .

# Start the container
CMD ["python3", "-u", "handler.py"]
