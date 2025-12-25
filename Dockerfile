FROM python:3.11-slim

WORKDIR /app

# Install pytest
RUN pip install --no-cache-dir pytest

# Copy project files
COPY src/ ./src/
COPY test/ ./test/

# Set the entry point
CMD ["python", "src/admin.py"]