# Web Crawler PDF Generator

I needed a crawler to generate PDF files that can be used to train/customize LLMs with.

This Python-based tool crawls a specified website, generates PDFs of the crawled pages, and merges them into a single PDF document. It's designed to be ethical and respectful of the target website's resources.

## How to Use

1. **Setup**:
   - Ensure you have Python 3.7+ installed on your system.
   - Clone this repository to your local machine.
   - Install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

2. **Running the Script**:
   - Open a terminal and navigate to the project directory.
   - Run the main script:
     ```
     python main.py
     ```
   - Follow the prompts:
     - Enter the full URL of the website you want to crawl (e.g., https://www.example.com).
     - Enter the number of pages you want to crawl, or type 'All' for unlimited crawling.

3. **Output**:
   - The script will create a directory named `[domain]_pdfs` (e.g., `example.com_pdfs`).
   - A merged PDF file will be generated in the project directory, named `[domain]_complete[_limit].pdf` (e.g., `example.com_complete_10.pdf` for 10 pages, or `example.com_complete.pdf` for unlimited crawling).

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

## Troubleshooting

- If you encounter any issues with PDF generation or merging, check the console output for error messages.
- Ensure you have a stable internet connection throughout the crawling process.
- For large websites, consider starting with a small number of pages to test the process before attempting to crawl the entire site.

## Contributing

Contributions to improve the tool are welcome. Please feel free to submit issues or pull requests on GitHub.

## License

This project is open-source and available under the MIT License.
