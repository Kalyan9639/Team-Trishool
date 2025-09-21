# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start FastAPI app from final_main.py
CMD ["uvicorn", "final_main:app", "--host", "0.0.0.0", "--port", "8080"]
