FROM python:3.10-slim

WORKDIR /

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your handler file
COPY handler.py requirements.txt ./

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Start the container
CMD ["python3", "-u", "handler.py"]