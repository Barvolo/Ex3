FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt with verbose output
RUN pip install --no-cache-dir -r requirements.txt -v

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run the app with Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]