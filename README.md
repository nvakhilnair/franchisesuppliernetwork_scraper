# Running Franchise Spider Scraper with Docker

This repository contains a Dockerfile and a Scrapy spider for scraping franchise information. Follow the steps below to run the spider using Docker.

Find the Analysis report as the a csv file named `scrape_report.csv` also with reference doc of it named `scrape_report.pdf`

## Steps to Run

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Navigate to the Repository Directory**: Open a terminal and navigate to the directory where you cloned the repository.

3. **Build the Docker Image**: Run the following command to build the Docker image:

    ```bash
    docker build -t franchise_scrapy .
    ```

4. **Run the Docker Container**: Use the following command to run the Docker container. Replace `/path/to/local/directory` with the directory where you want to save the output files:

    ```bash
    docker run -v /path/to/local/directory:/app/output franchise_scrapy
    ```

## About Saved Files

- **reference_report.csv**: This file contains the scraped data in CSV format. It will be saved in the specified output directory.

- **downloaded_data/**: This directory contains any additional data downloaded by the spider. It will be saved in the specified output directory.

### Note:

- Ensure that the directory provided for volume mounting (`/path/to/local/directory`) is accessible and writable by the Docker container.
- After running the Docker container, you can find the output files in the specified output directory on your local machine.

## Reference Documentation

For understanding the structure and content of the output data, please refer to the following documentation:

- [Notes Doc](https://docs.google.com/document/d/1prsJgQHLV1x2Bi2i74Kv5ZD_3_E6rc5FG6qHU45uNec/edit?usp=sharing)
- [Scrape Report Doc](https://docs.google.com/document/d/1vGhceUd_91wUktXpdtU40IPjIQj0GiLas477Nlgau4s/edit?usp=sharing)
