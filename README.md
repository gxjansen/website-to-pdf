# Web Crawler PDF Generator

I needed a crawler to generate PDF files that can be used to train/customize/give context to LLMs.

This Python-based tool crawls a specified website, generates PDFs of the crawled pages, and merges them into a single PDF document. It's designed to be ethical and respectful of the target website's resources and created with help from Claude 3.5 Sonnet.

The script tries to remove common elements from the webpages like headers, footers and navigation items. It also includes a PDF optimization process to bring down the PDF size.

Below are some benchmarks of a crawled documentation website. The end result of course very much depends on the amount of content (text and images) on those pages.
- 10 URLs: 51 PDF pages, total 4,6 MB
- 165 URLs: 881 PDF pages, total 30,8 MB
- 300 URLs: 1636 PDF pages, total 72,7 MB

## Index:
- [Web Crawler PDF Generator](#web-crawler-pdf-generator)
  - [Index:](#index)
  - [How to Use](#how-to-use)
  - [How It Works](#how-it-works)
  - [Ethical Considerations](#ethical-considerations)
  - [System Requirements](#system-requirements)
    - [Hardware Requirements:](#hardware-requirements)
    - [Software Requirements:](#software-requirements)
    - [Python Dependencies:](#python-dependencies)
    - [Additional Notes:](#additional-notes)
    - [Recommended Setup:](#recommended-setup)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)

## How to Use

1. **Setup**:
 - Ensure you have Python 3.7+ installed on your system.
 - Clone this repository to your local machine.
 - Navigate to the project directory in your terminal.
 - (Optional but recommended) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
 - Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

This will install all necessary packages for the Web Crawler PDF Generator to run.

2. **Running the Script**:
   - Open a terminal and navigate to the project directory.
   - Run the main script:
     ```
     python main.py
     ```
   - Follow the prompts:
     - Enter the full URL of the website you want to crawl (e.g., https://www.example.com).
     - Enter the number of pages you want to crawl, or type 'All' for unlimited crawling.
     - Enter the maximum PDF file size your want (an integer staring at 10MB), or type "no" for unlimited filesize.

3. **Output**:
   - The script will create a directory named `[domain]_pdfs` (e.g., `example.com_pdfs`).
   - A merged PDF file will be generated in the project directory, named `[domain]_complete[_limit].pdf` (e.g., `example.com_complete_10.pdf` for 10 pages, or `example.com_complete.pdf` for unlimited crawling).
   - Depending on the data volume (amount of URLs and amount of text an images on those pages) and your system performance, crawling an generating the final PDFs can take quite some time.

## How It Works

1. **Crawling**: 
   - The script uses a custom `EthicalCrawler` class to crawl the specified website.
   - It respects `robots.txt` files and implements polite crawling practices.
   - The crawler can be limited to a specific number of pages or set to crawl all accessible pages.

2. **PDF Generation**:
   - For each crawled URL, the script generates a PDF using Pyppeteer (a Python port of Puppeteer).
   - PDFs are temporarily stored in the `[domain]_pdfs` directory.

3. **PDF Merging**:
   - After all individual PDFs are generated, they are merged into a single PDF file using PyPDF2.
   - The merged PDF is saved in the project directory.

4. **Cleanup**:
   - Individual PDF files are removed after merging to save disk space.
   - The `[domain]_pdfs` directory is kept for reference.

## Ethical Considerations

- The crawler respects `robots.txt` files and implements a polite delay between requests.
- It's designed to minimize impact on the target website's resources.
- Users should ensure they have permission to crawl and reproduce content from the target website.

## System Requirements
To run the Web Crawler PDF Generator effectively, your system should meet the following minimum requirements:

### Hardware Requirements:
* **Processor**: Multi-core processor (2+ cores recommended)
* **RAM**: Minimum 4GB, 8GB or more recommended
* **Storage**: At least 1GB of free disk space (more may be required depending on the size and number of PDFs generated)
* **Internet Connection**: Stable broadband internet connection

### Software Requirements:

* Operating System:
  * Windows 10 or later 
  * macOS 10.14 (Mojave) or later
  * Linux (Ubuntu 18.04+, Fedora 30+, or equivalent)
* Python: Version 3.7 or later
* pip: Latest version

### Python Dependencies:
The script requires the following Python libraries (these will be installed automatically when you run `pip install -r requirements.txt`):

* PyPDF2
* Pillow
* requests
* beautifulsoup4
* pyppeteer

### Additional Notes:
* **Browser**: The script uses pyppeteer, which requires a browser to be installed. It typically uses Chromium, which it can download automatically if not present.
* **Disk Space**: The amount of free disk space needed may vary significantly based on the number and size of PDFs being generated. Ensure you have ample free space, especially when crawling large websites.
* **Memory Usage**: The script's memory usage can spike when processing large PDFs or crawling extensive websites. If you're working with very large sites, more RAM will be beneficial.
* **Processing Time**: The time taken to crawl websites and generate PDFs can vary greatly depending on the size of the website, your internet connection speed, and your computer's processing power.

### Recommended Setup:
For optimal performance, especially when crawling larger websites or generating many PDFs, I'd recommend:

* A quad-core processor or better
* 16GB of RAM or more
* An SSD with at least 5GB of free space
* A high-speed internet connection

Please note that while the script may run on lower-spec systems, performance and processing times may be affected, particularly for larger jobs.

## Troubleshooting

- If you encounter any issues with PDF generation or merging, check the console output for error messages.
- Ensure you have a stable internet connection throughout the crawling process.
- For large websites, consider starting with a small number of pages to test the process before attempting to crawl the entire site.

## Contributing

Contributions to improve the tool are welcome. Please feel free to submit issues or pull requests on GitHub.

## License

This project is open-source and available under the MIT License.
