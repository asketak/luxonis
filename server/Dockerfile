# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application's source code into the container at /app
COPY . /app/

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP app.py

# Run app.py when the container launches
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
