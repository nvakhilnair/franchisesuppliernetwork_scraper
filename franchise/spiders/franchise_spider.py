import os
from urllib.parse import urlparse

import scrapy
from lxml.html import fromstring

from ..items import ReferencesStats


class FranchiseSpiderSpider(scrapy.Spider):
    name = "franchise_spider"
    allowed_domains = ["franchisesuppliernetwork.com"]
    start_urls = ["https://franchisesuppliernetwork.com/"]

    def get_path(self, parsed_url):
        """
        Generate a file path based on the parsed URL.

        Args:
            parsed_url (ParseResult): The parsed URL object containing components like scheme, netloc, path, etc.

        Returns:
            str: The generated file path based on the parsed URL.
                If the path is '/' or '', the page is considered the homepage and the path '/output/downloaded_data/homepage/' is returned.
                Otherwise, the path '/output/downloaded_data' concatenated with the parsed URL's path component is returned.
        """
        if parsed_url.path == "/" or parsed_url.path == "":
            return "./output/downloaded_data/homepage/"
        return "./output/downloaded_data" + parsed_url.path

    def get_stats(self, path, text_list, classified_urls_list):
        """
        Calculate statistics based on extracted data.

        Args: A dictionary containing classified URLs with thei
            path (str): The path of the webpage from which the data is extracted.
            text_list (list): A list containing the extracted text data.
            classified_urls_list (dict): A dictionary containing classified URLs with their extension types.

        Returns:
            dict: A dictionary containing statistics based on the extracted data and classified URLs.
                - 'page': The path of the webpage relative to the '/output/downloaded_data' directory.
                - 'text_extracted': The number of unique text elements extracted from the webpage.
                - 'resources_referenced': A dictionary where keys are different types of resource extensions (e.g., 'jpg', 'css', 'js') and values are the counts of resources referenced of that type.

        """
        stats = {}
        resources_refereced = {}
        for extension_type in classified_urls_list.keys():
            resources_refereced[extension_type] = len(
                classified_urls_list[extension_type]
            )
        stats["page"] = path.replace("./output/downloaded_data", "")
        stats["text_extracted"] = len(set(text_list))
        stats["resources_refereced"] = resources_refereced
        return stats

    def classify_urls(self, urls_list):
        """
        Classify URLs based on their extension types.

        Args:
            urls_list (list): A list of URLs to be classified.

        Returns:
            dict: A dictionary containing classified URLs with their respective extension types as keys.
                The extension types are determined by parsing the URL paths.
                If the URL path ends with an extension (e.g., '.jpg', '.html'), that extension is used.
                If the URL path does not end with an extension, it is classified as 'page_urls'.

        """
        classified_urls = {}
        for url in urls_list:
            # Since its noticed that /fsn-members/ redirects to login
            if (
                url.startswith("https://franchisesuppliernetwork.com/")
                and "/fsn-members/" not in url
            ):
                parsed_url = urlparse(url)
                extension = os.path.basename(parsed_url.path)
                if len(extension.split(".")) >= 2:
                    extension = extension.split(".")[-1]
                else:
                    extension = "page_urls"
                if extension not in classified_urls:
                    classified_urls[extension] = []
                classified_urls[extension].append(url)
        return classified_urls

    def save_text_file(self, path, text_list):
        """
        Save text data to a text file.

        Args:
            path (str): The path where the text file will be saved.
            text_list (list): A list containing the text data to be saved.
        """
        texts = "\n".join(text_list)
        filename = os.path.join(f"{path}text.txt")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.writelines(texts)

    def parse(self, response):
        # Initialising Parser
        parser = fromstring(response.text)

        # Extract all the text inside html body under <p> tag and using set to remove duplicates
        texts_list = set(parser.xpath("//body//p//text()"))

        # Extract all the src urls inside html body under <img> and using set to remove duplicates
        images_urls_set = set(parser.xpath("//body//img/@src"))

        # Extract all the href urls inside html body under <a> and using set to remove duplicates
        reference_urls_set = set(parser.xpath("//body//a/@href"))

        # Parseing the request url so that it can be used to arrange the files in dir
        parsed_url = urlparse(response.request.url)
        path = self.get_path(parsed_url)

        # Combine URLs set
        urls_list = sorted(images_urls_set.union(reference_urls_set))

        # Classifying the urls based on file extension
        classified_urls_list = self.classify_urls(urls_list)

        # Getting the stats
        stats = self.get_stats(path, texts_list, classified_urls_list)
        yield ReferencesStats(**stats)

        # Saving textual data
        self.save_text_file(path, texts_list)

        # Spliting and remove page_urls
        page_urls = classified_urls_list.get("page_urls")
        files_urls = classified_urls_list
        files_urls.pop("page_urls")

        for file_extension in files_urls.keys():
            for file_url in files_urls[file_extension]:
                meta = {"file_url": file_url, "path": path}
                yield scrapy.Request(
                    url=file_url,
                    dont_filter=False,
                    callback=self.download_file,
                    meta=meta,
                )
        for page_url in page_urls:
            yield scrapy.Request(url=page_url, dont_filter=False, callback=self.parse)

    def download_file(self, response):
        """
        Download a file from the response and save it to disk.

        Args:
            response (scrapy.http.Response): The response object containing the file to be downloaded.
        """
        meta = response.meta
        file_url = meta.get("file_url")
        path = meta.get("path")
        parsed_file_url = urlparse(file_url)
        filename = os.path.join(f"{path}files/", os.path.basename(parsed_file_url.path))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            f.write(response.body)
