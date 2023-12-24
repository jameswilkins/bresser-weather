# Use a multi-stage build to minimize the size of the final image
# Start with a larger image for building
FROM python:3.8-slim as builder


# Metadata
LABEL maintainer="jiwilkins@outlook.com"
LABEL version="0.1"
LABEL description="Bresser Weather Station API Listener"


# Set environment variables
ENV INFLUXDB_URL="http://localhost:8086"
ENV INFLUXDB_TOKEN="your-token"
ENV INFLUXDB_ORG="your-org"
ENV INFLUXDB_BUCKET="your-bucket"

# Set a working directory
WORKDIR /usr/src/app


# Install dependencies in a virtual environment
RUN python -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Use a separate layer for requirements to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files (exclude unnecessary files with .dockerignore)
COPY . .

# Final stage: use a smaller base image
FROM python:3.8-alpine

# Create a non-root user and switch to it
RUN adduser -D nonrootuser
USER nonrootuser

# Set working directory in the new image
WORKDIR /usr/src/app

# Copy virtual environment from builder stage
COPY --from=builder /usr/src/app/venv /usr/src/app/venv

# Set environment variables
ENV PATH="/usr/src/app/venv/bin:$PATH"
ENV NAME World

# Copy the application from the builder stage
COPY --from=builder /usr/src/app .
COPY health_check.py /usr/src/app/health_check.py
# Expose port 30000 for the application
EXPOSE 30000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python", "/usr/src/app/health_check.py" ]
# Run the application with Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:30000", "srv:app"]
