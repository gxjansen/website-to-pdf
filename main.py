import os
import asyncio
import tempfile
import json
from urllib.parse import urlparse
from crawler import EthicalCrawler
from pdf_generator import generate_pdf
from pdf_optimizer import optimize_pdf
from PyPDF2 import PdfMerger, PdfReader
from PyPDF2.errors import PdfReadError

async def generate_pdfs_batch(urls, output_dir, batch_size=50, size_limit=None):
    pdf_files = []
    current_merged_size = 0
    current_merge_group = []
    merge_group_number = 1

    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        tasks = [generate_pdf(url, os.path.join(output_dir, f"page_{j}.pdf")) 
                 for j, url in enumerate(batch, start=i)]
        await asyncio.gather(*tasks)
        
        for j, url in enumerate(batch, start=i):
            output_path = os.path.join(output_dir, f"page_{j}.pdf")
            if os.path.exists(output_path):
                optimized_path = os.path.join(output_dir, f"optimized_page_{j}.pdf")
                try:
                    optimize_pdf(output_path, optimized_path)
                    file_size = os.path.getsize(optimized_path) / (1024 * 1024)  # Size in MB
                    
                    if size_limit and (current_merged_size + file_size > size_limit):
                        # Merge the current group and start a new one
                        merged_path = merge_pdf_group(current_merge_group, output_dir, merge_group_number)
                        pdf_files.append(merged_path)
                        current_merge_group = []
                        current_merged_size = 0
                        merge_group_number += 1

                    current_merge_group.append(optimized_path)
                    current_merged_size += file_size

                except Exception as e:
                    print(f"Error optimizing PDF for {url}: {str(e)}")
                    current_merge_group.append(output_path)
                finally:
                    if os.path.exists(output_path):
                        os.remove(output_path)  # Remove the original, unoptimized PDF

    # Merge any remaining PDFs
    if current_merge_group:
        merged_path = merge_pdf_group(current_merge_group, output_dir, merge_group_number)
        pdf_files.append(merged_path)

    return pdf_files

def merge_pdf_group(pdf_group, output_dir, group_number):
    merger = PdfMerger()
    
    for pdf_file in pdf_group:
        try:
            reader = PdfReader(pdf_file)
            if len(reader.pages) > 0:
                merger.append(reader)
            else:
                print(f"Skipping empty PDF: {pdf_file}")
        except PdfReadError:
            print(f"Error reading PDF: {pdf_file}. Skipping this file.")
        except Exception as e:
            print(f"Unexpected error with {pdf_file}: {str(e)}. Skipping this file.")
    
    output_file = os.path.join(output_dir, f"merged_group_{group_number}.pdf")
    if len(merger.pages) > 0:
        merger.write(output_file)
        print(f"Successfully created {output_file} with {len(merger.pages)} pages")
    else:
        print(f"No valid PDFs to merge for group {group_number}. Output file not created.")
    
    merger.close()
    
    # Clean up individual PDF files
    for pdf_file in pdf_group:
        try:
            os.remove(pdf_file)
        except Exception as e:
            print(f"Error removing file {pdf_file}: {str(e)}")
    
    return output_file

def check_existing_crawl_data():
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        if item.endswith('_crawl_data.json'):
            return os.path.join(current_dir, item)
    return None

def load_crawl_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['start_url'], data['urls']

def save_crawl_data(start_url, urls, filename):
    data = {
        'start_url': start_url,
        'urls': urls
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

async def new_crawl():
    # Prompt user for the domain to crawl
    start_url = input("Enter the full URL of the website you want to crawl (e.g., https://www.example.com): ")
    
    # Validate the input URL
    if not start_url.startswith(('http://', 'https://')):
        print("Invalid URL. Please include the protocol (http:// or https://)")
        return None, [], None

    # Inform user about the ignore file
    print("\nNote: You can add URLs to ignore in the 'ignore-urls.txt' file.")
    print("The crawler will skip any URLs that match the patterns in this file.")
    print("You can use '*' as a wildcard in the ignore patterns.")

    # Ask user for the number of pages to crawl or "All"
    while True:
        crawl_option = input("\nEnter the number of pages to crawl or 'All' for unlimited crawling: ").strip().lower()
        if crawl_option == 'all':
            limit = None
            break
        elif crawl_option.isdigit() and int(crawl_option) > 0:
            limit = int(crawl_option)
            break
        print("Invalid option. Please enter a positive integer or 'All'.")

    # Ask for file size limit
    while True:
        size_limit_input = input("Enter the maximum size per PDF in MB (5 or higher), or 'no' for no limit: ").strip().lower()
        if size_limit_input == 'no':
            size_limit = None
            break
        elif size_limit_input.isdigit() and int(size_limit_input) >= 5:
            size_limit = int(size_limit_input)
            break
        print("Invalid input. Please enter a number 5 or higher, or 'no'.")

    # Crawl the site
    crawler = EthicalCrawler(start_url)
    urls = crawler.crawl(limit=limit)
    print(f"Crawled {len(urls)} URLs.")

    # Save crawl data
    domain = urlparse(start_url).netloc
    save_crawl_data(start_url, urls, f"{domain}_crawl_data.json")

    return start_url, urls, size_limit

async def main():
    existing_data = check_existing_crawl_data()
    
    if existing_data:
        print(f"Existing crawl data found: {existing_data}")
        use_existing = input("Do you want to use this data? (yes/no): ").strip().lower()
        if use_existing == 'yes':
            start_url, urls = load_crawl_data(existing_data)
            print(f"Using existing crawl data for {start_url} with {len(urls)} URLs.")
            # Ask for file size limit when using existing data
            while True:
                size_limit_input = input("Enter the maximum size per PDF in MB (5 or higher), or 'no' for no limit: ").strip().lower()
                if size_limit_input == 'no':
                    size_limit = None
                    break
                elif size_limit_input.isdigit() and int(size_limit_input) >= 5:
                    size_limit = int(size_limit_input)
                    break
                print("Invalid input. Please enter a number 5 or higher, or 'no'.")
        else:
            start_url, urls, size_limit = await new_crawl()
    else:
        print("No existing crawl data found.")
        start_url, urls, size_limit = await new_crawl()

    domain = urlparse(start_url).netloc
    output_dir = f"{domain}_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    # Generate PDFs in batches
    pdf_files = await generate_pdfs_batch(urls, output_dir, size_limit=size_limit)

    print(f"PDF generation complete. Generated {len(pdf_files)} PDF file(s).")
    for pdf_file in pdf_files:
        print(f"- {pdf_file} (Size: {os.path.getsize(pdf_file) / (1024 * 1024):.2f} MB)")

    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
