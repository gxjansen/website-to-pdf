import os
import asyncio
import tempfile
from urllib.parse import urlparse
from crawler import EthicalCrawler
from pdf_generator import generate_pdf
from PyPDF2 import PdfMerger, PdfReader
from PyPDF2.errors import PdfReadError

async def generate_pdfs_batch(urls, output_dir, batch_size=50):
    pdf_files = []
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        tasks = [generate_pdf(url, os.path.join(output_dir, f"page_{j}.pdf")) 
                 for j, url in enumerate(batch, start=i)]
        await asyncio.gather(*tasks)
        
        for j, url in enumerate(batch, start=i):
            output_path = os.path.join(output_dir, f"page_{j}.pdf")
            if os.path.exists(output_path):
                pdf_files.append(output_path)
    
    return pdf_files

def merge_pdfs(pdf_files, output_file):
    merger = PdfMerger()
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        for pdf_file in pdf_files:
            try:
                with open(pdf_file, 'rb') as file:
                    reader = PdfReader(file)
                    if len(reader.pages) > 0:
                        merger.append(reader)
                    else:
                        print(f"Skipping empty PDF: {pdf_file}")
            except PdfReadError:
                print(f"Error reading PDF: {pdf_file}. Skipping this file.")
            except Exception as e:
                print(f"Unexpected error with {pdf_file}: {str(e)}. Skipping this file.")
        
        # Write the merged PDF to the output file
        if len(merger.pages) > 0:
            with open(output_file, 'wb') as final_file:
                merger.write(final_file)
            print(f"Successfully created {output_file} with {len(merger.pages)} pages")
        else:
            print("No valid PDFs to merge. Output file not created.")
    
    merger.close()

async def main():
    # Prompt user for the domain to crawl
    start_url = input("Enter the full URL of the website you want to crawl (e.g., https://www.example.com): ")
    
    # Validate the input URL
    if not start_url.startswith(('http://', 'https://')):
        print("Invalid URL. Please include the protocol (http:// or https://)")
        return

    # Ask user for the number of pages to crawl or "All"
    while True:
        crawl_option = input("Enter the number of pages to crawl or 'All' for unlimited crawling: ").strip().lower()
        if crawl_option == 'all':
            limit = None
            break
        elif crawl_option.isdigit() and int(crawl_option) > 0:
            limit = int(crawl_option)
            break
        print("Invalid option. Please enter a positive integer or 'All'.")

    domain = urlparse(start_url).netloc
    output_dir = f"{domain}_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    # Crawl the site
    crawler = EthicalCrawler(start_url)
    urls = crawler.crawl(limit=limit)
    print(f"Crawled {len(urls)} URLs.")

    # Generate PDFs in batches
    pdf_files = await generate_pdfs_batch(urls, output_dir)

    # Merge PDFs
    if pdf_files:
        output_file = f"{domain}_complete{'_' + str(limit) if limit else ''}.pdf"
        merge_pdfs(pdf_files, output_file)
    else:
        print("No PDFs were generated.")

    # Cleanup individual PDF files, but keep the directory
    for pdf in pdf_files:
        try:
            os.remove(pdf)
        except Exception as e:
            print(f"Error removing file {pdf}: {str(e)}")
    
    print(f"Temporary files have been removed. The output directory '{output_dir}' has been kept for your reference.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
