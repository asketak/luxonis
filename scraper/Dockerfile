# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Install any necessary dependencies for your Scrapy spider
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy your Scrapy project into the container at /app
COPY . /app/my_scraper/

# Change to the Scrapy project directory
WORKDIR /app/my_scraper/


CMD ["scrapy", "crawl", "my_spider", "--set=ROBOTSTXT_OBEY=False"]
