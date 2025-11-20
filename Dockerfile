FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the port Render uses internally (10000)
EXPOSE 10000

# Start the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
