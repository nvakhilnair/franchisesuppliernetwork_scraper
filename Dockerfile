# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Create the output directory
RUN mkdir -p /app/output

# Run the scrapy command
CMD ["scrapy", "crawl", "franchise_spider", "-o", "/app/output/reference_report.csv"]
