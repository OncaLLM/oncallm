FROM python:3.11-slim

WORKDIR /app

# Set environment variables for port consistency
ENV APP_PORT=8001
ENV APP_HOST=0.0.0.0

# Copy only the final requirements.txt
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# Ensure only 'oncallm' directory and 'ui' (if it's part of the runtime) are copied.
# This is better handled by .dockerignore, but let's be specific here too.
COPY ./oncallm /app/oncallm
# If Streamlit app is run from the same container and needs these files
COPY ./ui /app/ui 
EXPOSE $APP_PORT

# Command to run the application using Uvicorn
# Note: oncallm/main.py uses os.environ.get("APP_PORT", 8001), so APP_PORT env var will be respected.
CMD uvicorn oncallm.main:app --host ${APP_HOST} --port ${APP_PORT}
