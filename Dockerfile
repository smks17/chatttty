# Use the official Python runtime image
FROM python:3.12
RUN mkdir /app
WORKDIR /app
# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Build
RUN pip install --upgrade pip
COPY . .
RUN chmod +x ./build.sh
RUN ./build.sh

# Run Django’s server
CMD ["/app/entrypoint.sh"]
