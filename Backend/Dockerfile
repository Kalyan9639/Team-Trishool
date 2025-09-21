# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Pre-copy requirements to leverage caching
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the model once (adjust model name if needed)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the rest of the code
COPY backend/ .

# Expose port
EXPOSE 8080

# Start the app (adjust if using Flask)
CMD ["uvicorn", "final_main:app", "--host", "0.0.0.0", "--port", "8080"]
