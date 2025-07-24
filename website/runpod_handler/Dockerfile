FROM python:3.10-slim

WORKDIR /

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your handler file
COPY handler.py requirements.txt ./

# Start the container
CMD ["python3", "-u", "handler.py"]