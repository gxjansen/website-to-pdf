import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random
from urllib.robotparser import RobotFileParser
from requests.exceptions import RequestException
import re

class EthicalCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited = set()
        self.user_agent = 'EthicalCrawler/1.0'
        self.robot_parser = RobotFileParser()
        self.robot_parser.set_url(urljoin(start_url, '/robots.txt'))
        self.robot_parser.read()
        self.crawl_delay = self.get_crawl_delay()
        self.ignore_patterns = self.load_ignore_patterns()

    def get_crawl_delay(self):
        crawl_delay = self.robot_parser.crawl_delay('*')
        return crawl_delay if crawl_delay is not None else 1

    def can_fetch(self, url):
        return self.robot_parser.can_fetch(self.user_agent, url)

    def adaptive_delay(self, response_time):
        delay = max(self.crawl_delay, response_time * 2)
        time.sleep(delay + random.uniform(0.5, 1.5))

    def load_ignore_patterns(self):
        patterns = []
        try:
            with open('ignore-urls.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        pattern = line.replace('*', '.*')  # Convert wildcard to regex
                        patterns.append(re.compile(pattern))
        except FileNotFoundError:
            print("ignore-urls.txt not found. No URLs will be ignored.")
        return patterns

    def should_ignore(self, url):
        return any(pattern.match(url) for pattern in self.ignore_patterns)

    def get_links(self, url):
        try:
            start_time = time.time()
            response = requests.get(url, headers={'User-Agent': self.user_agent})
            response_time = time.time() - start_time
            
            self.adaptive_delay(response_time)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        full_url = urljoin(url, href)
                        if urlparse(full_url).netloc == self.domain and '#' not in full_url:
                            if not self.should_ignore(full_url):
                                links.append(full_url)
                            else:
                                print(f"Ignoring URL: {full_url}")
                return links
            else:
                print(f"Failed to fetch {url}: HTTP {response.status_code}")
                return []
        except RequestException as e:
            print(f"Error fetching {url}: {e}")
            return []

    def crawl(self, limit=None):
        to_visit = [self.start_url]
        while to_visit and (limit is None or len(self.visited) < limit):
            url = to_visit.pop(0)
            if url not in self.visited and self.can_fetch(url) and not self.should_ignore(url):
                print(f"Crawling: {url}")
                self.visited.add(url)
                for link in self.get_links(url):
                    if link not in self.visited and link not in to_visit:
                        to_visit.append(link)
                        
                if limit and len(self.visited) >= limit:
                    break

        return list(self.visited)
